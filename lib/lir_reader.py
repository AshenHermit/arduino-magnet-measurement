import binascii

from .reader_base import ReaderBase


class LIRReader(ReaderBase):
    def __init__(self, port_code="COM4"):
        super().__init__(port_code)
        self.x_coord = None
        self.y_coord = None

    def read_hex_byte(self, length=1):
        data = self.serial.read(length)
        return binascii.hexlify(data).decode()

    def convert_str_uint_to_float(self, s):
        num = int(s)  # Преобразуем строку в целое число
        if num > 50000000:  # Если число больше 5*10^7, считаем его отрицательным
            num -= 100000000
        return num / 1000  # Делим на 10^3 для получения дробной части

    # Декодирование потока байтов в данные о позиции
    def read_coords(self):
        if self.read_hex_byte(1) == "0a":
            xCoord = ""
            for i in range(4):
                xCoord = self.read_hex_byte(1) + xCoord

            yCoord = ""
            for i in range(4):
                yCoord = self.read_hex_byte(1) + yCoord

            if self.read_hex_byte(1) == "0b":
                return [
                    self.convert_str_uint_to_float(xCoord),
                    self.convert_str_uint_to_float(yCoord),
                ]
        return None

    def update(self):
        coords = self.read_coords()
        if not coords is None:
            self.x_coord = coords[0]
            self.y_coord = coords[1]
