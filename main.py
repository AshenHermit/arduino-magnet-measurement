print()
import serial.tools.list_ports
import struct
import binascii
import asyncio
import json
from pathlib import Path
import time

def print_ports():
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        print(f"Порт: {port.device}")
        print(f"Описание: {port.description}")
        print(f"Производитель: {port.manufacturer}\n")

class SensorReader():
    def __init__(self):
        self.sensor_info = None
        self.arduino_serial = serial.Serial('COM3', 9600, timeout=1)

    def read_sensor(self):
        data = self.arduino_serial.readline()
        try:
            if data: return json.loads(data)
        except:
            pass
        return None
    
    def update(self):
        res = self.read_sensor()
        if not res is None:
            self.sensor_info = res

    def get_digital(self):
        if not self.sensor_info: return None
        return self.sensor_info["sensorDigital"]
    
    def get_analog(self):
        if not self.sensor_info: return None
        return self.sensor_info["sensorAnalog"]
    
    def has_value(self): return not self.sensor_info is None

class LIRReader():
    def __init__(self):
        self.sensor_info = None
        self.lir_serial = serial.Serial('COM4', 9600, timeout=1)
    
    def read_LIR_hex(self, length=1):
        data = self.lir_serial.read(length)
        return binascii.hexlify(data).decode()

    def convert_string_to_float(self, s):
        num = int(s)  # Преобразуем строку в целое число
        if num > 50000000:  # Если число больше 50000000, считаем его отрицательным
            num -= 100000000
        return num / 1000  # Делим на 10^6 для получения дробной части

    def read_x_coord(self):
        if self.read_LIR_hex(1) == "0a":
            xCoord = ""
            for i in range(4):
                xCoord = self.read_LIR_hex(1) + xCoord

            yCoord = ""
            for i in range(4):
                yCoord = self.read_LIR_hex(1) + yCoord

            if self.read_LIR_hex(1) == "0b":
                return self.convert_string_to_float(xCoord)
        return None
    
    def update(self):
        res = self.read_x_coord()
        if not res is None:
            self.x_coord = res

    def has_value(self): return not self.x_coord is None

lir_reader = LIRReader()
sensor_reader = SensorReader()

CWD = Path(__file__).parent
record_file = CWD / "record.txt"
record_file.write_text("")

start_time = time.time()

def loop():
    lir_reader.update()
    sensor_reader.update()

    if lir_reader.has_value() and sensor_reader.has_value():
        measure_time = time.time() - start_time
        record_text = f"{measure_time} : {lir_reader.x_coord} : {sensor_reader.get_digital()} : {sensor_reader.get_analog()}\n"

        with record_file.open("a") as record_file_buff:
            record_file_buff.write(record_text)

        print(record_text)

def main():
    while True:
        loop()

main()