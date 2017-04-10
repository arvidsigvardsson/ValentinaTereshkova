//
/*
Program som testar LEDs Och knappar
*/


#include <inttypes.h>
#include <asf.h>
#include "Init_Pins.h"


void init_pins(void)
{
	ioport_init();
	
	//Sätter våra Led-pinnar till outputs
	ioport_set_pin_dir(led1, IOPORT_DIR_OUTPUT);
	ioport_set_pin_dir(led2, IOPORT_DIR_OUTPUT);
	ioport_set_pin_dir(led3, IOPORT_DIR_OUTPUT);
	ioport_set_pin_dir(led4, IOPORT_DIR_OUTPUT);

}