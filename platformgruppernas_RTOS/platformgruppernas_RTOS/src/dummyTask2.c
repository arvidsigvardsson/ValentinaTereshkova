/*
 * dummyTask2.c
 *
 * Created: 08/05/2017 14:50:55
 *  Author: Gustaf Bohlin
 */ 

#include "asf.h"
#include "dummyTask2.h"


void task_dummy2(void *pvParameters)
{
	portTickType xLastWakeTime;
	const portTickType xTimeIncrement = 500;
	
	xLastWakeTime = xTaskGetTickCount();
	
	while(1)
	{
		vTaskDelayUntil(&xLastWakeTime, xTimeIncrement);
	}
}