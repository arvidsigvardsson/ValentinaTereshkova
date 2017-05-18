#include <Wire.h>

uint8_t rx_buff[3];
int8_t send_data[5];
int8_t byteArray[8];
int8_t twi_state = 0,request_state = 0;
int8_t led1[5];
int8_t led2[5];
int8_t strumpa[5];
int8_t kub[5];
int8_t glas[5];



#define SLAVE_ADR 0x03

void setup() {
  Wire.begin(SLAVE_ADR);
  Wire.onRequest(requestEvent);
  Wire.onReceive(recieveEvent);
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial.println("Starting up twi");
}

void loop() {
  
  while(Serial1.available()) {
    Serial1.readBytes(byteArray, 5);
    //Serial.println((byteArray[1] << 8) | (byteArray[2] << 0));
    //Serial.println((byteArray[3] << 8) | (byteArray[4] << 0));
    
    switch(byteArray[0]) {
      case 0x50:  //lysdiod 1 positon
        led1[0] = 0x50; 
        led1[1] = byteArray[1];
        led1[2] = byteArray[2];
        led1[3] = byteArray[3];
        led1[4] = byteArray[4];
        //Serial.println("led1");
      break;
      case 0x51: //lysdiod 2 position
        led2[0] = 0x51;
        led2[1] = byteArray[1];
        led2[2] = byteArray[2];
        led2[3] = byteArray[3];
        led2[4] = byteArray[4];
        //Serial.println("led2");
      break;
      case 0x52:  //strumpa position
        strumpa[0] = 0x52;
        strumpa[1] = byteArray[1];
        strumpa[2] = byteArray[2];
        strumpa[3] = byteArray[3];
        strumpa[4] = byteArray[4];
        //Serial.println("strumpa");
      break;
      case 0x53:  //kubens position
        kub[0] = 0x53;
        kub[1] = byteArray[1];
        kub[2] = byteArray[2];
        kub[3] = byteArray[3];
        kub[4] = byteArray[4];
        //Serial.println("kub");
      break;
      case 0x54:  //glasets position
        kub[0] = 0x54;
        glas[1] = byteArray[1];
        glas[2] = byteArray[2];
        glas[3] = byteArray[3];
        glas[4] = byteArray[4];
        //Serial.println("glas");
      break;
    }
    Serial.println(".");
  }
}

//skicka datan som har blivit förberedd
void requestEvent(){
  if(send_data[0] != 0){
    Wire.write(send_data, 5);
    for(int n = 0; n < 5; n++) {
      Serial.println(send_data[n]);
    }
  }
}

//ta emot ett kommando
void recieveEvent(int TURNDOWNFORWHAT){
  while(Wire.available()){
    twi_state = Wire.read();
    rx_buff[0] = twi_state;
  }
  Serial.print("Kommando: ");
  Serial.println(rx_buff[0], HEX);
  switch(rx_buff[0]){
    case 0x00:
      send_data[0] = 0;
    break;
    case 0x50:  //efterfrågar lysdiod 1 positon
      for(int n = 0; n < 5; n++) {
        send_data[n] = led1[n];
      }
      //send_data[0] = 0x50;
      //send_data[1] = 0;
      //send_data[2] = 200;
      //send_data[3] = 0;
      //send_data[4] = 200;
    break;
    case 0x51: //efterfrågar lysdiod 2 position
      for(int n = 0; n < 5; n++) {
        send_data[n] = led2[n];
      }
      //send_data[0] = 0x51;
      //send_data[1] = 0;
      //send_data[2] = 150;
      //send_data[3] = 0;
      //send_data[4] = 150;
    break;
    case 0x52:  //efterfrågar strumpa position
      /*for(int n = 0; n < 5; n++) {
        send_data[n] = strumpa[n];
      }*/

      send_data[0] = 0x52;
      send_data[1] = 0;
      send_data[2] = 100;
      send_data[3] = 0;
      send_data[4] = 100;
    break;
    case 0x53:  //efterfrågar kubens position
      /*for(int n = 0; n < 5; n++) {
        send_data[n] = kub[n];
      }*/
      send_data[0] = 0x53;
      send_data[1] = 0;
      send_data[2] = 50;
      send_data[3] = 0;
      send_data[4] = 50;
    break;
    case 0x54:  //efterfrågar glasets position
      /*for(int n = 0; n < 5; n++) {
        send_data[n] = glas[n];
      }*/
      send_data[0] = 0x54;
      send_data[1] = 0;
      send_data[2] = 10;
      send_data[3] = 0;
      send_data[4] = 10;
    break;
  }
  
}


