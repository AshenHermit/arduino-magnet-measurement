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

        self.stop_signal = False

        self.on_line_recorded = None

    def read_lir(self):
        while not self.stop_signal:
            self.lir_reader.update()
            with self.lir_lock:
                self.lir_data = self.lir_reader.x_coord

    def read_sensor(self):
        while not self.stop_signal:
            self.sensor_reader.update()
            with self.sensor_lock:
                self.sensor_data = (
                    self.sensor_reader.get_digital(),
                    self.sensor_reader.get_analog(),
                )

    def iterate(self):
        with self.lir_lock:
            lir_snapshot = self.lir_data
        with self.sensor_lock:
            sensor_snapshot = self.sensor_data

        if (not lir_snapshot is None) and sensor_snapshot:
            measure_time = time.time() - self.start_time
            record_text = f"{measure_time} : {lir_snapshot} : {sensor_snapshot[0]} : {sensor_snapshot[1]}\n"

            with self.record_file.open("a") as record_file_buff:
                record_file_buff.write(record_text)

            if not self.on_line_recorded is None:
                self.on_line_recorded(record_text)

            return record_text

    def loop(self):
        while not self.stop_signal:
            self.iterate()

    def start(self):
        self.thread_lir.start()
        self.thread_sensor.start()
        self.thread_loop.start()

    def stop(self):
        self.stop_signal = True

    def join(self):
        self.thread_loop.join()  # Ждем завершения основного потока
