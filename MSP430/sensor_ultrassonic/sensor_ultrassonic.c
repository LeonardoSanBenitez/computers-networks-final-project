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
 *    Watchdog
 *    Pins described above
 */

#include "sensor_ultrassonic.h"

uint8_t _f;
void (*_collision_callback)() = 0;

volatile uint16_t CCR1_countA;
volatile uint16_t CCR1_countB;
volatile uint32_t CCR1_sum = 0; //used for averaging
volatile uint8_t CCR1_state = 0;

volatile uint8_t measure_count = 0;
volatile uint8_t watchdog_count = 0;
volatile uint16_t last_value = 0; //for debug
volatile uint8_t timer_busy = 0;


// @Parameter f: global frequency in MHz (not eveything is automatically calculated)
// @Parameter *collision_callback: will be called when an object is too close
void sensor_ultrassonic_init(uint8_t f, void (*collision_callback)()){
	_f = f;
	_collision_callback = collision_callback;

	CLR_BIT(P2DIR, BIT0); // input
	SET_BIT(P2REN, BIT0); // pull enable
	CLR_BIT(P2OUT, BIT0); // pull down
    P2SEL0 = BIT0; //Input capture
	SET_BIT(P2DIR, BIT2); //output

	// Watchdog to start the readings
	WDTCTL = WDT_MDLY_32;                   // WDT 32ms (default, at F=1MHz) = 1.3ms (at 24MHz), SMCLK, interval timer
	SFRIE1 |= WDTIE;                        // Enable WDT interrupt
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
            break;

        /* Vector 10:  TBIFG -> Overflow do timer 0*/
        case TB1IV_TBIFG:
            CCR1_state = 2;
            CCR1_countB = 65535;
            CCR1_countA = 0;
            break;
        default:
            break;
    }
    if (CCR1_state==2){ //one measure concluded
        CCR1_state = 0;

        CLR_BIT(TB1CCTL1, CCIE);
        CLR_BIT(TB1CCTL2, CCIE);
        CLR_BIT(TB1CTL, TBIE | CCIE);

        CCR1_sum += CCR1_countB - CCR1_countA;
        measure_count++;

        if (measure_count>=16){
            last_value = CCR1_sum>>4; //for debug
            //check for collision
            if ((CCR1_sum>>4) < COLLISION_THRESHOLD){
                SET_BIT(PORT_OUT(LED1_PORT), LED1_BIT); // LED
                (*_collision_callback)();
            } else{
                CLR_BIT(PORT_OUT(LED1_PORT), LED1_BIT); // LED
            }
            measure_count = 0;
            CCR1_sum = 0;
        }
        timer_busy = 0;
    }

}

uint16_t sensor_ultrassonic_last_value(){
    return last_value;
}


/* ISR do watchdog:
 * executado toda a vez que o temporizador estoura, 1.3ms
 * O ultrassonico é trigado a cada 3.9ms
 * */
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector = WDT_VECTOR
__interrupt void watchdog_timer(void)
#elif defined(__GNUC__)
void __attribute__((interrupt(WDT_VECTOR))) watchdog_timer(void)
#else
#error Compiler not supported!
#endif
{
    if (!timer_busy){
        // Echo goes high for a period of time which will be equal to the time taken for the US wave to return back to the sensor
        // Enable Timer
        TB1CCR0 = _f*10;
        TB1CCTL0 |= CCIE;
        TB1CCTL1 |= CM_3 | CCIS_0 | CCIE | CAP | SCS;
        //TB1CCTL2 |= CM_3 | CCIS_0 | CCIE | CAP | SCS;
                                                        // Capture in both rising and falling edge,
                                                        // Use CCI0A,
                                                        // Synchronous capture,
                                                        // Enable capture mode,
                                                        // Enable capture interrupt
                                                        // Enable overflow interrupt

        TB1CTL |= TBSSEL_2 | MC_2 | TBCLR | TBIE;// | ID__4;
                                                        // Use SMCLK as clock source
                                                        // clear TB1R
                                                        // TBCCR0 interrupt enabled
                                                        // prescaller 4x
        SET_BIT(P2OUT, BIT2);
        timer_busy = 1;
    }
}

// Timer B1 interrupt service routine
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector = TIMER1_B0_VECTOR
__interrupt void Timer1_B0_ISR(void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(TIMER1_B0_VECTOR))) Timer1_B0_ISR (void)
#else
#error Compiler not supported!
#endif
{
    CLR_BIT(P2OUT, BIT2);
}


