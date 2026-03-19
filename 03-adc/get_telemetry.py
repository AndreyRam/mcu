import time
import serial
import matplotlib.pyplot as plt

def read_value(ser):
    """Читает строку с двумя числами (напряжение и температура)"""
    while True:
        try:
            line = ser.readline().decode('ascii').strip()
            if not line:
                continue
            v, t = map(float, line.split())
            return v, t
        except (ValueError, UnicodeDecodeError):
            continue

def main():
    ser = serial.Serial(port='COM6', baudrate=115200, timeout=1.0)
    
    if ser.is_open:
        print(f"Port {ser.name} opened")
    else:
        print(f"Port {ser.name} closed")
        return
    
    measure_temperature_C = []
    measure_voltage_V = []
    measure_ts = []
    
    # Очищаем входной буфер
    ser.reset_input_buffer()
    
    # Отправляем команду старта телеметрии
    ser.write("tm_start\n".encode('ascii'))
    print("Telemetry started")
    
    # Небольшая задержка для первой телеметрии
    time.sleep(0.1)
    
    # Время старта измерений
    start_ts = time.time()
    
    try:
        # Бесконечный цикл сбора данных
        while True:
            # Читаем напряжение и температуру одной строкой из телеметрии
            voltage_V, temp_C = read_value(ser)
            
            ts = time.time() - start_ts
            
            measure_ts.append(ts)
            measure_voltage_V.append(voltage_V)
            measure_temperature_C.append(temp_C)
            
            print(f'{ts:.2f}s: {voltage_V:.3f} V, {temp_C:.1f}°C')
            
            # Небольшая задержка для снижения нагрузки
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\nMeasurement stopped by user")
        
    finally:
        # Отправляем команду остановки телеметрии
        ser.write("tm_stop\n".encode('ascii'))
        print("Telemetry stopped")
        
        # Небольшая задержка для отправки команды
        time.sleep(0.1)
        
        ser.close()
        print("Port closed")
        
        # Построение графиков
        if measure_ts:
            plt.figure(figsize=(12, 8))
            
            # Напряжение
            plt.subplot(2, 1, 1)
            plt.plot(measure_ts, measure_voltage_V, 'b-', linewidth=1.5)
            plt.ylabel('напряжение, В')
            plt.xlabel('время, с')
            plt.title('График зависимости напряжения от времени')
            
            # Температура
            plt.subplot(2, 1, 2)
            plt.plot(measure_ts, measure_temperature_C, 'r-', linewidth=1.5)
            plt.xlabel('время, с')
            plt.ylabel('температура, C')
            plt.title('График зависимости температуры от времени')
            
            plt.tight_layout()
            plt.show()
            
           
if __name__ == "__main__":
    main()