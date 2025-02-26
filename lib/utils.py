import serial.tools.list_ports

def print_ports():
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        print(f"Порт: {port.device}")
        print(f"Описание: {port.description}")
        print(f"Производитель: {port.manufacturer}\n")