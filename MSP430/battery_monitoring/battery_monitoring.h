/*
 * battery_monitoring.h
 *
 *  Created on: 21 de ago de 2020
 *      Author: benitez
 */

#ifndef BATTERY_MONITORING_BATTERY_MONITORING_H_
#define BATTERY_MONITORING_BATTERY_MONITORING_H_

#include <msp430.h>
#include <stdint.h>

volatile unsigned int ADC_Result[3];             // 12-bit ADC conversion result array
volatile unsigned char i;

//@Brief: initializations
//@Hardware: timer B0, ADC
//@Parameter f: frequency
//@Parameter death_callback: will be called if the battery is critically low
void battery_monitoring_init(uint8_t f, void (*death_callback)());

//@Brief: check if the values read are normal
//@Return: 1 (normal) or 0 (not normal)
//TODO: receive a callback function as parameter
uint8_t battery_monitoring_death_policy ();


#endif /* BATTERY_MONITORING_BATTERY_MONITORING_H_ */
