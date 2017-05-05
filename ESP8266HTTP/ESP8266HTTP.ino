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
      
      //Serial.println(xcor);
      str1 = xcors + ycors + "0000" + "0000";
      Serial.println(str1);    

    }
  }
  rxtx.print(str1);
  
   delay(1000); 

}


