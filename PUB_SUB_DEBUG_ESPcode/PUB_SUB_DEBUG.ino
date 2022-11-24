#include <ESPmDNS.h>
#include <Arduino.h>
#include <driver/i2s.h>
#include <driver/adc.h>
#include <driver/dac.h>
#include <soc/syscon_reg.h>
#define FS_NO_GLOBALS
#include <FS.h>
#include "SPIFFS.h"
#include <stdlib.h>
#include <iostream>
#include "esp_spi_flash.h"
#include "esp_err.h"
#include "esp_log.h"
#include "esp_partition.h"
#include <assert.h>
#include <WiFi.h>
#define FS_NO_GLOBALS
#include <FS.h>
#include "SPIFFS.h"
#include <stdlib.h>
#include <ArduinoOTA.h>
#include "mqtt.h"
#include "ramQ.h"

#define payload_topic "Data"
//#define PARTITION_NAME   "storage"

/*---------------------------------------------------------------
                            EXAMPLE CONFIG
  ---------------------------------------------------------------*/

static volatile int RECORD_IN_FLASH_EN = 1;
static volatile int DATA_SEND = 0;
#define REPLAY_FROM_FLASH_EN      (1)

//enable display buffer for debug
#define EXAMPLE_I2S_BUF_DEBUG     (1)


#define EXAMPLE_I2S_SAMPLE_BITS   (16)
#define EXAMPLE_I2S_SAMPLE_RATE   (16000)
#define ADC_CHANNEL   ADC1_CHANNEL_4//
#define NUM_SAMPLES   1024                       // number of samples
#define I2S_NUM         (0)

//I2S read buffer length
#define EXAMPLE_I2S_READ_LEN      (16 * 1024)//(16 * 1024)


//sector size of flash
#define FLASH_SECTOR_SIZE         (0x4000)//(0x1000)
//flash read / write address
//flash record size, for recording n seconds' data
#define FLASH_RECORD_SIZE         (1 * EXAMPLE_I2S_SAMPLE_RATE * EXAMPLE_I2S_SAMPLE_BITS / 8 * 40)
#define FLASH_ERASE_SIZE          (FLASH_RECORD_SIZE % FLASH_SECTOR_SIZE == 0) ? FLASH_RECORD_SIZE : FLASH_RECORD_SIZE + (FLASH_SECTOR_SIZE - FLASH_RECORD_SIZE % FLASH_SECTOR_SIZE)

//sector size of flash
#define FLASH_ADDR                (0x200000)


#define PACKET_SIZE 2048*16//1024*8//1024*16//2048*16
#define PACKET_NO     1
TaskHandle_t Task0;
TaskHandle_t Task1;
SemaphoreHandle_t Semaphore;
QueueHandle_t queue;

uint8_t buf[PACKET_NO * PACKET_SIZE];
static uint8_t mqttMid = 1;



/***************************************
   Main Functions
 ****************************************/



void configure_i2s() {
  i2s_config_t i2s_config =
  {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX | I2S_MODE_TX | I2S_MODE_ADC_BUILT_IN), // I2S receive mode with ADC
    .sample_rate = EXAMPLE_I2S_SAMPLE_RATE ,                                             // sample rate
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,                                 // 16 bit I2S
    .channel_format = I2S_CHANNEL_FMT_ALL_LEFT,  //I2S_CHANNEL_FMT_RIGHT_LEFT,                                 // only the left channel
    .communication_format = (i2s_comm_format_t)(I2S_COMM_FORMAT_I2S | I2S_COMM_FORMAT_I2S_MSB),   // I2S format
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,             // or 0                                            // none
    .dma_buf_count = 2,                                                           // number of DMA buffers
    .dma_buf_len = NUM_SAMPLES,                                                   // number of samples
    .use_apll = 0,                                                                // no Audio PLL
  };

  adc1_config_channel_atten(ADC_CHANNEL, ADC_ATTEN_0db);
  adc1_config_width(ADC_WIDTH_12Bit);
  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);

  i2s_set_adc_mode(ADC_UNIT_1, ADC_CHANNEL);


  // This 32 bit register has 4 bytes for the first set of channels to scan.
  // Each byte consists of:
  // Scan multiple channels.
  // SET_PERI_REG_BITS(SYSCON_SARADC_CTRL_REG, SYSCON_SARADC_SAR1_PATT_LEN, 7, SYSCON_SARADC_SAR1_PATT_LEN_S);





}



