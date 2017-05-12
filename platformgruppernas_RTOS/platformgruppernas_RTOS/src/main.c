/**
 * \file
 *
 * \brief Empty user application template
 *
 */

/**
 * \mainpage User Application template doxygen documentation
 *
 * \par Empty user application template
 *
 * Bare minimum empty user application template
 *
 * \par Content
 *
 * -# Include the ASF header files (through asf.h)
 * -# "Insert system clock initialization code here" comment
 * -# Minimal main function that starts with a call to board_init()
 * -# "Insert application code here" comment
 *
 */

/*
 * Include header files for all drivers that have been imported from
 * Atmel Software Framework (ASF).
 */
 /**
 * Support and FAQ: visit <a href="http://www.atmel.com/design-support/">Atmel Support</a>
 */
#include <asf.h>
#include "task1.h"
#include "dummyTask1.h"
#include "dummyTask2.h"
#include "consoleFunctions.h"


#define CONF_UART_CONSOLE UART
#define CONF_UART_CONSOLE_BAUDRATE 115200
#define CONF_UART_CONSOLE_PARITY UART_MR_PAR_NO

//#define CONF_UART_ESP USART1
#define CONF_UART_ESP_BAUDRATE	9600
#define CONF_UART_ESP_PARITY	US_MR_PAR_NO
#define CONF_UART_ESP_CHRLEN	9
#define CONF_UART_ESP_STOP_BITS		US_MR_NBSTOP_1_BIT

uint8_t rx[8];
uint8_t c_counter = 0;

void configure_console(void) {
	const usart_serial_options_t uart_serial_options = {
		.baudrate = CONF_UART_CONSOLE_BAUDRATE,
		.paritytype = CONF_UART_CONSOLE_PARITY
	};
	sysclk_enable_peripheral_clock(CONSOLE_UART_ID);
	stdio_serial_init(CONF_UART_CONSOLE, &uart_serial_options);
	
	const usart_serial_options_t uart_serial_options_esp = {
		.baudrate = CONF_UART_ESP_BAUDRATE,
		.paritytype = CONF_UART_ESP_PARITY,
		.charlength = CONF_UART_ESP_CHRLEN,
		.stopbits = CONF_UART_ESP_STOP_BITS
	};
	
	sysclk_enable_peripheral_clock(BOARD_USART1_BASE);
	usart_serial_init(CONF_UART_ESP, &uart_serial_options_esp);
	
	//CONF_UART_ESP->US_MR &= ~(0xF << 0);
	//CONF_UART_ESP->US_MR |= (0x3 << 6);
	//CONF_UART_ESP->US_MR |= (1 << 20);
}

void USART1_Handler() {
	CONF_UART_ESP->US_CR |= (1 << US_CR_RSTRX);
	rx[c_counter++] = CONF_UART_ESP->US_RHR & US_RHR_RXCHR_Msk;
	char a[1];
	sprintf(&a, "%d", rx[c_counter]);
	printf("%s\n", a);
	
	if (c_counter > 15)
	{
		c_counter = 0;
	}
}

int main (void)
{
	sysclk_init();
	board_init();
	delay_init();
	configure_console();
	/*NVIC_SetPriority((IRQn_Type) ID_USART1, 0x0e);
	usart_enable_interrupt(CONF_UART_ESP, UART_IER_RXRDY);
	NVIC_EnableIRQ((IRQn_Type) ID_USART1);*/
	
	if (xTaskCreate(task_dummy1, (const signed char * const) "task_dummy1", TASK_DUMMY1_STACK_SIZE, NULL, TASK_DUMMY1_STACK_PRIORITY, NULL) != pdPASS)
	{
	}
	if (xTaskCreate(task_dummy2, (const signed char * const) "task_dummy2", TASK_DUMMY2_STACK_SIZE, NULL, TASK_DUMMY2_STACK_PRIORITY, NULL) != pdPASS)
	{
	}
	if (xTaskCreate(task_uart, (const signed char * const) "task_uart", TASK_LED_STACK_SIZE, NULL, TASK_LED_STACK_PRIORITY, NULL) != pdPASS)
	{
	}
	vTaskStartScheduler();
	// Insert application code here, after the board has been initialized.
	while(1);
}