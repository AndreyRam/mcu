#include "protocol-task.h"
#include <stdio.h>
#include <string.h>

static api_t* api = NULL; 
static int commands_count = 0; 

void protocol_task_init(api_t* device_api)
{
    // Сохраняем указатель на массив команд
    api = device_api;
    
    // Подсчитываем количество команд в массиве
    commands_count = 0;
    
    while (api[commands_count].command_name != NULL)
    {
        commands_count++;
    }
    
    printf("Protocol task initialized with %d commands\n", commands_count);
}

void protocol_task_handle(char* command_string)
{
    // Проверка на NULL
    if (!command_string)
    {
        // Строка команды еще не получена, просто выходим
        return;
    }
    
    // Логика обработки полученной строки. Делим ее на команду и аргументы
    char* command_name = command_string;  
    char* command_args = NULL;             
    
    // Ищем пробел в строке
    char* space_symbol = strchr(command_string, ' ');
    
    if (space_symbol)
    {
        // Если нашли пробел, разделяем строку
        *space_symbol = '\0';       
        command_args = space_symbol + 1;  
    }
    else
    {
        // Если пробела нет, значит аргументов нет
        command_args = "";
    }
    
    printf("Command: '%s', Args: '%s'\n", command_name, command_args);
    
    if (!api || commands_count == 0)
    {
        printf("Error: API not initialized or no commands registered\n");
        return;
    }
    
    // В цикле проходим по массиву команд и ищем совпадение имени команды
    for (int i = 0; i < commands_count; i++)
    {
        if (strcmp(command_name, api[i].command_name) == 0)
        {
            // Мы нашли команду, вызываем callback найденной команды
            api[i].command_callback(command_args);
            return;  // Выходим после успешного выполнения
        }
    }
    
    printf("Error: unknown command '%s'\n", command_name);
    printf("Type 'help' for list of available commands\n");
    
    return;
}