/*void send_buf(uint8_t* buf, int length)
  {

   mqttConnect();
   ramQSet(&buf,length , 1);
   float T8=millis();
   static uint8_t mqttMid = 1;
   uint8_t *writePtr = (uint8_t*)ramQHead();
        if(writePtr != NULL)
        {
          writePtr=buf;
          ramQUpdateHead();
          Serial.println("|----Reading Finished----|");
        }
   Serial.print("TdisStart:");Serial.println(T8);

   float T2=millis();
   Serial.print("T2:");Serial.println(T2);

  uint8_t *readPtr = (uint8_t*)ramQRead();  /// reading data pointer from ramq
        if (readPtr != NULL)
        {
          if(mqttMid == 0) mqttMid++;
          Serial.println(F("<-----Read Data---->"));
          mqtt.publish(payload_topic,readPtr,PACKET_SIZE, mqttMid);
         // printSensor(readPtr,length);
          ramQUpdateTail();
          mqttMid++;
        }

   printf("======\n");

  }  */




void example_erase_flash(void *parameter)
{
  while (1) {
    if (RECORD_IN_FLASH_EN)
    {
      printf("Erasing flash \n");
      const esp_partition_t *data_partition = NULL;

      data_partition = esp_partition_find_first(ESP_PARTITION_TYPE_DATA, ESP_PARTITION_SUBTYPE_DATA_SPIFFS, "spiffs");
      if (data_partition != NULL) {
        Serial.printf("SPIFFS partiton addr: 0x%08x; size: %d; label: %s\n", data_partition->address, data_partition->size, data_partition->label);
      }
      float T39 = millis();
      printf("Erase size: %d Bytes\n", FLASH_ERASE_SIZE);
      ESP_ERROR_CHECK(esp_partition_erase_range(data_partition, 0, FLASH_ERASE_SIZE));


      float T3 = millis();
      Serial.print("TreadERaseTime:"); Serial.println(T3 - T39);
      int i2s_read_len = EXAMPLE_I2S_READ_LEN;
      int flash_wr_size = 0;
      size_t bytes_read, bytes_written;


      uint16_t* i2s_read_buff = (uint16_t*) calloc(i2s_read_len, sizeof(uint16_t));

      //char* i2s_read_buff = (char*) calloc(i2s_read_len, sizeof(char));


      i2s_adc_enable(I2S_NUM_0);
      while (flash_wr_size < FLASH_RECORD_SIZE) {
        //read data from I2S bus, in this case, from ADC.
        //  float T0=millis();
        //    WRITE_PERI_REG(SYSCON_SARADC_SAR1_PATT_TAB1_REG, 0x0F4F0F4F);
        //  WRITE_PERI_REG(SYSCON_SARADC_SAR1_PATT_TAB2_REG, 0x0F4F3F5F);
        // WRITE_PERI_REG(SYSCON_SARADC_SAR1_PATT_TAB1_REG, 0x0F4F3F5F);
        // WRITE_PERI_REG(SYSCON_SARADC_SAR1_PATT_TAB2_REG, 0x0F4F3F5F);
        //  WRITE_PERI_REG(SYSCON_SARADC_SAR1_PATT_TAB1_REG, 0x4F0F0000);

        // Scan multiple channels.
        //SET_PERI_REG_BITS(SYSCON_SARADC_CTRL_REG, SYSCON_SARADC_SAR1_PATT_LEN, 7, SYSCON_SARADC_SAR1_PATT_LEN_S);
        i2s_read(I2S_NUM_0, (void*) i2s_read_buff, i2s_read_len, &bytes_read, portMAX_DELAY);

        //save original data from I2S(ADC) into flash.
        esp_partition_write( data_partition, flash_wr_size, i2s_read_buff, i2s_read_len);
        // float T2=millis();
        //Serial.printf("SPIFFS partiton addr: 0x%08x; size: %d; label: %s\n", data_partition->address, data_partition->size, data_partition->label);
        Serial.print("flash_wr_size (Bytes) :");
        Serial.println(flash_wr_size);
        Serial.println(F("<-----Read Data---->"));
        flash_wr_size += i2s_read_len;
        xQueueSend(queue, &flash_wr_size, portMAX_DELAY);
        xSemaphoreTake(Semaphore, portMAX_DELAY);

        DATA_SEND = 1;
        xSemaphoreGive(Semaphore);

        ets_printf("DATA recording %u%%\n", flash_wr_size * 100 / FLASH_RECORD_SIZE);
      }
      i2s_adc_disable(I2S_NUM_0);
      free(i2s_read_buff);
      i2s_read_buff = NULL;
      float T4 = millis();
      xSemaphoreTake(Semaphore, portMAX_DELAY);
      RECORD_IN_FLASH_EN = 0;
      DATA_SEND = 1;
      xSemaphoreGive(Semaphore);
    }
  }

  float T5 = millis();
  Serial.print("TreadEND:"); Serial.println(T5);
  Serial.print("Sending Time:"); Serial.println(T5 - T4);
  Serial.print("After Erase: "); Serial.println(RECORD_IN_FLASH_EN);
  Serial.print("After Erase DATA SEND: "); Serial.println(DATA_SEND);
  vTaskDelete(NULL);

  float T4 = millis();


}


