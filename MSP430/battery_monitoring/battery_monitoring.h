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

//@Brief: initializations
//@Hardware: timer B0, ADC
//@Parameter f: frequency
//@Parameter death_callback: will be called if the battery is critically low
void battery_monitoring_init(uint8_t f, void (*death_callback)());


#endif /* BATTERY_MONITORING_BATTERY_MONITORING_H_ */
