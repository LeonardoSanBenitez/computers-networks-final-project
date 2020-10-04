/*
 * battery_monitoring.c
 *
 *  Created on: 21 de ago de 2020
 *      Author: benitez
 */

#include "battery_monitoring.h"

void (*_death_callback)() = 0;
void battery_monitoring_init(uint8_t f, void (*death_callback)()){
    _death_callback = death_callback;

    TB0CCTL0 |= CCIE;                             // TBCCR0 interrupt enabled
    TB0CCR0 = (uint16_t)24*2000;                  // CCR on that value. T=2ms
    TB0CTL = TBSSEL__SMCLK | MC__UP;              // SMCLK, UP mode

    // Configure ADC A0~2 pins
    P1SEL0 |=  BIT0 + BIT1 + BIT2;
    P1SEL1 |=  BIT0 + BIT1 + BIT2;

    // Configure ADC
    ADCCTL0 |= ADCSHT_2 | ADCMSC | ADCON;                       // 16ADCclks, MSC, ADC ON
    ADCCTL1 |= ADCSHP | ADCCONSEQ_1 | ADCSSEL_1;                // ADC clock ACLK, sampling timer, s/w trig.,single sequence
    ADCCTL2 &= ~ADCRES;                                         // clear ADCRES in ADCCTL
    ADCCTL2 |= ADCRES_2;                                        // 12-bit conversion results
    ADCMCTL0 |= ADCINCH_2 | ADCSREF_0;                          // A0~2(EoS); reference internal (3.3)
    ADCIE |= ADCIE0;                                            // Enable ADC conv complete interrupt
    __delay_cycles(400);                                        // Delay for reference settling
}

uint8_t battery_monitoring_death_policy (){
    // Referência de 3.3V
    // V = 3.3*adc[n]/4095

    // v_total = ADC_Result[1]*10/30 // batery 0 + batery 1, about 7V (before opamp)
    // v_bat0 = 10/15*ADC_Result[2] //tensão no ponto intermeriário, v_med
    // v_bat1 = v_total - v_bat0
    //TODO: esses calculos acima estão certos?
    //TODO: considerar algum tipo de "debouncer"
    if (ADC_Result[1]<3846 || ADC_Result[2]<3846){
        return 1;
    } else {
        i = 2;
        return 0;
    }
}


// ADC interrupt service routine
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector=ADC_VECTOR
__interrupt void ADC_ISR(void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(ADC_VECTOR))) ADC_ISR (void)
#else
#error Compiler not supported!
#endif
{
    switch(__even_in_range(ADCIV,ADCIV_ADCIFG))
    {
        case ADCIV_NONE:
            break;
        case ADCIV_ADCOVIFG:
            break;
        case ADCIV_ADCTOVIFG:
            break;
        case ADCIV_ADCHIIFG:
            break;
        case ADCIV_ADCLOIFG:
            break;
        case ADCIV_ADCINIFG:
            break;
        case ADCIV_ADCIFG:
            ADC_Result[i] = ADCMEM0;
            if(i==0 && battery_monitoring_death_policy()) {
                (*_death_callback)();
            } else {
                i--;
            }
            break;
        default:
            break;
    }
}



/* Timer0_B0 interrupt service routine
 * Período: 2ms
 * Utilizado para trigar o ADC
 * */
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector = TIMER0_B0_VECTOR
__interrupt void Timer0_B0_ISR (void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(TIMER0_B0_VECTOR))) Timer0_B0_ISR (void)
#else
#error Compiler not supported!
#endif
{
    while(ADCCTL1 & ADCBUSY);                                // Wait if ADC core is active
    ADCCTL0 |= ADCENC | ADCSC;                               // Sampling and conversion start
}





