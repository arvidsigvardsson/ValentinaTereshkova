#include <Wire.h>


uint8_t rx_buff[3];
uint8_t send_data[5];
uint8_t byteArray[8];
uint8_t twi_state = 0,request_state = 0;
uint8_t led1[5];
uint8_t led2[5];
uint8_t strumpa[5];
uint8_t kub[5];
uint8_t glas[5];



#define SLAVE_ADR 0x03

void setup() {
  Wire.begin(SLAVE_ADR);
  Wire.onRequest(requestEvent);
  Wire.onReceive(recieveEvent);
  Serial.begin(115200);
  Serial1.begin(9600);
  Serial.println("Starting up twi");
}

void loop() {

  while(Serial1.available()) {
    Serial1.readBytes(byteArray, 5);
    //Serial.println((byteArray[1] << 8) | (byteArray[2] << 0));
    //Serial.println((byteArray[3] << 8) | (byteArray[4] << 0));
    Serial.println("--------------");
    switch(byteArray[0]) {
      case 0x50:  //lysdiod 1 positon
        led1[0] = 0x33; 
        led1[1] = byteArray[1];
        led1[2] = byteArray[2];
        led1[3] = byteArray[3];
        led1[4] = byteArray[4];
        Serial.println("led1");
      break;
      case 0x51: //lysdiod 2 position
        led2[0] = 0x34;
        led2[1] = byteArray[1];
        led2[2] = byteArray[2];
        led2[3] = byteArray[3];
        led2[4] = byteArray[4];
        Serial.println("led2");
      break;
      case 0x52:  //strumpa position
        strumpa[0] = 0x35;
        strumpa[1] = byteArray[1];
        strumpa[2] = byteArray[2];
        strumpa[3] = byteArray[3];
        strumpa[4] = byteArray[4];
        Serial.println("strumpa");
      break;
      case 0x53:  //kubens position
        kub[0] = 0x36;
        kub[1] = byteArray[1];
        kub[2] = byteArray[2];
        kub[3] = byteArray[3];
        kub[4] = byteArray[4];
        Serial.println("kub");
      break;
      case 0x54:  //glasets position
        kub[0] = 0x37;
        glas[1] = byteArray[1];
        glas[2] = byteArray[2];
        glas[3] = byteArray[3];
        glas[4] = byteArray[4];
        Serial.println("glas");
      break;
    }
  }
}

//skicka datan som har blivit förberedd
void requestEvent(){
  Wire.write(send_data, 5);s
}

//ta emot ett kommando
void recieveEvent(int TURNDOWNFORWHAT){
  Serial.println("kommando");
  int i = 0;
  while(Wire.available()){
    twi_state = Wire.read();
    rx_buff[i] = twi_state;
    i++;
  }
  switch(rx_buff[0]){
    case 0x50:  //efterfrågar lysdiod 1 positon
      for(int n = 0; n < 5; n++) {
        send_data[n] = led1[n];
      }
    break;
    case 0x51: //efterfrågar lysdiod 2 position
      for(int n = 0; n < 5; n++) {
        send_data[n] = led2[n];
      }
    break;
    case 0x52:  //efterfrågar strumpa position
      for(int n = 0; n < 5; n++) {
        send_data[n] = strumpa[n];
      }
    break;
    case 0x53:  //efterfrågar kubens position
      for(int n = 0; n < 5; n++) {
        send_data[n] = kub[n];
      }
    break;
    case 0x54:  //efterfrågar glasets position
      for(int n = 0; n < 5; n++) {
        send_data[n] = glas[n];
      }
    break;
  }
  
}


