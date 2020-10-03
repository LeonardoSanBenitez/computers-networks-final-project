/*
 * motor_control.h
 *
 *  Created on: 22 de ago de 2020
 *      Author: benitez
 */

#ifndef MOTOR_CONTROL_MOTOR_CONTROL_H_
#define MOTOR_CONTROL_MOTOR_CONTROL_H_

#include <msp430.h>
#include <stdint.h>
#include "lib/bits.h"

enum motor_state_t {
                      MOTOR_STATE_FORTH = (uint8_t) 0,
                      MOTOR_STATE_LEFT = (uint8_t) 1,
                      MOTOR_STATE_RIGHT = (uint8_t) 2,
                      MOTOR_STATE_STOP = (uint8_t) 3,
                      MOTOR_STATE_BACK = (uint8_t) 4,
};

/*
 * @Brief: configure
 * @Parameter: f = master frequency, in MHz
 */
void motor_control_init(int f);

/*
 * @Parameter motor1_dir:   0=back, 1=stop, 2=forth
 * @Parameter motor1_speed: from 0 to 100
 * @Parameter motor2_dir:   0=back, 1=stop, 2=forth
 * @Parameter motor2_speed: from 0 to 100
 * Cada motor é controlado de forma independente
 */
void motor_control_set_params(uint8_t motor1_dir, uint8_t motor1_speed, uint8_t motor2_dir, uint8_t motor2_speed);


#endif /* MOTOR_CONTROL_MOTOR_CONTROL_H_ */
