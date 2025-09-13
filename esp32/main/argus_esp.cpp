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
        read_data();
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
