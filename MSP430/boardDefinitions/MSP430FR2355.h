//***************************************************************************************
//  MSP physical board connections
//  Author: Leonardo Benitez
//  Date: 2020-1
//***************************************************************************************


#ifndef __MSP430FR2355__
    #error "Wrong board, you dumb!"
#endif

#ifndef BOARD_MSP430FR2355
#define BOARD_MSP430FR2355

// Button1 (right)
#define BUTTON1_BIT  BIT3
#define BUTTON1_PORT P2


// Button2 (left)
#define BUTTON2_BIT  BIT1
#define BUTTON2_PORT P4

// LED1 (right)
#define LED1_BIT BIT6
#define LED1_PORT P6
//set as output: SET_BIT(PORT_DIR(LED1_PORT), LED1_BIT);
//complement: CPL_BIT(PORT_OUT(LED1_PORT), LED1_BIT);

// LED2 (left)
#define LED2_BIT BIT0
#define LED2_PORT P1


#endif /* BOARD_MSP430FR2355 */
