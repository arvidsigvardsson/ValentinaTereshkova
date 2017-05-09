/*
 * dummyTask1.c
 *
 * Created: 08/05/2017 14:50:45
 *  Author: Gustaf Bohlin
 */ 
#include "asf.h"
#include "dummyTask1.h"


void task_dummy1(void *pvParameters)
{
	portTickType xLastWakeTime;
	const portTickType xTimeIncrement = 500;
	
	xLastWakeTime = xTaskGetTickCount();
	
	while(1)
	{
		vTaskDelayUntil(&xLastWakeTime, xTimeIncrement);
	}
}