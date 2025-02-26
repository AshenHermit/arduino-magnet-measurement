# Arduino Magnet Measurement

### Необходимо
- Python 3.12.2+

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

### Запуск
```
python main.py
```

### Запись значений
- значения записываются в файл `./measurements/record.txt`

### Анализ значений
- для него есть ipython книжка `analysis.ipynb`