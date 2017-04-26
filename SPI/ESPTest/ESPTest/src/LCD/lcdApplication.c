/*
 * lcdApplication.c
 *
 * Created: 2015-09-10 08:44:50
 *  Author: Anton Hellbe, Gustaf Bohlin
 */ 

#include "stdio.h"
#include "lcdApplication.h"
#include "LCDFunctions.h"
#include "buttons.h"	/* to get the buttontype definiton */

int lcdWrite4DigitNumber(int number)
{
	char toWrite[5];	/*define a char array to store number in*/
	sprintf(toWrite, "%d", number);	/*convert integer to char array*/
	uint8_t i = 0;
	while(toWrite[i] != '\0')	/*write all chars to display*/
	{
		lcdWrite(toWrite[i++], HIGH);
	}
	
	return 0;	/* Assuming everything went ok */
}

int lcdWriteAsciiString(const char *string)
/* writes an ascii string up to 40 characters on the LCD display */
{	
	while (*string != '\0')
	{
		lcdWrite(*string, HIGH);	/*write the char the pointer points at*/
		string++;	/*point at the next char*/
	}	
	return 0;	/* Assuming everything went ok */
}

int lcdWriteButtonValue(buttonType inputButton)
{
	/*write to lcd depending on what button was pressed*/
	switch(inputButton) {
		case btnRIGHT:
			lcdWriteAsciiString("RIGHT");
		break;
		case btnLEFT:
			lcdWriteAsciiString("LEFT");
		break;
		case btnDOWN:
			lcdWriteAsciiString("DOWN");
		break;
		case btnUP:
			lcdWriteAsciiString("UP");
		break;
		case btnSELECT:
			lcdWriteAsciiString("SELECT");
		break;
		case btnNONE:
			lcdWriteAsciiString("NONE");
		break;
		default:
			lcdWriteAsciiString("ERROR");
		break;	
	}
	return 0;	/* Assuming everything went ok */
}