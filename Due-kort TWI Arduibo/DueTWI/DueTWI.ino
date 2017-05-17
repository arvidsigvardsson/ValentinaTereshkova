#include <Wire.h>


uint8_t rx_buff[3];
uint8_t send_data[8];
uint8_t byteArray[8];
uint8_t twi_state = 0,request_state = 0;
uint8_t lowerArray[5];
uint8_t upperArray[5];



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
    Serial1.readBytes(byteArray, 8);
    Serial.println((byteArray[0] << 8) | (byteArray[1] << 0));
    Serial.println((byteArray[2] << 8) | (byteArray[3] << 0));
    Serial.println((byteArray[4] << 8) | (byteArray[5] << 0));
    Serial.println((byteArray[6] << 8) | (byteArray[7] << 0));
    Serial.println("--------------");    
    }

    
    //for(int i=0; i<sizeof(byteArray) - 1; i++){
    //  Serial.println(byteArray[i]);
    //}
    //uint8_t data = (uint8_t) Serial1.read();
    //Serial.println(data);
  }

  //uint16_t data = ((byteArray[0] << 8) | (byteArray[1] << 0));
//  for(int i=0; i< sizeof(byteArray) - 1; i++){
//    send_data[i] = byteArray[i];
//  }
//  Serial.println(send_data[1]);
//  Serial.println(send_data[3]);
//  delay(100);
}

void requestEvent(){
  switch(rx_buff[0]){
    case 0x50:
    Wire.write(send_data, 5);
    break;
    case 0x51:
    Wire.write(send_data, 5);
    break;
  }
}

void recieveEvent(int TURNDOWNFORWHAT){
  int i = 0;
  while(Wire.available()){
    twi_state = Wire.read();
    rx_buff[i] = twi_state;
    i++;
  }
  switch(rx_buff[0]){
    case 0x50:
      lowerArray[0] = 0x33;
      lowerArray[1] = byteArray[0]
      lowerArray[2] = byteArray[1];
      lowerArray[3] = byteArray[2];
      lowerArray[4] = byteArray[3];
    break;
    case 0x51:
     upperArray[0] = 0x34;
     upperArray[1] = byteArray[4];
     upperArray[2] = byteArray[5];
     upperArray[3] = byteArray[6];
     upperArray[4] = byteArray[7];
    break;
  }
  
}


