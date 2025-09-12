#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/ledc.h"
#include "driver/gpio.h"
#include "esp_err.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "esp_mac.h"
#include "sdkconfig.h"

#include "servo.h"
#include "pi_comms.h"
#include <string>
#include <iostream>




extern "C" void app_main(void) {
setup_ledc();
init_uart();

    while(1){
        std::string test_string = "Hello Pi 5, Im a better Microship loser";
        uart_write_bytes(UART_PORT, test_string.c_str(), std::size(test_string));
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
