/*
 * adcFunctions.h
 *
 * Created: 2015-06-16 08:59:27
 *  Author: To Be Decided
 */ 


#ifndef ADCFUNCTIONS_H_
#define ADCFUNCTIONS_H_

#define ADC_BASE_ADDRESS 0x400C0000U

#include <inttypes.h>

int analogInit(int pinNumber);
uint32_t analogRead(int pinNumber);

#endif /* ADCFUNCTIONS_H_ */