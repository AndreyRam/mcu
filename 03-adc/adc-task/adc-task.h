#pragma once
#include <stdint.h>
#include <stdbool.h>  // Добавить для bool, если понадобится

void adc_task_init(void);
float adc_task_measure_voltage(void);
float adc_task_measure_temperature(void);

typedef enum {
    ADC_TASK_STATE_IDLE = 0,
    ADC_TASK_STATE_RUN = 1,
} adc_task_state_t;

void adc_task_handle(void);
void adc_task_set_state(adc_task_state_t state);
adc_task_state_t adc_task_get_state(void);  