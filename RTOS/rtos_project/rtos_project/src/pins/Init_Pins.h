


#ifndef Init_h
#define Init_h
#include "asf.h"

//Definierar våra LED-pinnar
#define led1 PIO_PB25_IDX
#define led2 PIO_PC28_IDX
#define led3 PIO_PC26_IDX
#define led4 PIO_PC25_IDX


void init_pins(void);

#endif
