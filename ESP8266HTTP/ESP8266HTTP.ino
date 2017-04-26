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

SoftwareSerial rxtx(12,14);

/*
String readResponse(String payload){
  //Serial.println(payload);
//  JsonObject& root = jsonBuffer.parseObject(payload);
  xcor = root["coordinate"]["x"];
  ycor = root["coordinate"]["y"];
  Serial.println(xcor);
  String str1 = xcor + "-" + ycor;
  return str1;
}*/

void setup() {
  pinMode(CS, OUTPUT);
  Serial.begin(115200);
  rxtx.begin(9600);
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

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
}

void loop() {
  
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin("http://192.168.20.145:5000/srv/coordinate/getlatest");
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

      while(xcors.length()<3){
        xcors = "0" + xcors;
      }
      while(ycors.length()<3){
        ycors = "0" + ycors;
      }
      
      //Serial.println(xcor);
      str1 = xcors + "-" + ycors;
      Serial.println(str1);    

    }
  }

    
  

  
  
  if(rxtx.available()) {
    char c = rxtx.read();
    mess += c;
    Serial.println(mess);
  }
  
  if (mess.indexOf("req")>=0) {
    String data = xcors + "-" + ycors;
    
    Serial.println("rxtx");
    rxtx.print(data);
    
    mess = "";
    
  }
  /*
  if(rxtx.available()) {
    char c = rxtx.read();
    mess += c;
    //Serial.println(mess+"rxtx");
  }
  if (mess.indexOf("ack")>=0) {
   
    rxtx.flush();
    
    mess = "";
    
  }*/
   delay(10);
   
  
  

}


