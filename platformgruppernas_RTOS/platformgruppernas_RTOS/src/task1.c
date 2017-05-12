/*
 * CFile1.c
 *
 * Created: 2017-04-10 14:29:08
 *  Author: Anton
 */ 

#include "asf.h"
#include "task1.h"
#include "stdio.h"

void task_uart(void *pvParameters)
{
	
	uint8_t req[] = "r";
	portTickType xLastWakeTime;
	const portTickType xTimeIncrement = 500;
	xLastWakeTime = xTaskGetTickCount();
	uint8_t rx[8];
	char c;
	uint8_t char_counter = 0;
	uint32_t counter = 0;
	
	uint16_t x1, y1, x2, y2;
	char sx1[4];
	char sy1[4];
	char sx2[4];
	char sy2[4];
	
	while(1)
	{
		//printf("data stuff\n");
		if ((CONF_UART_ESP->US_CSR & US_CSR_TXRDY)) {
			CONF_UART_ESP->US_THR = US_THR_TXCHR('r');
		}
		//usart_serial_read_packet(CONF_UART_ESP, &rx, 1);
		//printf("read");
		while(1) {
			delay_us(10);
			if (!(CONF_UART_ESP->US_CSR & US_CSR_RXRDY)) {
				counter++;
			}
			else {
				rx[char_counter++] = CONF_UART_ESP->US_RHR & 0xFF;US_RHR_RXCHR_Msk;
				counter = 0;
			}
			if(counter > 10000){
				counter = 0;
				char_counter = 0;
				break;
			}
		}
		
		x1 = (rx[0] << 8) | (rx[1] << 0);
		/*y1 = (rx[2] << 8) | (rx[3] << 0);
		x2 = (rx[4] << 8) | (rx[5] << 0);
		y2 = (rx[6] << 8) | (rx[7] << 0);*/
		
		
 		sprintf(sx1, "%d", rx[0]);
// // 		sprintf(sy1, "%d", y1);
// // 		sprintf(sx2, "%d", x2);
// // 		sprintf(sy2, "%d", y2);
// // 		
   		printf("1: %s\n", sx1);
// //  		printf("2: %s\n", sy1);
// //  		printf("3: %s\n", sx2);
// //  		printf("4: %s\n", sy2);
		
		vTaskDelayUntil(&xLastWakeTime, xTimeIncrement);
	}
}