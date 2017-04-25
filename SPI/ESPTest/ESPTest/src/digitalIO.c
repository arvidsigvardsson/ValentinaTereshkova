/*
 * digitalIO.c
 *
 * Created: 2015-06-10 15:11:18
 *  Author: Ulrik
 *  Editors: Gustaf Bohlin & Anton Hellbe
 */ 

#include <inttypes.h>	/* See http://en.wikipedia.org/wiki/C_data_types#Fixed-width_integer_types for more info */
#include <asf.h>		/* Only needed to get the definitions for HIGH and LOW */
#include "digitalIO.h"

#define PIOB_BASE_ADDRESS 0x400E1000U
static uint32_t *const p_PIOB_PER = (uint32_t *) (PIOB_BASE_ADDRESS+0x0000U);
static uint32_t *const p_PIOB_OER = (uint32_t *) (PIOB_BASE_ADDRESS+0x0010U);
static uint32_t *const p_PIOB_SODR = (uint32_t *) (PIOB_BASE_ADDRESS+0x0030U);
static uint32_t *const p_PIOB_CODR = (uint32_t *) (PIOB_BASE_ADDRESS+0x0034U);



void pinMode(int pinNumber, mode_definition mode)
{		
	/*if pin sent in is 13, use pinNumber 27*/
	if(pinNumber == 13) {
		pinNumber = 27;
	}
	/*if pin sent in is 22, use pinNumber 26*/
	else if (pinNumber == 22)
	{
		pinNumber = 26;
	}
	
	if (mode == OUTPUT)	/* You only have to program a function that cares about OUTPUT, and does nothing for the other values */
	{
		//enable port B registers
		*p_PIOB_PER |= (1<<(pinNumber));
		//port B, pinNumber output
		*p_PIOB_OER |= (1<<(pinNumber));
	}
	else
	{
		/* Do nothing */
	}
}

void digitalWrite(int pinNumber, int value)
{	
	//0b00010100
	//0b00001101
	//0b00000001
	
	//*(value ? (p_PIOB_SODR) : (p_PIOB_CODR)) |= (1 << (26 + (0x1 & pinNumber)));
	if (value == HIGH)
	{
		if (pinNumber == 13) 
		{
			/*set pin 27 (actual pin 13) to high*/
			*p_PIOB_SODR |= (1 << (27));
		}
		else if (pinNumber == 22)
		{
			/*set pin 26 (actual pin 22) to high*/
			*p_PIOB_SODR |= (1 << (26));
		}
	}
	else if (value == LOW)
	{
		if (pinNumber == 13)
		{
			/*set pin 27 (actual pin 13) to low*/
			*p_PIOB_CODR |= (1 << (27));
		}
		else if (pinNumber == 22)
		{
			/*set pin 26 (actual pin 22) to low*/
			*p_PIOB_CODR |= (1 << (26));
		}	
	}
	else
	{
		/* Something is wrong */
	}
}