#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <Wire.h>



#define CS 14
#define SLAVE_ADR 0x03
const char* ssid     = "VHAM";
const char* password = "MAHVMAHV";
String mess = "";
String payload="";
int xcor = 0;
int ycor = 0;
int xcor2 = 0;
int ycor2 = 0;
String str1 = "";
String xcors = "";
String ycors = "";
uint16_t x_1 = 200;
uint16_t y_1 = 300;
uint16_t x_2 = 400;
uint16_t y_2 = 500;
uint8_t x1_H = 0;
uint8_t x1_L = 0;
uint8_t y1_H = 0;
uint8_t y1_L = 0;
uint8_t x2_H = 10;
uint8_t x2_L = 20;
uint8_t y2_H = 15;
uint8_t y2_L = 177;

uint8_t byteArray[8];

SoftwareSerial rxtx(12,14);

void setup() {
  pinMode(CS, OUTPUT);
  Serial.begin(115200);
  rxtx.begin(9600);
  delay(10);

  // Connect to WiFi

  Serial.println();
  Serial.println();

  
  //Serial.print("Connecting to ");
  //Serial.println(ssid);
  
  /*WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());*/
  
}

void loop() {
  
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin("http://192.168.20.133:5000/srv/coordinate/getlatest");
    int httpCode = http.GET();

    if(httpCode > 0){
      payload = http.getString();
      StaticJsonBuffer<512> jsonBuffer;
      //String response = readResponse(payload);
      //Serial.println(response);
      JsonObject& root = jsonBuffer.parseObject(payload);
      xcor = root["coordinate"]["x1"];
      ycor = root["coordinate"]["y1"];
<<<<<<< HEAD
=======
      xcor2 = root["coordinate"]["x2"];
      ycor2 = root["coordinate"]["y2"];
>>>>>>> Lagt till bilder, och DUE-Twi kod
      xcors = String(xcor);
      ycors = String(ycor);
      x_1 = (uint16_t) int(xcor);
      y_1 = (uint16_t) int(ycor);
      x_2 = (uint16_t) int(xcor2);
      y_2 = (uint16_t) int(ycor2);
      if(x_1 < 0) {
        x_1 = 0;
      }
      if(y_1 < 0) {
        y_1 = 0;
      }

      x1_H = (uint8_t) (x_1 >> 8);
      x1_L = (uint8_t) (x_1);
      y1_H = (uint8_t) (y_1 >> 8);
      y1_L = (uint8_t) (y_1);
      x2_H = (uint8_t) (x_2 >> 8);
      x2_L = (uint8_t) (x_2);
      y2_H = (uint8_t) (y_2 >> 8);
      y2_L = (uint8_t) (y_2);


      //Padds xcors with 0s to contain 4characters
      while(xcors.length()<4){
        
        if(xcors.charAt(0)=='-'){
          xcors = xcors.substring(1);
          xcors = "0" + xcors;
          xcors = "-" + xcors;          
        }else{
          xcors = "0" + xcors;
        }
        
      }
      //Padds ycors with 0s to contain 4characters
      while(ycors.length()<4){
        
         if(ycors.charAt(0)=='-'){
          ycors = ycors.substring(1);
          ycors = "0" + ycors;
          ycors = "-" + ycors;          
        }else{
          ycors = "0" + ycors;
        }
      }
      str1 = xcors + '-' + ycors;

    }
    byteArray[0] = x1_H;
    byteArray[1] = x1_L;
    byteArray[2] = y1_H;
    byteArray[3] = y1_L;
    byteArray[4] = x2_H;
    byteArray[5] = x2_L;
    byteArray[6] = y2_H;
    byteArray[7] = y2_L;
    rxtx.write(byteArray, 8);
  }
  
<<<<<<< HEAD
   delay(100                            );
=======
   delay(100);
>>>>>>> Lagt till bilder, och DUE-Twi kod
   /*while(rxtx.available()) {
    char buf[8];
    rxtx.readBytes(buf, 8);
    if(String(buf) == "request!") {
      rxtx.write(byteArray, 8);
    }
    else if(String(buf) == "okx") {
      Serial.println("Success!");
    }
    Serial.println(String(buf));
   }*/

}
