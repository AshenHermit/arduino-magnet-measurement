import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import asyncio
import serial.tools.list_ports
from pathlib import Path
import threading

from lib import MeasurementSync, LIRReader, LIRMock, SensorMock, SensorReader

# GUI частично сгенерирован gpt в связи отсутсвия желания
# тратить время на вуз который больше колечит людей чем делает из них специалистов


class GUIProgram:

    def __init__(self, _settings_file, mesurements_folder: Path):
        # Файл для сохранения настроек
        self.settings_file: Path = _settings_file
        self.measurements_folder = mesurements_folder
        self.settings = {}

        self.LIR_port = None
        self.arduino_port = None
        self.record_filename = None
        self.test_mode = None

        self.measure_recorder: MeasurementSync = None

        self.start_button: tk.Button = None

    def port_str_to_port(self, port_str: str):
        return port_str.split("-")[0]

    def save_settings(self):
        self.settings = {
            "lir_port": self.port_str_to_port(self.LIR_port.get()),
            "arduino_port": self.port_str_to_port(self.arduino_port.get()),
        }
        self.settings_file.write_text(json.dumps(self.settings), encoding="utf-8")
        messagebox.showinfo("Сохранение", "Настройки сохранены")

    def load_settings(self):
        try:
            settings_json = self.settings_file.read_text(encoding="utf-8")
            settings = json.loads(settings_json)
            self.LIR_port.set(settings.get("lir_port", ""))
            self.arduino_port.set(settings.get("arduino_port", ""))
        except:
            pass

    def start_program(self):
        lir_port = self.port_str_to_port(self.LIR_port.get())
        arduino_port = self.port_str_to_port(self.arduino_port.get())

        if lir_port and arduino_port:
            record_filename = self.measurements_folder / self.record_filename.get()
            if not record_filename.parent.exists():
                record_filename.parent.mkdir(parents=True, exist_ok=True)

            if self.test_mode.get() < 1:
                lir_reader = LIRReader(lir_port)
                sensor_reader = SensorReader(arduino_port)
            else:
                ### это для теста многопоточности:
                lir_reader = LIRMock()
                sensor_reader = SensorMock()

            self.measure_recorder = MeasurementSync(
                lir_reader, sensor_reader, record_filename
            )
            self.clear_log()
            self.measure_recorder.on_line_recorded = self.write_log_line

            self.start_button.config(text="Остановить", command=self.stop_program)
            self.measure_recorder.start()
        else:
            messagebox.showwarning("Ошибка", "Выберите оба порта перед запуском")

    def stop_program(self):
        if not self.measure_recorder is None:
            self.measure_recorder.stop()
            self.measure_recorder = None

        self.start_button.config(text="Запустить", command=self.start_program)

    def clear_log(self):
        self.log_box.delete(1.0, "end")

    def write_log_line(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    def build(self):
        # Список доступных портов (замени на реальные)
        ports = list(serial.tools.list_ports.comports())
        ports_names = [
            f"{port.device}-{port.description}-{port.manufacturer}" for port in ports
        ]

        # Создание окна
        root = tk.Tk()
        root.title("Arduino x ЛИР measurement (´｡• ᵕ •｡`)")
        root.geometry("500x500")

        self.LIR_port = tk.StringVar()
        self.arduino_port = tk.StringVar()
        self.record_filename = tk.StringVar(value="record.txt")
        self.test_mode = tk.IntVar()

        enabled_checkbutton = ttk.Checkbutton(text="test mode", variable=self.test_mode)
        enabled_checkbutton.pack(padx=6, pady=6, anchor=tk.NW)

        # Виджеты
        ttk.Label(root, text="Выберите порт установки ЛИР:").pack(pady=5)
        lir_port_menu = ttk.Combobox(
            root, textvariable=self.LIR_port, values=ports_names, width=50
        )
        lir_port_menu.pack()

        ttk.Label(root, text="Выберите порт Ардуино:").pack(pady=5)
        arduino_port_menu = ttk.Combobox(
            root, textvariable=self.arduino_port, values=ports_names, width=50
        )
        arduino_port_menu.pack()

        save_button = ttk.Button(
            root, text="Сохранить настройки", command=self.save_settings
        )
        save_button.pack(pady=5)

        ttk.Label(root, text="Введите имя файла для записи").pack(pady=5)
        ttk.Entry(root, textvariable=self.record_filename).pack(pady=1)

        ttk.Label(
            root,
            text=f"Записи сохраняются по пути",
        ).pack(pady=1)
        ttk.Label(
            root,
            text=f'"{self.measurements_folder.absolute().as_posix()}"',
        ).pack(pady=1)

        self.start_button = ttk.Button(
            root, text="Запустить", command=self.start_program
        )
        self.start_button.pack(pady=5)

        self.log_box = scrolledtext.ScrolledText(root, width=200, height=100)
        self.log_box.pack()

        # Загрузка сохраненных настроек
        self.load_settings()

        root.mainloop()