void sendData(void* parameter) {
  while (1) {
    if (!mqttConnect()) {
      mqttConnect();
    }
    else
    {
      Serial.print("Before Sending DATA SEND:"); Serial.println(DATA_SEND);
      if (DATA_SEND) {
        const esp_partition_t *data_partition ;
        data_partition = esp_partition_find_first(ESP_PARTITION_TYPE_DATA, ESP_PARTITION_SUBTYPE_DATA_SPIFFS, "spiffs");

        int flash_written_size = 8192 + FLASH_ERASE_SIZE;
        int flash_wr_size_rcv;
        int i2s_read_len = EXAMPLE_I2S_READ_LEN;
        //uint16_t* flash_read_buff = (uint16_t*) calloc(i2s_read_len, sizeof(char));
        uint8_t* flash_read_buff = (uint8_t*) calloc(i2s_read_len, sizeof(uint8_t));

        uint8_t *readPtr = (uint8_t*)ramQRead();
        //3. Read flash and replay the Data via DAC



        int packetn = 0;
        ramQSet(&flash_read_buff, PACKET_SIZE , 1);
        for (int rd_offset = 0; rd_offset < flash_written_size; rd_offset += FLASH_SECTOR_SIZE)  //rd_offset must be int in order to function properly

        {
          xQueueReceive(queue, &flash_wr_size_rcv, portMAX_DELAY);
          if (rd_offset > flash_wr_size_rcv)
          {
            delay(3);
          }
          else
          {
            //read I2S(ADC) original data from flash
            esp_partition_read(data_partition, rd_offset, flash_read_buff, FLASH_SECTOR_SIZE);
            Serial.print("rd_offset size: (Bytes) ");
            Serial.println(rd_offset);
            // Serial.print("flash_wr_size size: (Bytes) ");
            // Serial.println(flash_wr_size);

            printf("playing: %d %%\n", rd_offset * 100 / flash_written_size);





            Serial.print("TdisStart:"); Serial.println(T8);

            readPtr = flash_read_buff;
            ramQUpdateHead();
            if (readPtr != NULL)
            {
              if (mqttMid == 0) mqttMid++;
              Serial.println(F("<-----Send Data---->"));
              mqtt.publish(payload_topic, readPtr, PACKET_SIZE, mqttMid);
              //  printSensor(readPtr,PACKET_SIZE);
              ramQUpdateTail();
              mqttMid++;
            }
            packetn = packetn + 1;
            Serial.print("PacketNum:"); Serial.print(packetn);

            // float T33 = millis();
            // ESP_ERROR_CHECK(esp_partition_erase_range(data_partition, rd_offset, FLASH_SECTOR_SIZE));
            // data_partition2 +=FLASH_SECTOR_SIZE;
            //float T34 = millis();
            //Serial.print("TreadERaseTime:");Serial.println(T34-T33);
          }
        }





        free(flash_read_buff);
        Serial.println("DATA_transmission Finished");
        xSemaphoreTake(Semaphore, portMAX_DELAY);
        RECORD_IN_FLASH_EN = 1;
        DATA_SEND = 0;
        xSemaphoreGive(Semaphore);
        Serial.print("After sending Record Flash Enable: "); Serial.println(RECORD_IN_FLASH_EN);
        Serial.print("After DATA SEND: "); Serial.println(DATA_SEND);

      }
    }
  }
  float T5 = millis();
  Serial.print("TreadEND:"); Serial.println(T5);
  vTaskDelete(NULL);
}


