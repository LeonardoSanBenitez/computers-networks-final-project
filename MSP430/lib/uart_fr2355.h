/*
 * uart.h
 *
 *  Created on: Jun 4, 2020
 *      Author: Renan Augusto Starke
 *      Instituto Federal de Santa Catarina
 */

#ifndef LIB_UART_FR2355_H_
#define LIB_UART_FR2355_H_

#include <stdint.h>

#define CLOCK_24MHz
#define UART_ACK "ACK"
#define UART_NACK "NACK"

void init_uart();
void uart_send_package(uint8_t *data, uint8_t size);
void uart_receive_package(uint8_t *data, uint8_t size);

#endif /* LIB_UART_FR2355_H_ */
