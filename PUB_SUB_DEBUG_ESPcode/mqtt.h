#ifndef _ESP_MQTT_H_
#define _ESP_MQTT_H_
#include <esp_wifi.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include  "param.h"


void wifiBegin(String ssid, String pass);
bool mqttIsConnected();
bool wifiIsconnected();
bool mqttConnect();

extern PubSubClient mqtt;
extern char *payload_topic;
extern char *will_feed;
extern const char disconnect_msg[];

#endif //_ESP_MQTT_H_
