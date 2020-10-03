/*
 * motor_control.c
 *
 *  Created on: 22 de ago de 2020
 *  Author: benitez
 *  Based on: http://dev.ti.com/tirex/explore/node?devtools=MSP-EXP430FR2355&kernels=nortos&node=ANpcp-O2BhrQD6mIInmeag__IOGqZri__LATEST&resourceClasses=example
 */

#include "motor_control.h"



uint16_t motor_control_f;

void motor_control_init(int f){
    // Configure GPIO, all off
    P6DIR |= BIT0 | BIT1 | BIT2 | BIT3;               // P6.0 P6.1 P6.2 P6.3 direction output
    P6SEL0 &= ~(BIT0 | BIT1 | BIT2 | BIT3);           // P6.0 P6.1 P6.2 P6.3 options select
    P6OUT &= ~(BIT0 | BIT1 | BIT2 | BIT3);            // P6.0 P6.1 P6.2 P6.3 output=0

    // Setup Timer3_B
    TB3CCR0 = f*1000-1;                               //PWM period at 1kHz

    TB3CCTL1 = OUTMOD_7;                              // CCR1 reset/set
    TB3CCTL2 = OUTMOD_7;                              // CCR2 reset/set
    TB3CCTL3 = OUTMOD_7;                              // CCR3 reset/set
    TB3CCTL4 = OUTMOD_7;                              // CCR4 reset/set

    TB3CTL = TBSSEL_2 | MC_1 | TBCLR;                 // ACLK, up mode, clear TBR
    motor_control_f = f;
}

void motor_control_set_params(uint8_t motor1_dir, uint8_t motor1_speed, uint8_t motor2_dir, uint8_t motor2_speed){
    //low: DIR=1, SEL1=0, SEL0=0, OUT=0
    //pwm: DIR=1, SEL1=0, SEL0=1

    /*
     * PWM1  = P6.0 -> TB3.1 pwm or low
     * PWM1n = P6.1 -> TB3.2 pwm or low
     * PWM2  = P6.2 -> TB3.3 pwm or low
     * PWM2n = P6.3 -> TB3.4 pwm or low
     */
    //Configure speed by duty_cycle
    TB3CCR1 = motor_control_f*10*motor1_speed -1;
    TB3CCR2 = motor_control_f*10*motor1_speed -1;
    TB3CCR3 = motor_control_f*10*motor2_speed -1;
    TB3CCR4 = motor_control_f*10*motor2_speed -1;

    if (motor1_dir==2){
        //PWM1 to timer output, PWM1n to low
        CLR_BIT(P6SEL0, BIT1);
        CLR_BIT(P6OUT, BIT1);

        SET_BIT(P6SEL0, BIT0);
    } else if (motor1_dir==1){
        //PWM1 to low, PWM1n to low
        CLR_BIT(P6SEL0, BIT1);
        CLR_BIT(P6OUT, BIT1);

        CLR_BIT(P6SEL0, BIT0);
        CLR_BIT(P6OUT, BIT0);

    } else {
        //PWM1 to low, PWM1n to timer output
        CLR_BIT(P6SEL0, BIT0);
        CLR_BIT(P6OUT, BIT0);

        SET_BIT(P6SEL0, BIT1);
    }


    if (motor2_dir==2){
        //PWM2 to timer output, PWM2n to low
        CLR_BIT(P6SEL0, BIT3);
        CLR_BIT(P6OUT, BIT3);

        SET_BIT(P6SEL0, BIT2);
    } else if (motor2_dir==1){
        //PWM2 to low, PWM2n to low
        CLR_BIT(P6SEL0, BIT3);
        CLR_BIT(P6OUT, BIT3);

        CLR_BIT(P6SEL0, BIT2);
        CLR_BIT(P6OUT, BIT2);
    } else {
        //PWM2 to low, PWM2n to timer output
        CLR_BIT(P6SEL0, BIT2);
        CLR_BIT(P6OUT, BIT2);

        SET_BIT(P6SEL0, BIT3);
    }
}






