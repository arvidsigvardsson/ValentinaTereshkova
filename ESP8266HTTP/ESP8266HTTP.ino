#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <Wire.h>



#define CS 14
#define SLAVE_ADR 0x03
<<<<<<< HEAD
const char* ssid     = "vetinte";
const char* password = "redbull123";
const char* ssid     = "ComHem<F580A8>";
const char* password = "4673a335";

String payload = "";
HTTPClient http;
int httpCode;
byte byteArray[8];
byte sockArray[5];
byte cubeArray[5];
byte glassArray[5];
byte led1Array[5];
byte led2Array[5];

uint8_t newState = 0;
uint8_t state = 0;

SoftwareSerial rxtx(12,14);

void setup() {
  pinMode(CS, OUTPUT);
  pinMode(2, OUTPUT);
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
  digitalWrite(2, LOW);
  Serial.println("");
  Serial.println("WiFi connected ");  
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
      digitalWrite(2, HIGH);
    break;
    case 1:
      http.begin("http://192.168.20.133:5000/srv/objectlist");
      http.begin("http://192.168.20.12:5000/srv/objectlist");
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
        sockArray[1] = (byte) (sockx >> 8);
        sockArray[2] = (byte) (sockx);
        sockArray[3] = (byte) (socky >> 8);
        sockArray[4] = (byte) (socky);
        rxtx.write(sockArray, 5);
        delay(1);
        cubeArray[0] = 0x53;
        cubeArray[1] = (byte) (cubex >> 8);
        cubeArray[2] = (byte) (cubex);
        cubeArray[3] = (byte) (cubey >> 8);
        cubeArray[4] = (byte) (cubey);
        rxtx.write(cubeArray, 5);
        delay(1);
        glassArray[0] = 0x54;
        glassArray[1] = (byte) (glassx >> 8);
        glassArray[2] = (byte) (glassx);
        glassArray[3] = (byte) (glassy >> 8);
        glassArray[4] = (byte) (glassy);
        rxtx.write(glassArray, 5);
        delay(1);
        newState = 2;
        Serial.println("sent obj");
        digitalWrite(2, LOW);
      }
      else {
        newState = 1;
      }
    break;
    case 2:  
      http.begin("http://192.168.20.133:5000/srv/coordinate/getlatest");
      http.begin("http://192.168.20.12:5000/srv/coordinate/getlatest");
      httpCode = http.GET();
  
      if(httpCode > 0){
        payload = http.getString();
        StaticJsonBuffer<512> jsonBuffer;
        JsonObject& root = jsonBuffer.parseObject(payload);
        int16_t x_1 = (int16_t) int(root["coordinate"]["x1"]);
        int16_t y_1 = (int16_t) int(root["coordinate"]["y1"]);
        int16_t x_2 = (int16_t) int(root["coordinate"]["x2"]);
        int16_t y_2 = (int16_t) int(root["coordinate"]["y2"]);
        led1Array[0] = 0x50;
        led1Array[1] = (byte) (x_1 >> 8);
        led1Array[2] = (byte) (x_1);
        led1Array[3] = (byte) (y_1 >> 8);
        led1Array[4] = (byte) (y_1);
        rxtx.write(led1Array, 5);
        delay(1);
        led2Array[0] = 0x51;
        led2Array[1] = (byte) (x_2 >> 8);
        led2Array[2] = (byte) (x_2);
        led2Array[3] = (byte) (y_2 >> 8);
        led2Array[4] = (byte) (y_2);
        rxtx.write(led2Array, 5);
        Serial.println("sent coord");
        digitalWrite(2, LOW);
      }
      newState = 2;
    break;
  }
  state = newState;
  delay(200);

}
