import binascii

from .reader_base import ReaderBase


class LIRReader(ReaderBase):
    def __init__(self, port_code="COM4"):
        super().__init__(port_code)
        self.x_coord = None

    def read_LIR_hex(self, length=1):
        data = self.serial.read(length)
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

    def has_value(self):
        return not self.x_coord is None
