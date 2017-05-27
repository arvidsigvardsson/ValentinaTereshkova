#include <Wire.h>

uint8_t rx_buff[3];
byte send_data[5];
byte byteArray[8];
int8_t twi_state = 0,request_state = 0;
byte led1[5];
byte led2[5];
byte sock[5];
byte cube[5];
byte glass[5];



#define SLAVE_ADR 0x03 //this slaves address

/*
Initialize the system by starting various communications
*/
void setup() {
  Wire.begin(SLAVE_ADR);
  Wire.onRequest(requestEvent);
  Wire.onReceive(recieveEvent);
  Serial.begin(115200);
  Serial1.begin(115200);
}

/*
Main part of the program, acts as a gateway and retrieves data from the ESP
*/
void loop() {
  
  while(Serial1.available()) {
    Serial1.readBytes(byteArray, 5);
    switch(byteArray[0]) {
      case 0x50:  //LED 1 positon
        led1[0] = 0x50; 
        led1[1] = byteArray[1];
        led1[2] = byteArray[2];
        led1[3] = byteArray[3];
        led1[4] = byteArray[4];
      break;
      case 0x51: //LED 2 position
        led2[0] = 0x51;
        led2[1] = byteArray[1];
        led2[2] = byteArray[2];
        led2[3] = byteArray[3];
        led2[4] = byteArray[4];
      break;
      case 0x52:  //sock position
        sock[0] = 0x52;
        sock[1] = byteArray[1];
        sock[2] = byteArray[2];
        sock[3] = byteArray[3];
        sock[4] = byteArray[4];
      break;
      case 0x53:  //cube position
        cube[0] = 0x53;
        cube[1] = byteArray[1];
        cube[2] = byteArray[2];
        cube[3] = byteArray[3];
        cube[4] = byteArray[4];
      break;
      case 0x54:  //glass position
        glass[0] = 0x54;
        glass[1] = byteArray[1];
        glass[2] = byteArray[2];
        glass[3] = byteArray[3];
        glass[4] = byteArray[4];
      break;
    }
  }
}

/*
 * send the data that has been prepared for transmission
 */
void requestEvent(){
  if(send_data[0] != 0){ //if the ID is 0 it was a probe, do nothing
    Wire.write(send_data, 5);
  }
}

/*
 * recieve a request for data
 * params: TURNDOWNFORWHAT
 * TURNDOWNFORWHAT: number of bytes reveived
*/
void recieveEvent(int TURNDOWNFORWHAT){
  while(Wire.available()){
    twi_state = Wire.read();
    rx_buff[0] = twi_state;
  }
  switch(rx_buff[0]){
    case 0x00:
      send_data[0] = 0;
    break;
    case 0x50: //requests the position of LED 1
      for(int n = 0; n < 5; n++) {
        send_data[n] = led1[n];
      }
    break;
    case 0x51: //requests the position of LED 2
      for(int n = 0; n < 5; n++) {
        send_data[n] = led2[n];
      }
    break;
    case 0x52: //requests the position of the sock
      for(int n = 0; n < 5; n++) {
        send_data[n] = sock[n];
      }
    break;
    case 0x53: //requests the position of the cube
      for(int n = 0; n < 5; n++) {
        send_data[n] = cube[n];
      }
    break;
    case 0x54: //requests the position of the glass
      for(int n = 0; n < 5; n++) {
        send_data[n] = glass[n];
      }
    break;
    case 0x55: //Unused
      send_data[0] = 0x55;
      send_data[1] = 0;
      send_data[2] = 0;
      send_data[3] = 0;
      send_data[4] = 0;
    break;
  }
  
}


