/***************************************************************************************
 *  MSP part of the project
 *  Author: Leonardo Benitez
 *  Coauthor: Renan Augusto Starke
 *  Date: 2020-10
 *  Hardware usage:
 *    Watchdog timer: delay
 *    Timer0_B0:      battery
 *    Timer1_B1:      ultrassonic
 *    Timer3_B:       motor
 *    EUSCI:          uart
 *    ADC: battery

****************************************************************************************/


/* System includes */

#include <msp430.h>
#include <stdint.h>
#include "lib/bits.h"
#include "lib/gpio.h"
#include "lib/uart_fr2355.h"
#include "boardDefinitions/MSP430FR2355.h"
#include "motor_control/motor_control.h"
#include "sensor_ultrassonic/sensor_ultrassonic.h"
#include "battery_monitoring/battery_monitoring.h"


/* Project includes */
#include "lib/bits.h"

#ifndef __MSP430FR2355__
#error "Clock system not supported/tested for this device"
#endif

volatile enum motor_state_t motor_state = MOTOR_STATE_STOP;
volatile uint16_t distance;

/**
  * @brief  Configura sistema de clock para usar o Digitally Controlled Oscillator (DCO) em 24MHz
  *         Essa configuração utiliza pinos para cristal externo.
  * @param  none
  *
  * @retval none
  */
void init_clock_24MHz(void) {

    // Configure two FRAM wait state as required by the device data sheet for MCLK
    // operation at 24MHz(beyond 8MHz) _before_ configuring the clock system.
    FRCTL0 = FRCTLPW | NWAITS_2 ;

    P2SEL1 |= BIT6 | BIT7;                       // P2.6~P2.7: crystal pins
    do
    {
        CSCTL7 &= ~(XT1OFFG | DCOFFG);           // Clear XT1 and DCO fault flag
        SFRIFG1 &= ~OFIFG;
    } while (SFRIFG1 & OFIFG);                   // Test oscillator fault flag

    __bis_SR_register(SCG0);                     // disable FLL
    CSCTL3 |= SELREF__XT1CLK;                    // Set XT1 as FLL reference source
    CSCTL0 = 0;                                  // clear DCO and MOD registers
    CSCTL1 = DCORSEL_7;                          // Set DCO = 24MHz
    CSCTL2 = FLLD_0 + 731;                       // DCOCLKDIV = 327358*731 / 1
    __delay_cycles(3);
    __bic_SR_register(SCG0);                     // enable FLL
    while(CSCTL7 & (FLLUNLOCK0 | FLLUNLOCK1));   // FLL locked

    /* CSCTL4 = SELMS__DCOCLKDIV | SELA__REFOCLK;
     * set XT1 (~32768Hz) as ACLK source, ACLK = 32768Hz
     * default DCOCLKDIV as MCLK and SMCLK source
     - Selects the ACLK source.
     * 00b = XT1CLK with divider (must be no more than 40 kHz)
     * 01b = REFO (internal 32-kHz clock source)
     * 10b = VLO (internal 10-kHz clock source) (1)   */
    CSCTL4 = SELMS__DCOCLKDIV | SELA__REFOCLK;
}

void collision_callback(){
    //TODO: collision avoidance proceadure will be done in raspberry
    motor_state = MOTOR_STATE_STOP;
    motor_control_set_params(1, 0, 1, 0);
}

void battery_death_callback(){
    //TODO: kill program? Raise exception?
    // desligar motor
    // desligar o resto
    // preferencialmente, desligar o raspberry
    motor_state = MOTOR_STATE_STOP;
    motor_control_set_params(1, 0, 1, 0);
}

int main(){
    char my_data[8];

    WDTCTL = WDTPW | WDTHOLD; // Stop watchdog timer
    PM5CTL0 &= ~LOCKLPM5;     // Disable the GPIO power-on

    /* Initializations */
    init_clock_24MHz();
    sensor_ultrassonic_init(24, &collision_callback);
    motor_control_init(24);
    init_uart();
    battery_monitoring_init(24, &battery_death_callback);

    /* Leds de depuração */
    SET_BIT(PORT_DIR(LED1_PORT), LED1_BIT);

    __bis_SR_register(GIE);
    while (1){
        /* Configura o recebimento de um pacote de 4 bytes */
        uart_receive_package((uint8_t *)my_data, 4);
        __bis_SR_register(CPUOFF | GIE); // Desliga a CPU enquanto pacote não chega

        /* Echo */
        //uart_send_package((uint8_t *)my_data[2], 2);
        //__bis_SR_register(CPUOFF | GIE);

        if (my_data[3] == (my_data[0]+my_data[1]+my_data[2])%256){
            // Checksum is right
            if ((my_data[2]>>4)==0x08){
                // Received a command
                if (my_data[2]==0x80){
                    motor_state = MOTOR_STATE_FORTH;
                    motor_control_set_params(2, 100, 2, 100);
                } else if (my_data[2]==0x81){
                    motor_state = MOTOR_STATE_LEFT;
                    motor_control_set_params(2, 100, 0, 100);
                } else if (my_data[2]==0x82){
                    motor_state = MOTOR_STATE_RIGHT;
                    motor_control_set_params(0, 100, 2, 100);
                } else if (my_data[2]==0x83){
                    motor_state = MOTOR_STATE_STOP;
                    motor_control_set_params(1, 0, 1, 0);
                } else if (my_data[2]==0x84){
                    motor_state = MOTOR_STATE_BACK;
                    motor_control_set_params(0, 100, 0, 100);
                }
                uart_send_package((uint8_t *)UART_ACK,sizeof(UART_ACK));
                __bis_SR_register(CPUOFF | GIE);
            }
            else if ((my_data[2]>>4)==0x00){
                // Received a read request
                if (my_data[2]==0x00){
                    uart_send_package((uint8_t *)&motor_state, sizeof(motor_state));
                    __bis_SR_register(CPUOFF | GIE);
                } else if (my_data[2]==0x01){
                   uint16_t value = sensor_ultrassonic_last_value();
                    uart_send_package((uint8_t *)&value, sizeof(value));
                    __bis_SR_register(CPUOFF | GIE);
                }
            }
        } else {
            //wrong checksum
            uart_send_package((uint8_t *)UART_NACK,sizeof(UART_NACK));
            __bis_SR_register(CPUOFF | GIE);
        }
    }
}
