
#include "mqtt.h"
const char disconnect_msg[] = "{\"status\" : 0}";
const char connected_msg[]  = "{\"status\" : 1}";
char *will_feed = CLIENT_ID"/last_will";
char *payload_topic = CLIENT_ID"/data";

/******* for WIFI CLIENT*********/
WiFiClient espClient;

/******* for pubsub client ******/
PubSubClient mqtt(espClient);


void wifiBegin(String ssid, String pass)
{
  if(ssid.length() && pass.length())
  {
#if defined(ESP32)
  WiFi.begin(ssid.c_str(),pass.c_str());
#else
  WiFi.begin(ssid, pass);
#endif
  }
  else
  {
    WiFi.begin();
  }
  debugSerial.println("Wifi Setup Done");
}

bool wifiIsconnected()
{
  return (WiFi.status() == WL_CONNECTED);
}


bool mqttConnect()
{
  static int mqttRetry = 4;
  
  if(wifiIsconnected())
  {
    debugSerial.println(F("MQTT Connecting.."));
    if(mqttRetry > 2)
    {
      mqtt.disconnect();
      mqttRetry = 0;
      delay(1000);
    }
    mqtt.connect(CLIENT_ID,MQTT_USER,MQTT_PASS,will_feed,2,0,disconnect_msg);
    delay(1000);
    bool mqttState = mqttIsConnected();
    if (mqttState)
    {
//      lastWill.publish(connected_msg);
      debugSerial.println(F("MQTT Connected"));
      return true;
    }
    else
    {
      mqttRetry++;
    }
  }
  return false;
}

bool mqttIsConnected()
{
  if(mqtt.state() == MQTT_CONNECTED)
  {
    return true;
  }
  else
  {
    return false;
  }
}
