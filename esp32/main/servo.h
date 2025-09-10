#pragma once
#include <stdint.h>
#include "driver/ledc.h"
#include "driver/gpio.h"

#define SERVO_PAN_GPIO    GPIO_NUM_25
#define SERVO_TILT_GPIO   GPIO_NUM_26
#define SERVO_MAX_US      2500
#define SERVO_MIN_US      1200
#define SERVO_TIMER       LEDC_TIMER_0
#define SERVO_RES         LEDC_TIMER_16_BIT
#define SERVO_FREQ_HZ     50

void setup_ledc(void);
void servo_update(uint8_t angle);   // or change to int here and in .cpp if you prefer
