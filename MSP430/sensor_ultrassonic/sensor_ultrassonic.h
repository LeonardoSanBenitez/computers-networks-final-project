/*
 * sensor_ultrassonic.h
 *
 *  Created on: 22 de ago de 2020
 *      Author: Leonardo Benitez
 */

#ifndef SENSOR_ULTRASSONIC_SENSOR_ULTRASSONIC_H_
#define SENSOR_ULTRASSONIC_SENSOR_ULTRASSONIC_H_

#include <msp430.h>
#include <stdint.h>
#include <stdint.h>
#include "lib/bits.h"

void sensor_ultrassonic_init(uint8_t f, void (*collision_callback)());
void sensor_ultrassonic_trigger();
uint8_t sensor_ultrassonic_collision_policy();


#endif /* SENSOR_ULTRASSONIC_SENSOR_ULTRASSONIC_H_ */
