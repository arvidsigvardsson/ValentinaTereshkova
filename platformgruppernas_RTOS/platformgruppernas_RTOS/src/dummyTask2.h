/*
 * dummyTask2.h
 *
 * Created: 08/05/2017 14:51:18
 *  Author: Gustaf Bohlin
 */ 


#ifndef DUMMYTASK2_H_
#define DUMMYTASK2_H_

#define TASK_DUMMY2_STACK_SIZE (1024/sizeof(portSTACK_TYPE))
#define TASK_DUMMY2_STACK_PRIORITY (tskIDLE_PRIORITY)

void task_dummy2(void *pvParameters);

#endif /* DUMMYTASK2_H_ */