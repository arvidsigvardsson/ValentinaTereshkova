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
#include <inttypes.h>
#include "ConsoleFunc/consoleFunctions.h"
#include "DelayFunctions.h"
#include "digitalIO.h"
#include "LCD/adcFunctions.h"
#include "LCD/buttons.h"
#include "LCD/lcdApplication.h"
#include "LCD/LCDFunctions.h"
static char alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789,.:+?_-/\\=!";
typedef enum aTCommands {AT, AT_RST, AT_CWMODE, AT_CWJAP, AT_CIPSTART, AT_CIPSEND, AT_ERROR, AT_CWJAP_CHECK, AT_STATUS, AT_GET} atCommands;

#define PIOB_BASE_ADDRESS 0x400E1000U
static uint32_t *const p_PIOB_PER = (uint32_t *) (PIOB_BASE_ADDRESS+0x0000U);
static uint32_t *const p_PIOB_OER = (uint32_t *) (PIOB_BASE_ADDRESS+0x0010U);
static uint32_t *const p_PIOB_SODR = (uint32_t *) (PIOB_BASE_ADDRESS+0x0030U);
static uint32_t *const p_PIOB_CODR = (uint32_t *) (PIOB_BASE_ADDRESS+0x0034U);

int contains(char rx) {
	for (uint8_t i = 0; i < sizeof(alphabet); i++)
	{
		if (rx == alphabet[i])
		{
			return 1;
		}
	}
	return 0;
}

atCommands btnCommand() {
	buttonType btn = readLCDbutton();
	atCommands atcom;
	switch(btn) {
		case btnRIGHT:
		atcom = AT_CIPSEND;
		break;
		case btnLEFT:
		atcom = AT_CIPSTART;
		break;
		case btnDOWN:
		atcom = AT_CWJAP;
		break;
		case btnUP:
		atcom = AT_CWMODE;
		break;
		case btnSELECT:
		atcom = AT_RST;
		break;
		case btnNONE:
		atcom = AT_ERROR;
		break;
		default:
		atcom = AT_ERROR;
		break;
	}
	return atcom;
}

uint32_t sendATCommand(atCommands selection) {
	uint8_t rx[200];
	uint32_t counter = 0;
	uint32_t char_counter = 0;
	switch(selection) {
		case AT:
		;
		const char at[] = "AT\r\n";
		usart_serial_write_packet(CONF_UART, (const uint8_t*)at, sizeof(at) - 1);
		break;
		case AT_CIPSEND:
		;
		const char _at[] = "AT+CIPSEND=54\r\n";
		usart_serial_write_packet(CONF_UART, (const uint8_t*)_at, sizeof(_at) - 1);
		break;
		case AT_CIPSTART:
		;
		const char __at[] = "AT+CIPSTART=\"TCP\",\"192.168.20.111\",5000\r\n";
		usart_serial_write_packet(CONF_UART, (const uint8_t*)__at, sizeof(__at) - 1);
		break;
		case AT_CWJAP:
		;
		const char ___at[] = "AT+CWJAP=\"VHAM\",\"MAHVMAHV\"\r\n";
		usart_serial_write_packet(CONF_UART, (const uint8_t*)___at, sizeof(___at) - 1);
		break;
		case AT_CWMODE:
		;
		const char ____at[] = "AT+CWMODE=3\r\n";
		usart_serial_write_packet(CONF_UART, (const uint8_t*)____at, sizeof(____at) - 1);
		break;
		break;
		case AT_RST:
		;
		const char _____at[] = "AT+RST\r\n";
		usart_serial_write_packet(CONF_UART, (const uint8_t*)_____at, sizeof(_____at) - 1);
		break;
		case AT_CWJAP_CHECK:
		;
		const char ______at[] = "AT+CWJAP?\r\n";
		usart_serial_write_packet(CONF_UART, (const uint8_t*)______at, sizeof(______at) - 1);
		break;
		case AT_STATUS:
		;
		const char _______at[] = "AT+CIPSTATUS\r\n";
		usart_serial_write_packet(CONF_UART, (const uint8_t*)_______at, sizeof(_______at) - 1);
		break;
		case AT_GET:
		;
		const char ________at[] = "GET todo/api/v1.0/coordinate/getlatest HTTP/1.1\r\n\r\n\r\n";
		usart_serial_write_packet(CONF_UART, (const uint8_t*)________at, sizeof(________at) - 1);
		break;
		case AT_ERROR:
		return 0;
		break;
		default:
		return 0;
		break;
	}
	if (selection == AT_GET) delayMicroseconds(200000);
	delayMicroseconds(1000);
	while(1) {
		if (!(CONF_UART->US_CSR & US_CSR_RXRDY)) {
			counter++;
		}
		else {
			rx[char_counter++] = CONF_UART->US_RHR & US_RHR_RXCHR_Msk;
			counter = 0;
		}
		delayMicroseconds(5);
		if(counter > 1000){
			counter = 0;
			break;
		}
	}
	for (uint32_t i = 0; i < char_counter; i++)
	{
		if (contains(rx[i]))
		{
			lcdWrite(rx[i], HIGH);
		}
		
	}
	delayMicroseconds(6000000);
	return 0;
}



int main (void)
{
	sysclk_init();
	delayInit();
	board_init();
	lcdInit();
	configureConsole();
	atCommands selection[10] = {AT_RST, AT, AT_CWMODE, AT_CWJAP, AT_CWJAP_CHECK, AT_CIPSTART, AT_STATUS, AT_CIPSEND, AT_GET};
	uint8_t counter = 0;
	lcdWriteAsciiString("Booting...");
	delayMicroseconds(1000000);
	while(1) {
		lcdClearDisplay();
		sendATCommand(selection[counter++]);
		if (counter > sizeof(selection) - 1) break;
	}
	while(1);
	// Insert application code here, after the board has been initialized.
}


