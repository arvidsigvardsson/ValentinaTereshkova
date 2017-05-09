/*
 * dummyTask1.h
 *
 * Created: 08/05/2017 14:51:08
 *  Author: Gustaf Bohlin
 */ 


#ifndef DUMMYTASK1_H_
#define DUMMYTASK1_H_

#define TASK_DUMMY1_STACK_SIZE (1024/sizeof(portSTACK_TYPE))
#define TASK_DUMMY1_STACK_PRIORITY (tskIDLE_PRIORITY)

void task_dummy1(void *pvParameters);

#endif /* DUMMYTASK1_H_ */