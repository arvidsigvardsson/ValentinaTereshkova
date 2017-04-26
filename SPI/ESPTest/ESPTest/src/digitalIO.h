/*
 * digitalIO.h
 *
 * Created: 2015-06-09 13:14:37
 * Author: Ulrik Eklund
 */ 


#ifndef DIGITALIO_H_
#define DIGITALIO_H_

/*
 * The following values are already defined by Atmel in the file compiler.h
 * They are not changed to avoid any conflicts
 * #define LOW       0
 * #define HIGH      1
 */

typedef enum  {INPUT, INPUT_PULLUP, OUTPUT} mode_definition;	/* Three values to be consistent with Arduino API, see http://www.arduino.cc/en/Reference/PinMode */

void pinMode(int pinNumber, mode_definition mode); /* You only have to program a function that cares about OUTPUT, and does nothing for the other values */

void digitalWrite(int pinNumber, int value);

#endif /* DIGITALIO_H_ */