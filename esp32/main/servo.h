#pragma once
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define SERVO_PAN_GPIO GPIO_NUM_25
#define SERVO_TILT_GPIO GPIO_NUM_26

void setup_ledc(void);
void servo_update(uint8_t deg_pan, uint8_t deg_tilt);

#ifdef __cplusplus
}
#endif
