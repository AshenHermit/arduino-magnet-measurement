import serial


class ReaderBase:
    def __init__(self, port_code="COM3"):
        self.serial = serial.Serial(port_code, 9600, timeout=1)

    def update(self):
        pass

    def has_value(self):
        return False
