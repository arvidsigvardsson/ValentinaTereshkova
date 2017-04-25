/*
 * buttons.h
 *
 * Created: 2015-06-12 16:29:24
 * Author: Ulrik Eklund
 */ 


#ifndef BUTTONS_H_
#define BUTTONS_H_

typedef enum button {btnRIGHT, btnUP, btnDOWN, btnLEFT, btnSELECT, btnNONE} buttonType;
buttonType readLCDbutton(void);

#endif /* BUTTONS_H_ */