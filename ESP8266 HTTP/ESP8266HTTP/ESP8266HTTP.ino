#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>


const char* ssid     = "FESTMEDHEST";
const char* password = "Hellbe920226";


void setup() {
  Serial.begin(115200);
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

    http.begin("http://192.168.0.3:5000/srv/coordinate/getlatest");
    int httpCode = http.GET();

    if(httpCode > 0){
      String payload = http.getString();
      Serial.println(payload);
      
    }

    delay(30000);
  }

}