void setup() {
  Serial.begin(115200);
  ramQSet(&buf, PACKET_SIZE, PACKET_NO);
  wifiBegin(WIFI_SSID, WIFI_PASS);
  Serial.println(F("Setup done"));

  Serial.print("Connecting wifi..");
  while (!wifiIsconnected()) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("Connected.");

  mqtt.setServer(MQTT_SERVER, MQTT_PORT);
  mqtt.connect(CLIENT_ID, MQTT_USER, MQTT_PASS, will_feed, 2, 0, disconnect_msg);
  mqtt.setBufferSize(PACKET_SIZE + 100);  // keep 100 bytes extra with maximum packet size.

  mqttConnect();
  while (!mqttConnect())
  {
    Serial.print("Retrying mqtt in 5 second..");
    delay(5000);
  }

  WiFi.setTxPower(WIFI_POWER_MINUS_1dBm);
  //  WiFi.setTxPower(WIFI_POWER_19_5dBm);
  // ESP_ERROR_CHECK(esp_wifi_set_max_tx_power(int(2));

  delay(1000);
  configure_i2s();
  queue = xQueueCreate(2, sizeof(int));
  Semaphore = xSemaphoreCreateMutex();

  xTaskCreatePinnedToCore(
    example_erase_flash, /* Function to implement the task */
    "example_i2s_adc_dac", /* Name of the task */
    1024 * 2, /* Stack size in words */
    NULL, /* Task input parameter */
    14, /* Priority of the task */
    &Task0, /* Task handle. */
    1); /* Core where the task should run */

  xTaskCreatePinnedToCore(
    sendData, /* Function to implement the task */
    "sendData", /* Name of the task */
    1024 * 2, /* Stack size in words */
    NULL, /* Task input parameter */
    14, /* Priority of the task */
    &Task1, /* Task handle. */
    0); /* Core where the task should run */


  //example_erase_flash();

}




void loop() {

  // esp_log_level_set("I2S", ESP_LOG_INFO);
  //xTaskCreate(example_i2s_adc_dac, "example_i2s_adc_dac", 1024 * 2, NULL, 6, NULL);
  mqtt.loop();

  delay(03);
}


void printSensor(uint8_t *buff, int length)
{
  Serial.print(" Buff: ");
  for (uint16_t i = 0; i < length; i++)
  {
    Serial.print(buff[i]);
    Serial.print(" ");
  }
  Serial.println("");
}
