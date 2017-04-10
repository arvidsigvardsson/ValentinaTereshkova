/*
 * task1.h
 *
 * Created: 2017-04-10 14:29:24
 *  Author: Anton
 */ 


#ifndef TASK1_H_
#define TASK1_H_

#define TASK_LED_STACK_SIZE (1024/sizeof(portSTACK_TYPE))
#define TASK_LED_STACK_PRIORITY (tskIDLE_PRIORITY)

void task_led(void *pvParameters);


#endif /* TASK1_H_ */