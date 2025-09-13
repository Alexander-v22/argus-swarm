extern "C" {
  #include "driver/uart.h"
  #include "driver/gpio.h"
  #include "esp_log.h"
  #include "sdkconfig.h"
}

#include <cstring>

#define UART_TX_GPIO GPIO_NUM_17
#define UART_RX_GPIO GPIO_NUM_16
#define UART_PORT UART_NUM_1 //#define UART_PORT 1 -> this will compile as an int
#define UART_BUFFER 1024


void init_uart (void);
void read_data (void);