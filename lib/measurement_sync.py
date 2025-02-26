import threading
from pathlib import Path
import time

from . import LIRReader, SensorReader


class MeasurementSync:
    def __init__(
        self,
        lir_reader: LIRReader,
        sensor_reader: SensorReader,
        record_filename: Path = "record.txt",
    ):
        self.lir_reader = lir_reader
        self.sensor_reader = sensor_reader

        self.record_file = record_filename
        self.record_file.write_text("")

        self.start_time = time.time()

        self.lir_lock = threading.Lock()
        self.sensor_lock = threading.Lock()

        self.lir_data = None
        self.sensor_data = None

        self.thread_lir = threading.Thread(target=self.read_lir, daemon=True)
        self.thread_sensor = threading.Thread(target=self.read_sensor, daemon=True)
        self.thread_loop = threading.Thread(target=self.loop, daemon=True)

    def read_lir(self):
        while True:
            self.lir_reader.update()
            with self.lir_lock:
                self.lir_data = self.lir_reader.x_coord

    def read_sensor(self):
        while True:
            self.sensor_reader.update()
            with self.sensor_lock:
                self.sensor_data = (
                    self.sensor_reader.get_digital(),
                    self.sensor_reader.get_analog(),
                )

    def loop(self):
        while True:
            with self.lir_lock:
                lir_snapshot = self.lir_data
            with self.sensor_lock:
                sensor_snapshot = self.sensor_data

            if lir_snapshot is not None and sensor_snapshot is not None:
                measure_time = time.time() - self.start_time
                record_text = f"{measure_time} : {lir_snapshot} : {sensor_snapshot[0]} : {sensor_snapshot[1]}\n"

                with self.record_file.open("a") as record_file_buff:
                    record_file_buff.write(record_text)

                print(record_text)
            time.sleep(0.01)

    def start(self):
        self.thread_lir.start()
        self.thread_sensor.start()
        self.thread_loop.start()
        self.thread_loop.join()  # Ждем завершения основного потока
