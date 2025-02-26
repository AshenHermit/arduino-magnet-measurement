# Arduino Magnet Measurement

### Необходимо
- Python 3.12.2+
- [драйвер для кабеля rs232-usb](https://vk.com/s/v1/doc/ZoalqLNy4OJpXTkGzqvfkLbH9Zzhycc9edHZp0W9i11MWciaY40)

### Установка зависимостей
```
pip install -r requirements.txt
```

### Подключение ЛИР
- *ЛИР* подключается к *USB* порту
- затем включается питание

### Подключение Ардуино
- *Ардуино* подключается к *USB* порту
- затем компилируется и загружается проект `./arduino-project/magnet-detector/magnet-detector.ino`

### Настройка
- если нужно сменить порты, то сменить их можно в `main.py`
- если нужно сменить имя файла `record.txt`, то сменить можно в `main.py`

### Запуск
```
python main.py
```

### Запись значений
- значения записываются в файл `./measurements/record.txt`

### Анализ значений
- для него есть ipython книжка `analysis.ipynb`