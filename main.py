from lib import LIRReader, SensorReader, MeasurementSync, utils, LIRMock, SensorMock
from pathlib import Path

CWD = Path(__file__).parent


def main():
    utils.print_ports()

    lir_reader = LIRReader("COM4")
    sensor_reader = SensorReader("COM3")

    ### это для теста многопоточности:
    # lir_reader = LIRMock()
    # sensor_reader = SensorMock()

    record_path = CWD / "measurements/record.txt"

    sensor_sync = MeasurementSync(lir_reader, sensor_reader, record_path)
    sensor_sync.start()


if __name__ == "__main__":
    print()
    main()
