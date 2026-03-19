import time
import serial
import matplotlib.pyplot as plt

def read_value(ser):
	while True:
		try:
			line = ser.readline().decode('ascii')
			v, t = map(float, line.split())
			return v, t
		except ValueError:
			continue
def main():
    ser = serial.Serial(port='COM5', baudrate=115200, timeout=0.0)
    if ser.is_open:
        print(f"Port {ser.name} opened")
    else:
        print(f"Port {ser.name} closed")
        return
    
    measure_temperature_C = []
    measure_voltage_V = []
    measure_ts = []
    
    #время старта измерений
    start_ts = time.time()
    ser.write("tm_start\n".encode('ascii'))
    try:
        # Бесконечный цикл сбора данных
        while True:
            ts = time.time() - start_ts
            ser.write("get_adc\n".encode('ascii'))
            voltage_V = read_value(ser)
            
            #температура
            ser.write("get_temp\n".encode('ascii'))
            temp_C = read_value(ser)
            
            measure_ts.append(ts)
            measure_voltage_V.append(voltage_V)
            measure_temperature_C.append(temp_C)
            
            print(f'{voltage_V:.3f} V - {temp_C:.1f}°C - {ts:.2f}s')
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nMeasurement stopped by user")
    finally:
        ser.close()
        print("Port closed")
        
        # После остановки можно построить графики
        if measure_ts:
            plt.figure(figsize=(12, 8))
            
            
            # напряжение
            plt.subplot(2, 1, 1)
            plt.plot(measure_ts, measure_voltage_V, 'b-')
            plt.ylabel('напряжение, В')
            plt.xlabel('время, с')
            plt.title('График зависимости напряжения от времени')
            
            #температуры
            plt.subplot(2, 1, 2)
            plt.plot(measure_ts, measure_temperature_C, 'r-')
            plt.xlabel('время, с')
            plt.ylabel('температура, C')
            plt.title('График зависимости температуры от времени')
            
            plt.tight_layout()
            plt.show()
            
          
if __name__ == "__main__":
    main()