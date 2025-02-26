from .. import LIRReader
import time
import random


class LIRMock(LIRReader):
    def __init__(self, port_code="COM3"):
        self.x_coord = None

    def update(self):
        time.sleep(1)
        self.x_coord = random.randint(10, 19)
