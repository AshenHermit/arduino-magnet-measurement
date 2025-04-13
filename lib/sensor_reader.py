import json
from .reader_base import ReaderBase


class SensorReader(ReaderBase):
    def __init__(self, port_code="COM3"):
        super().__init__(port_code)
        self.sensor_info = None

    def read_sensor(self):
        data = self.serial.readline()
        try:
            if data:
                return json.loads(data)
        except:
            pass
        return None

    def update(self):
        res = self.read_sensor()
        if not res is None:
            self.sensor_info = res

    def get_digital(self):
        if not self.sensor_info:
            return None
        return self.sensor_info["sensorDigital"]

    def get_analog(self):
        if not self.sensor_info:
            return None
        return self.sensor_info["sensorAnalog"]
