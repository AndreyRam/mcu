#include "pico/stdlib.h"
#include "stdio.h"
#include "stdlib.h"

#define DEVICE_NAME "my-pico-device"
#define DEVICE_VRSN "v0.0.1"

#include "stdio-task/stdio-task.h"
#include "protocol-task/protocol-task.h"
#include "led-task/led-task.h"

uint32_t global_variable = 0;
const uint32_t constant_variable = 42;


void version_callback(const char* args)
{
    (void)args;  
    printf("device name: '%s', firmware version: %s\n", DEVICE_NAME, DEVICE_VRSN);
}

void led_on_callback(const char* args)
{
    (void)args;
    led_task_state_set(LED_STATE_ON);
    printf("LED turned on\n");
}

void led_off_callback(const char* args)
{
    (void)args;
    led_task_state_set(LED_STATE_OFF);
    printf("LED turned off\n");
}

void led_blink_callback(const char* args)
{
    (void)args;
    led_task_state_set(LED_STATE_BLINK);
    printf("LED blinking started\n");
}

void led_blink_set_period_ms_callback(const char* args)
{
    uint period_ms = 0;
    sscanf(args, "%u", &period_ms);
    
    if (period_ms == 0)
    {
        printf("Error: period must be greater than 0\n");
        return;
    }
    
    led_task_set_blink_period_ms(period_ms);
    printf("LED blink period set to %u ms\n", period_ms);
}

api_t device_api[] =
{
    {"version", version_callback, "get device name and firmware version"},
    {"on", led_on_callback, "turn LED on"},
    {"off", led_off_callback, "turn LED off"},
    {"blink", led_blink_callback, "make LED blink"},
    {"set_period", led_blink_set_period_ms_callback, "set LED blink period in milliseconds"},
    {NULL, NULL, NULL},
};

int main()
{
    stdio_init_all();
    stdio_task_init();
    
    led_task_init();
    protocol_task_init(device_api);
    
    printf("System initialized. Available commands: version, on, off, blink, set_period\n");

    while (1)
    {
        char* command_string = stdio_task_handle();
        protocol_task_handle(command_string);
        led_task_handle();
    }   
}