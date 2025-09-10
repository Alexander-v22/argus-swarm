#include "driver/uart.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_mac.h"
#include "sdkconfig.h"

#include <cstring>

#define UART_RX_GPIO GPIO_NUM_16
#define UART_TX_GPIO GPIO_NUM_17
#define UART_PORT 1
#define UART_BUFFER 1024



void init_aurt () {
uart_config_t uart_config = {};
    uart_config.baud_rate = 115200;
    uart_config.data_bits = UART_DATA_8_BITS;
    uart_config.parity = UART_PARITY_DISABLE;
    uart_config.stop_bits = UART_STOP_BITS_1;
    uart_config.flow_ctrl = UART_HW_FLOWCTRL_CTS_RTS;
    uart_config.rx_flow_ctrl_thresh = 122;

}
