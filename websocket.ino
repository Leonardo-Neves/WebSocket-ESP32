#include <ArduinoWebsockets.h>
#include <WiFi.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

#include <iostream>
#include <cstdio>
#include <string>
#include <sstream>

const char* ssid = "HostspotSocketIOIMUBNO055"; //Enter SSID
const char* password = "7aecf2d1f18296861f73d63ccb2e1bbb"; //Enter Password
const char* websockets_server_host = "192.168.137.1"; //Enter server adress
const uint16_t websockets_server_port = 5000; // Enter server port

using namespace websockets;

WebsocketsClient client;
Adafruit_BNO055 bno = Adafruit_BNO055(55);

void setup() {
  Serial.begin(115200);
  
  if(!bno.begin())
  {
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  WiFi.begin(ssid, password);

  for(int i = 0; i < 10 && WiFi.status() != WL_CONNECTED; i++) {
    Serial.print(".");
    delay(1000);
  }

  if(WiFi.status() != WL_CONNECTED) {
    Serial.println("No Wifi!");
    return;
  }

  Serial.println("Connected to Wifi, Connecting to server.");
  bool connected = client.connect(websockets_server_host, websockets_server_port, "/");

  if(connected) {
    Serial.println("Connecetd!");
    client.send("Hello Server");
  } else {
    Serial.println("Not Connected!");
  }
  
  // client.onMessage([&](WebsocketsMessage message) {
  //   Serial.print("Got Message: ");
  //   Serial.println(message.data());
  // });

  bno.setExtCrystalUse(true);
}

void loop() {
    
  if(client.available()) {
    client.poll();
  }

  sensors_event_t orientationData;
  bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER); // Yaw, pitt, row

  std::string orientation_x = std::to_string(orientationData.orientation.x);
  std::string orientation_y = std::to_string(orientationData.orientation.y);
  std::string orientation_z = std::to_string(orientationData.orientation.z);

  std::string concatenated = orientation_x + " " + orientation_y + " " + orientation_z;

  const char* char_array = concatenated.c_str();

  client.send(char_array);
}