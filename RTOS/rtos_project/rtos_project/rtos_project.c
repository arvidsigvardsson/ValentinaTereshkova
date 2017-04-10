/*
 * rtos_project.c
 *
 * Created: 2017-04-10 14:02:56
 *  Author: Anton
 */ 

#include <asf.h>
#include "../pins/Init_Pins.h"
#include "../delay/delayFunctions.h"

/**
 * \brief Application entry point.
 *
 * \return Unused (ANSI-C compatibility).
 */
int main(void)
{
	sysclk_init();
    board_init();
	init_pins();
	delayInit();
	
    while (1) 
    {
        //TODO:: Please write your application code 
    }
}
