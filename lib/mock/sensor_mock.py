from .. import SensorReader
import time
import random


class SensorMock(SensorReader):
    def __init__(self, port_code="COM3"):
        self.sensor_info = None

    def update(self):
        time.sleep(3)
        self.sensor_info = {
            "sensorDigital": random.randint(0, 9),
            "sensorAnalog": random.randint(0, 9),
        }
