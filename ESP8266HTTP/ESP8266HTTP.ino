#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <Wire.h>



#define CS 14
#define SLAVE_ADR 0x03
const char* ssid     = "VHAM";
const char* password = "MAHVMAHV";

String payload = "";
HTTPClient http;
int httpCode;
int8_t byteArray[8];
int8_t sockArray[5];
int8_t cubeArray[5];
int8_t glassArray[5];
int8_t led1Array[5];
int8_t led2Array[5];

uint8_t newState = 0;
uint8_t state = 0;


SoftwareSerial rxtx(12,14);

void setup() {
  pinMode(CS, OUTPUT);
  Serial.begin(115200);
  rxtx.begin(115200);
  delay(10);

  // Connect to WiFi

  Serial.println();
  Serial.println();

  
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  state = 1;  //ansluten
  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
}

void loop() {

  if(WiFi.status() != WL_CONNECTED) { //we have disconnected from the network
    state = 0;
  }

  switch(state) {
    case 0: //reset the program in case we disconnect
      newState = 2;
    break;
    case 1:
      http.begin("http://192.168.20.133:5000/srv/objectlist");
      httpCode = http.GET();

      if(httpCode > 0){
        payload = http.getString();
        StaticJsonBuffer<512> jsonBuffer;
        JsonObject& root = jsonBuffer.parseObject(payload);
        int16_t sockx = (int16_t) int(root["sock"][0]["x"]);
        int16_t socky = (int16_t) int(root["sock"][0]["y"]);
        int16_t cubex = (int16_t) int(root["cube"][0]["x"]);
        int16_t cubey = (int16_t) int(root["cube"][0]["y"]);
        int16_t glassx = (int16_t) int(root["glas"][0]["x"]);
        int16_t glassy = (int16_t) int(root["glas"][0]["y"]);
        sockArray[0] = 0x52;
        delay(1);
        sockArray[1] = (int8_t) (sockx >> 8);
        sockArray[2] = (int8_t) (sockx);
        sockArray[3] = (int8_t) (socky >> 8);
        sockArray[4] = (int8_t) (socky);
        rxtx.write(sockArray, 5);
        delay(1);
        cubeArray[0] = 0x53;
        cubeArray[1] = (int8_t) (cubex >> 8);
        cubeArray[2] = (int8_t) (cubex);
        cubeArray[3] = (int8_t) (cubey >> 8);
        cubeArray[4] = (int8_t) (cubey);
        rxtx.write(cubeArray, 5);
        delay(1);
        glassArray[0] = 0x54;
        glassArray[1] = (int8_t) (glassx >> 8);
        glassArray[2] = (int8_t) (glassx);
        glassArray[3] = (int8_t) (glassy >> 8);
        glassArray[4] = (int8_t) (glassy);
        rxtx.write(glassArray, 5);
        newState = 2;
        Serial.println("sent obj");
      }
      else {
        newState = 1;
      }
    break;
    case 2:  
      http.begin("http://192.168.20.133:5000/srv/coordinate/getlatest");
      httpCode = http.GET();
  
      if(httpCode > 0){
        payload = http.getString();
        StaticJsonBuffer<512> jsonBuffer;
        JsonObject& root = jsonBuffer.parseObject(payload);
        int16_t x_1 = (int16_t) int(root["coordinate"]["x1"]);
        int16_t y_1 = (int16_t) int(root["coordinate"]["y1"]);
        int16_t x_2 = (int16_t) int(root["coordinate"]["x2"]);
        int16_t y_2 = (int16_t) int(root["coordinate"]["y2"]);
        if(x_1 < 0) {
          x_1 = 0;
        }
        if(y_1 < 0) {
          y_1 = 0;
        }
        if(x_2 < 0) {
          x_1 = 0;
        }
        if(y_2 < 0) {
          y_1 = 0;
        }
        led1Array[0] = 0x50;
        led1Array[1] = (int8_t) (x_1 >> 8);
        led1Array[2] = (int8_t) (x_1);
        led1Array[3] = (int8_t) (y_1 >> 8);
        led1Array[4] = (int8_t) (y_1);
        rxtx.write(led1Array, 5);
        delay(1);
        led2Array[0] = 0x51;
        led2Array[1] = (int8_t) (x_2 >> 8);
        led2Array[2] = (int8_t) (x_2);
        led2Array[3] = (int8_t) (y_2 >> 8);
        led2Array[4] = (int8_t) (y_2);
        rxtx.write(led2Array, 5);
        Serial.println("sent coord");
      }
      newState = 2;
    break;
  }
  state = newState;
  delay(400);

}
