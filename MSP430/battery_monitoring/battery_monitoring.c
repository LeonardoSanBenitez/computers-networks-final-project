/*
 * battery_monitoring.c
 *
 *  Created on: 21 de ago de 2020
 *      Author: benitez
 */

#include "battery_monitoring.h"

volatile unsigned int ADC_Result[3];             // 12-bit ADC conversion result array
volatile unsigned char i;
void (*_death_callback)() = 0;

void battery_monitoring_init(uint8_t f, void (*death_callback)()){
    _death_callback = death_callback;
    i = 2;

    // Configure ADC A0~2 pins
    P1SEL0 |=  BIT0 + BIT1 + BIT2;
    P1SEL1 |=  BIT0 + BIT1 + BIT2;

    // Configure reference
    PMMCTL0_H = PMMPW_H;                                        // Unlock the PMM registers
    PMMCTL2 |= INTREFEN;                                        // Enable internal reference
    __delay_cycles(4000);                                        // Delay for reference settling

    // Configure ADC
    ADCCTL0 |= ADCSHT_2 | ADCON;                                // 16ADCclks, ADC ON
    ADCCTL1 |= ADCSHP  | ADCCONSEQ_3;                 // ADC clock MODCLK, sampling timer, software trig.,repeat sequence
    ADCCTL2 &= ~ADCRES;
    ADCCTL2 |= ADCRES_2;                                        // 12-bit conversion results
    ADCMCTL0 |= ADCINCH_2 | ADCSREF_0;                          // A0~2(EoS); Vref=3.3
    ADCIE |= ADCIE0;                                            // Enable ADC conv complete interrupt

    //timer
    TB0CCTL0 |= CCIE;                             // TBCCR0 interrupt enabled
    TB0CCR0 = (uint16_t)f*2000;                  // CCR on that value. T=2ms
    TB0CTL = TBSSEL__SMCLK | MC__UP;              // SMCLK, UP mode
}


uint8_t battery_monitoring_death_policy (){
    /* Calculo completo:
    float v_total = ADC_Result[1] * (3.3/4095) * (30/40) * (40/10); // batery 0 + batery 1, about 7V (before opamp)
    float v_bat0  = ADC_Result[2] * (3.3/4095) * (15/25) * (25/10); //tensão no ponto intermeriário, v_med
    float v_bat1 = v_total - v_bat0;
    if (v_bat0<3.1 || v_bat1<3.1){}
    */
    //TODO: debouncer

    if ((ADC_Result[2]<2564) || (ADC_Result[1]<2564)){
        return 1;
    } else {
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
            if(i == 0){
                i = 2;
                if (battery_monitoring_death_policy()){
                    (*_death_callback)();
                }
            } else{
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
    ADCCTL0 |= ADCENC | ADCSC;                               // Sampling and conversion start
}
