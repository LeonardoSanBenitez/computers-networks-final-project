/*
 * sensor_ultrassonic.h
 *
 *  Created on: 22 de ago de 2020
 *      Author: Leonardo Benitez
 */

#ifndef SENSOR_ULTRASSONIC_SENSOR_ULTRASSONIC_H_
#define SENSOR_ULTRASSONIC_SENSOR_ULTRASSONIC_H_

#define COLLISION_THRESHOLD 20000
/* Conversion to mm
 * (CCRn_countB - CCRn_countA)*1715/(_f*10000) = measure_in_mm (without prescaller)
 * 20k = 142mm
 */

#include <msp430.h>
#include <stdint.h>
#include <stdint.h>
#include "lib/bits.h"
#include "lib/gpio.h"
#include "boardDefinitions/MSP430FR2355.h"

void sensor_ultrassonic_init(uint8_t f, void (*collision_callback)());
uint16_t sensor_ultrassonic_last_value();


//void sensor_ultrassonic_trigger();

#endif /* SENSOR_ULTRASSONIC_SENSOR_ULTRASSONIC_H_ */
