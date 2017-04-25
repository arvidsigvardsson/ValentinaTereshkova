/*
 * buttons.c
 *
 * Created: 2015-06-12 16:28:53
 * Author: Anton Hellbe, Gustaf Bohlin
 */ 

#include "buttons.h"
#include "adcFunctions.h"	/* Must use the value from the ADC to figure out which button */

buttonType readLCDbutton(void)
{
	buttonType btn;
	int value = analogRead(0);	/*Read the analog value on port 0*/
	/*Decide what button was pressed by dividing them into intervals*/
	if(value < 500) {
		btn = btnRIGHT;
	}
	else if(value > 500 && value < 1000) 
	{
		btn = btnUP;
	}
	else if(value > 1000 && value < 1500) 
	{
		btn = btnDOWN;
	}
	else if(value > 1500 && value < 2000) 
	{
		btn = btnLEFT;
	}
	else if(value > 2000 && value < 2500) 
	{
		btn = btnSELECT;
	}
	else 
	{
		btn = btnNONE;
	}
	return btn;
}