#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>

#define CS 14
const char* ssid     = "VHAM";
const char* password = "MAHVMAHV";
String mess = "";
String payload="";
int xcor = 0;
int ycor = 0;
String str1 = "";
String xcors = "";
String ycors = "";
uint16_t x_1 = 200;
uint16_t y_1 = 300;
uint16_t x_2 = 400;
uint16_t y_2 = 500;

uint8_t byteArray[8];

SoftwareSerial rxtx(12,14);

void setup() {
  pinMode(CS, OUTPUT);
  Serial.begin(115200);
  rxtx.begin(115200);
  delay(10);

  // Connect to WiFi

  Serial.println();
  Serial.println();

      byteArray[0] = x_1 & 0xFF00;
      byteArray[1] = x_1 & 0x00FF;
      byteArray[2] = y_1 & 0xFF00;
      byteArray[3] = y_1 & 0x00FF;
      byteArray[4] = x_2 & 0xFF00;
      byteArray[5] = x_2 & 0x00FF;
      byteArray[6] = y_2 & 0xFF00;
      byteArray[7] = y_2 & 0x00FF;
  
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
  
  /*if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin("http://192.168.20.133:5000/srv/coordinate/getlatest");
    int httpCode = http.GET();

    if(httpCode > 0){
      payload = http.getString();
      StaticJsonBuffer<512> jsonBuffer;
      //String response = readResponse(payload);
      //Serial.println(response);
      JsonObject& root = jsonBuffer.parseObject(payload);
      xcor = root["coordinate"]["x"];
      ycor = root["coordinate"]["y"];
      xcors = String(xcor);
      ycors = String(ycor);
      /*x_1 = (uint16_t) int(xcor);
      y_1 = (uint16_t) int(ycor);
      if(x_1 < 0) {
        x_1 = 0;
      }
      if(y_1 < 0) {
        y_1 = 0;
      }*/
      /*x_1 = 200;
      y_1 = 200;
      x_2 = 0;
      y_2 = 0;

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
      uint8_t x1_H = x_1 & 0xFF00;
      uint8_t x1_L = x_1 & 0x00FF;
      uint8_t y1_H = y_1 & 0xFF00;
      uint8_t y1_L = y_1 & 0x00FF;
      uint8_t x2_H = x_2 & 0xFF00;
      uint8_t x2_L = x_2 & 0x00FF;
      uint8_t y2_H = y_2 & 0xFF00;
      uint8_t y2_L = y_2 & 0x00FF;
      uint8_t byteArray[] = {x1_H, x1_L, y1_H, y1_L, x2_H, x2_L, y2_H, y2_L};
      //Serial.println(xcor);
      str1 = xcors + ycors + "0000" + "0000";
      Serial.println(str1);    

    }
    rxtx.print(str1);
  }
  
   delay(500); */
   while(rxtx.available()) {
    char buf[8];
    rxtx.readBytes(buf, 8);
    if(String(buf) == "request!") {
      rxtx.write(byteArray, 8);
    }
    else if(String(buf) == "okx") {
      Serial.println("Success!");
    }
    Serial.println(String(buf));
   }

}


