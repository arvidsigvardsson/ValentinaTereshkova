/*
 * CFile1.c
 *
 * Created: 2017-04-10 14:29:08
 *  Author: Anton
 */ 

#include "asf.h"
#include "task1.h"
#include "gpio.h"
#include "stdio_serial.h"
#include "../pins/Init_Pins.h"

static int state = 1;


void task_led(void *pvParameters)
{
	printf("TASK_LED");
	portTickType xLastWakeTime;
	const portTickType xTimeIncrement = 500;
	
	xLastWakeTime = xTaskGetTickCount();
	
	while(1)
	{
		vTaskDelayUntil(&xLastWakeTime, xTimeIncrement);
		ioport_set_pin_level(led4, state); // TODO - Insert PIN
		state ^= 1;
	}
}