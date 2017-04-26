/*
 * adcFunctions.c
 *
 * Created: 2015-06-16 09:00:18
 *  Author: To Be Decided
 */ 

#include <inttypes.h>
#include <asf.h>
#include "adcFunctions.h"
#include "DelayFunctions.h"

uint8_t pinmapping[] = {ADC_CHANNEL_7, ADC_CHANNEL_6, ADC_CHANNEL_5, ADC_CHANNEL_4, ADC_CHANNEL_3, ADC_CHANNEL_2, ADC_CHANNEL_1, ADC_CHANNEL_0};

int analogInit(int pinNumber)
{
	
	/* 
	 * The pin number is the analog input pin on the DUe board, see http://www.arduino.cc/en/Hacking/PinMappingSAM3X
	 * Obviously it starts at analog 0 which is equivalent to the analog input on PA16
	 * so you need to figure out which AD channel this corresponds to
	 *
	 * See code example http://asf.atmel.com/docs/latest/sam.drivers.adc.adc_example.arduino_due_x/html/sam_adc_quickstart.html
	 * It is assumed that the AD-converter is using 12 bits
	 */
	
	pmc_enable_periph_clk(ID_ADC);	/* power the clock for the ADC with pmc_enable_periph_clk(ID_ADC) */
	adc_init(ADC, sysclk_get_main_hz(), 1000000, 8);
	adc_configure_timing(ADC, 0, ADC_SETTLING_TIME_3, 1);
	adc_set_resolution(ADC, ADC_MR_LOWRES_BITS_12);
	adc_enable_channel(ADC, pinmapping[pinNumber]);
	adc_configure_trigger(ADC, ADC_TRIG_SW, 0);
	
	return 0;	/* if everything is ok */
}

uint32_t analogRead(int pinNumber)
{
	adc_start(ADC);
	delayMicroseconds(300);
	uint32_t result = adc_get_channel_value(ADC, pinmapping[pinNumber]);	/* Replace with actual value read from A/D input*/
	return result;
	
}