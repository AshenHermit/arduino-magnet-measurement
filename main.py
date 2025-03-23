from lib import LIRReader, SensorReader, MeasurementSync, utils, LIRMock, SensorMock
from gui import gui
from pathlib import Path
import os


def main():
    CWD = Path(__file__).parent

    utils.print_ports()

    lir_reader = LIRReader("COM4")
    sensor_reader = SensorReader("COM3")

    ### это для теста многопоточности:
    # lir_reader = LIRMock()
    # sensor_reader = SensorMock()

    record_path = CWD / "measurements/record.txt"

    sensor_sync = MeasurementSync(lir_reader, sensor_reader, record_path)
    sensor_sync.start()


def run_gui():
    CWD = Path(os.getcwd())
    program = gui.GUIProgram(CWD / "settings.json", CWD / "measurements")
    program.build()


if __name__ == "__main__":
    print()
    run_gui()
