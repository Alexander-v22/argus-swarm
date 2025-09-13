extern "C" {
  #include "driver/uart.h"
  #include "driver/gpio.h"
  #include "esp_log.h"
  #include "sdkconfig.h"
}

#include <cstring>
#include <vector>

#define UART_TX_GPIO GPIO_NUM_17
#define UART_RX_GPIO GPIO_NUM_16
#define UART_PORT UART_NUM_1 //#define UART_PORT 1 -> this will compile as an int
#define UART_BUFFER 1024
const static char* TAG = "UART";


void init_uart (void) {
    uart_config_t uart_config = {};
        uart_config.baud_rate = 115200;
        uart_config.data_bits = UART_DATA_8_BITS;
        uart_config.parity = UART_PARITY_DISABLE;
        uart_config.stop_bits = UART_STOP_BITS_1;
        uart_config.rx_flow_ctrl_thresh = 122;
        uart_config.flow_ctrl = UART_HW_FLOWCTRL_DISABLE;


    // Confiugre UART parameters 
    uart_param_config(UART_PORT, &uart_config);

    // Configuring pins. The last two can be replaced with 18, 19 for RTS , CTS
    ESP_ERROR_CHECK(uart_set_pin(UART_PORT, UART_TX_GPIO, UART_RX_GPIO, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));

    // Install UART driver using an event queue here(need to "wake up when new data arrives")
    ESP_ERROR_CHECK(uart_driver_install(UART_PORT, UART_BUFFER, UART_BUFFER, 0, nullptr,0));
    
    ESP_LOGI(TAG, "ESP32 UART configured");
}

void read_data(void){

  std::vector<uint8_t>rx_buf(UART_BUFFER);
  int len = uart_read_bytes(UART_PORT, rx_buf.data(), rx_buf.size(), pdMS_TO_TICKS(20));
  ESP_LOGW(TAG, "%d", len);

  if(len > 0 ) {

    if (len < (int)rx_buf.size()) rx_buf[len] = '\0';
    ESP_LOGI(TAG, "Pi said (%d): %s", len, (char*)rx_buf.data());  }
}