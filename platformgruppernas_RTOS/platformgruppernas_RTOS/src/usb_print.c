/*
 * usb_print.c
 *
 * Created: 08/05/2017 17:42:41
 *  Author: Gustaf Bohlin
 */ 

#include <asf.h>

#define BUFFER_SIZE 8
#define UART_BAUD_RATE 115200

// Declare the variables used as parameters to the
// freertos_uart_serial_init() function.
// Declare a buffer to be used as the UART receive DMA buffer.  The FreeRTOS
// peripheral control drivers manage this buffer, and use it as a circular
// buffer.
uint8_t receive_buffer[BUFFER_SIZE];
// Handle used to access the initialized port by other FreeRTOS ASF functions.
freertos_uart_if freertos_uart;
// Configuration structure.
freertos_peripheral_options_t driver_options_uart = {
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
	UART_RS232,
	// Flags set to allow access from multiple tasks, and to wait in the
	// transmit function until the transmit is complete.  Note that other
	// FreeRTOS tasks will execute during the wait period.
	(USE_RX_ACCESS_MUTEX | WAIT_TX_COMPLETE)
};
// The RS232 configuration.  This structure, and the values used in its
// setting, are from the standard ASF UART driver.
const sam_uart_opt_t uart_settings =
{
	UART_BAUD_RATE,
	US_MR_CHRL_8_BIT,
	US_MR_PAR_NO,
	US_MR_NBSTOP_1_BIT,
	US_MR_CHMODE_NORMAL,
	0 // Only used in IrDA mode, so all values are ignored.
};
// Call the UART specific FreeRTOS ASF driver initialization function,
// storing the return value as the driver handle.

void init(void) {
	freertos_uart = freertos_uart_serial_init(CONF_UART_CONSOLE, &uart_settings,
	&driver_options_uart);
}


void print(char *p_mess, uint8_t len) {
	freertos_uart_write_packet(freertos_uart, p_mess, len, 0);
}