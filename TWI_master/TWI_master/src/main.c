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
#include "config/conf_board.h"
#include "DelayFunctions.h"
#include "LCD/lcdApplication.h"
#include "LCD/LCDFunctions.h"
#include <ioport.h>

typedef enum {
	WRITE,
	READ
} data_dir;

void conf_master_mode(void)
{
	CONF_BOARD_TWI0->TWI_MMR |= (TWI_MMR_IADRSZ_NONE);
	CONF_BOARD_TWI0->TWI_MMR |= (8 << TWI_MMR_DADR_Pos);
	//CONF_BOARD_TWI0->TWI_IADR |= (0x07 << TWI_IADR_IADR_Pos);
	CONF_BOARD_TWI0->TWI_CWGR |= (10 << TWI_CWGR_CKDIV_Pos);
	CONF_BOARD_TWI0->TWI_CR |= (1 << TWI_CR_SVDIS);
	CONF_BOARD_TWI0->TWI_CR |= (1 << TWI_CR_MSEN);
}

void set_data_dir(data_dir direction) {
	if (direction == READ)
	{
		CONF_BOARD_TWI0->TWI_MMR |= (1 << TWI_MMR_MREAD);
	} 
	else
	{
		CONF_BOARD_TWI0->TWI_MMR &= ~(1 << TWI_MMR_MREAD);
	}
	
}

void load_data_register(Byte data) {
	CONF_BOARD_TWI0->TWI_THR = data;
}

void write_stop_command(void) {
	CONF_BOARD_TWI0->TWI_CR |= (1 << TWI_CR_STOP);
}

uint8_t data_holding_register_is_ready(void) {
	return CONF_BOARD_TWI0->TWI_SR & TWI_SR_TXRDY;
}

uint8_t data_sent(void) {
	return CONF_BOARD_TWI0->TWI_SR & TWI_SR_TXCOMP;
}

int main (void)
{
	sysclk_init();
	board_init();
	delayInit();
	lcdInit();
	lcdWriteAsciiString("abc");
	delayMicroseconds(1000000);
	lcdClearDisplay();
	ioport_init();
	pmc_enable_periph_clk(ID_TWI1);
	sysclk_enable_peripheral_clock(ID_TWI1);
	lcdWriteAsciiString("a");
	ioport_enable_port(IOPORT_PIOB, IOPORT_DIR_OUTPUT);
	lcdWriteAsciiString("b");
	ioport_set_pin_dir(PIO_PB13_IDX, IOPORT_DIR_OUTPUT);
	lcdWriteAsciiString("c");
	conf_master_mode();
	set_data_dir(WRITE);
	load_data_register(0xFF);
	delayMicroseconds(10);
	write_stop_command();
	lcdWriteAsciiString("Writing to register");
	while(!data_holding_register_is_ready());
	lcdClearDisplay();
	lcdWriteAsciiString("holding register ready");
	while(!data_sent());
	lcdClearDisplay();
	lcdWriteAsciiString("data sent");
	while(1);
	//data byte is sent
}
