/*
 * CFile1.c
 *
 * Created: 2017-04-10 14:29:08
 *  Author: Anton
 */ 

#include "asf.h"
#include "task1.h"
#include "usb_print.h"


void task_uart(freertos_usart_if *pvParameters)
{
	
	const char req[] = "request!";
	const char ok[] = "okx";
	portTickType xLastWakeTime;
	const portTickType xTimeIncrement = 500;
	freertos_usart_if *freertos_usart = *pvParameters;
	xLastWakeTime = xTaskGetTickCount();
	uint8_t rx[8];
	
	while(1)
	{
		/*freertos_usart_serial_read_packet(freertos_usart, &rx, 8, 10);
		if (rx[1] == 200)
		{
			print(&rx, 8);
		}
		else {
			freertos_usart_write_packet(freertos_usart, (const uint8_t*)req, sizeof(req) - 1, 0);
		}*/
		vTaskDelayUntil(&xLastWakeTime, xTimeIncrement);
	}
}