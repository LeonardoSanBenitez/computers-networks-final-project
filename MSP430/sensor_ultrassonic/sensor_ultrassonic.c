/*
 *  sensor_ultrassonic.c
 *  Created on: 22 de ago de 2020
 *  Author: benitez
 *
 *  Read two ultrassonic sensors HCSR04
 *  Timer em modo captura.
 *  Para evitar problemas de sincronização, o ideal seria triggar por um timer
 *  Pinout:
 *    MSP Pin      Signal
 *    P2.0/TB1.1   Echo0 (needs 5V->3.3V conversion)
 *    P2.2         Trig0
 *    P2.1/TB1.2   Echo1 (needs 5V->3.3V conversion)
 *    P2.4         Trig1
 *  Hardware resources:
 *    TIMER1_B1
 *    Pins described above
 */

#include "sensor_ultrassonic.h"

#define COLLISION_THRESHOLD 20000
/* Conversion to mm
 * (CCRn_countB - CCRn_countA)*1715/(_f*10000) = measure_in_mm (without prescaller)
 * 20k = 142mm
 */

uint8_t _f;
void (*_collision_callback)() = 0;

volatile uint16_t CCR1_countA;
volatile uint16_t CCR1_countB;
volatile uint8_t CCR1_state = 0;

volatile uint16_t CCR2_countA;
volatile uint16_t CCR2_countB;
volatile uint8_t CCR2_state = 0;

// @Parameter f: global frequency in MHz
// @Parameter *collision_callback: will be called when an object is too close
void sensor_ultrassonic_init(uint8_t f, void (*collision_callback)()){
	_f = f;
	_collision_callback = collision_callback;

	CLR_BIT(P2DIR, BIT0 | BIT1); // input
	SET_BIT(P2REN, BIT0 | BIT1); // pull enable
	CLR_BIT(P2OUT, BIT0 | BIT1); // pull down
    P2SEL0 = BIT0 | BIT1; //Input capture for P2.0

	SET_BIT(P2DIR, BIT2 | BIT4); //output 

	sensor_ultrassonic_trigger();
}





void sensor_ultrassonic_trigger(){
    // Echo goes high for a period of time which will be equal to the time taken for the US wave to return back to the sensor
    // Enable Timer
	TB1CCTL1 |= CM_3 | CCIS_0 | CCIE | CAP | SCS;
	TB1CCTL2 |= CM_3 | CCIS_0 | CCIE | CAP | SCS;
                                                    // Capture in both rising and falling edge,
                                                    // Use CCI0A,
                                                    // Synchronous capture,
                                                    // Enable capture mode,
                                                    // Enable capture interrupt
	                                                // Enable overflow interrupt

    TB1CTL |= TBSSEL_2 | MC_2 | TBCLR | TBIE;// | ID__4;      // Use SMCLK as clock source, clear TB1R, prescaller 4x


    // kept Trigger high for 10us
    int count = 0;
    int max = _f*10;
    SET_BIT(P2OUT, BIT2 | BIT4);
    while (count<=max){count++;}
    CLR_BIT(P2OUT, BIT2 | BIT4);
}

uint8_t sensor_ultrassonic_collision_policy(){
    if (((CCR1_countB - CCR1_countA) < COLLISION_THRESHOLD ) || ((CCR2_countB - CCR2_countA) < COLLISION_THRESHOLD)){
        SET_BIT(PORT_OUT(LED1_PORT), LED1_BIT); // LED
        return 1;
    } else{
        CLR_BIT(PORT_OUT(LED1_PORT), LED1_BIT); // LED
        return 0;
    }
}

// Timer1 Interrupt Handler
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector = TIMER1_B1_VECTOR
__interrupt void TIMER1_B1_ISR(void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(TIMER1_B0_VECTOR))) TIMER1_B0_ISR (void)
#else
#error Compiler not supported!
#endif
{
    switch(__even_in_range(TB1IV,0x0A))
    {
        /* Vector  0:  No interrupt */
        case  TB1IV_NONE:
            break;

        /* Vector  2:  TBCCR1 CCIFG -> Comparator 1*/
        case  TB1IV_TBCCR1:
            TB1CCTL1 &= ~CCIFG;
            if (CCR1_state==0){ //Rising edge,begin of the read
                CCR1_countA = TB1CCR1;
                CCR1_state=1;
            } else if (CCR1_state==1){ //falling edge, end of the read
                CCR1_countB = TB1CCR1;
                CCR1_state=2;
            }
            break;
        /* Vector  4:  TBCCR2 CCIFG -> Comparator 2*/
        case TB1IV_TBCCR2:
            TB1CCTL2 &= ~CCIFG;
            if (CCR2_state==0){ //Rising edge,begin of the read
                CCR2_countA = TB1CCR2;
                CCR2_state=1;
            } else if (CCR2_state==1){ //falling edge, end of the read
                CCR2_countB = TB1CCR2;
                CCR2_state=2;
            }
            break;

        /* Vector 10:  TBIFG -> Overflow do timer 0*/
        case TB1IV_TBIFG:
            //TODO: nunca entra aqui
            CCR1_state = 2;
            CCR2_state = 2;
            CCR1_countB = 65535;
            CCR1_countA = 0;
            CCR2_countB = 65535;
            CCR2_countA = 0;
            break;
        default:
            break;
    }
    if (CCR1_state==2 && CCR2_state==2){
        CCR1_state = 0;
        CCR2_state = 0;

        //check for collision
        if (sensor_ultrassonic_collision_policy()){
            //stop timer and call callback
            CLR_BIT(TB1CCTL1, CCIE);
            CLR_BIT(TB1CCTL2, CCIE);
            (*_collision_callback)();
        } else {
            // Read continuously
            sensor_ultrassonic_trigger();
        }
    }

}


