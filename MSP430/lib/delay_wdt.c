/***************************************************
 * Created by: Leonardo Benitez 
 * Date: 2020/03
 * License: MIT
****************************************************/

#include <msp430.h>
#include "delay_wdt.h"
#include "../lib/bits.h"

volatile uint16_t count = 0;
volatile uint8_t frequency = 1; //in MHz

void delay_ms_init(uint8_t f){
    frequency = f;
    WDTCTL = WDT_MDLY_32;                   // WDT 32ms (default, at F=1MHz), SMCLK, interval timer
    __bis_SR_register(GIE);
}

void delay_ms(uint16_t time){
    count = frequency*time/32;

    SFRIE1 |= WDTIE;                        // Enable WDT interrupt
    __bis_SR_register(LPM0_bits);           // Enter LPM0
    __no_operation();                       // For debug
}

/* ISR do watchdog: executado toda a vez que o temporizador estoura */
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector = WDT_VECTOR
__interrupt void watchdog_timer(void)
#elif defined(__GNUC__)
void __attribute__((interrupt(WDT_VECTOR))) watchdog_timer(void)
#else
#error Compiler not supported!
#endif
{
    count--;
    if (count<=0){
        __bic_SR_register_on_exit(LPM4_bits); //wake up
        CLR_BIT(SFRIE1, WDTIE);// desliga WDT interrupt
    }
}
