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

#define BUFFER_SIZE 8
#define USART_BAUD_RATE 115200
#define CONF_UART USART1

uint8_t receive_buffer[BUFFER_SIZE];

freertos_usart_if freertos_usart;
// Configuration structure.
freertos_peripheral_options_t driver_options = {
	// This peripheral has full duplex asynchronous operation, so the
	// receive_buffer value is set to a valid buffer location (declared
	// above).
	receive_buffer,
	// receive_buffer_size is set to the size, in bytes, of the buffer
	// pointed to by the receive_buffer value.
	BUFFER_SIZE,
	// The interrupt priority.  The FreeRTOS driver provides the interrupt
	// service routine, and handles all interrupt interactions.  The
	// application writer does not need to provide any interrupt handling
	// code, but does need to specify the priority of the DMA interrupt here.
	// IMPORTANT!!!  see <a href="http://www.freertos.org/RTOS-Cortex-M3-M4.html">how to set interrupt priorities to work with FreeRTOS</a>
	0x0e,
	// The operation_mode value.
	USART_RS232,
	// Flags set to allow access from multiple tasks, and to wait in the
	// transmit function until the transmit is complete.  Note that other
	// FreeRTOS tasks will execute during the wait period.
	(USE_RX_ACCESS_MUTEX | WAIT_TX_COMPLETE)
};
// The RS232 configuration.  This structure, and the values used in its
// setting, are from the standard ASF USART driver.
const sam_usart_opt_t usart_settings =
{
	USART_BAUD_RATE,
	US_MR_CHRL_8_BIT,
	US_MR_PAR_NO,
	US_MR_NBSTOP_1_BIT,
	US_MR_CHMODE_NORMAL,
	0 // Only used in IrDA mode, so all values are ignored.
};



#define BUFFER_SIZE_CONSOLE 8
#define UART_BAUD_RATE_CONSOLE 115200

uint8_t receive_buffer_console[BUFFER_SIZE_CONSOLE];

freertos_usart_if freertos_uart;
// Configuration structure.
freertos_peripheral_options_t driver_options_console = {
	// This peripheral has full duplex asynchronous operation, so the
	// receive_buffer value is set to a valid buffer location (declared
	// above).
	receive_buffer_console,
	// receive_buffer_size is set to the size, in bytes, of the buffer
	// pointed to by the receive_buffer value.
	BUFFER_SIZE_CONSOLE,
	// The interrupt priority.  The FreeRTOS driver provides the interrupt
	// service routine, and handles all interrupt interactions.  The
	// application writer does not need to provide any interrupt handling
	// code, but does need to specify the priority of the DMA interrupt here.
	// IMPORTANT!!!  see <a href="http://www.freertos.org/RTOS-Cortex-M3-M4.html">how to set interrupt priorities to work with FreeRTOS</a>
	0x0e,
	// The operation_mode value.
	UART_RS232,
	// Flags set to allow access from multiple tasks, and to wait in the
	// transmit function until the transmit is complete.  Note that other
	// FreeRTOS tasks will execute during the wait period.
	(USE_TX_ACCESS_MUTEX | USE_RX_ACCESS_MUTEX | WAIT_TX_COMPLETE)
};
// The RS232 configuration.  This structure, and the values used in its
// setting, are from the standard ASF USART driver.
const sam_usart_opt_t uart_settings_console =
{
	UART_BAUD_RATE_CONSOLE,
	US_MR_CHRL_8_BIT,
	US_MR_PAR_NO,
	US_MR_NBSTOP_1_BIT,
	US_MR_CHMODE_NORMAL,
	0 // Only used in IrDA mode, so all values are ignored.
};


int main (void)
{
	// Insert system clock initialization code here (sysclk_init()).
	sysclk_init();
	board_init();
	sysclk_enable_peripheral_clock(CONSOLE_UART_ID);
	
	// Call the USART specific FreeRTOS ASF driver initialization function,
	// storing the return value as the driver handle.
	//freertos_usart = freertos_usart_serial_init(CONF_UART, &usart_settings,
	//&driver_options);
	
	freertos_uart = freertos_uart_serial_init(CONF_UART_CONSOLE, &uart_settings_console,
	&driver_options_console);
	
	/*const sam_usart_opt_t usart_serial_options = {
		.baudrate = CONF_UART_BAUDRATE,
		.paritytype = CONF_UART_PARITY,
		.charlength = CONF_UART_CHAR_LENGTH,
		.stopbits = CONF_UART_STOP_BITS
	};

	/* Configure console UART. */
	//sysclk_enable_peripheral_clock(BOARD_USART1_BASE);
	//freertos_usart_serial_init(CONF_UART, &usart_serial_options)
	
	if (xTaskCreate(task_dummy1, (const signed char * const) "task_dummy1", TASK_DUMMY1_STACK_SIZE, NULL, TASK_DUMMY1_STACK_PRIORITY, NULL) != pdPASS)
	{
	}
	if (xTaskCreate(task_dummy2, (const signed char * const) "task_dummy2", TASK_DUMMY2_STACK_SIZE, NULL, TASK_DUMMY2_STACK_PRIORITY, NULL) != pdPASS)
	{
	}
	if (xTaskCreate(task_uart, (const signed char * const) "task_uart", TASK_LED_STACK_SIZE, &freertos_uart, TASK_LED_STACK_PRIORITY, NULL) != pdPASS)
	{
	}
	vTaskStartScheduler();
	// Insert application code here, after the board has been initialized.
	while(1);
}