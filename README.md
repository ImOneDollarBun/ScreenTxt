# Text Recognizer App

## Описание / Description
Приложение для выделения области на экране, распознавания текста (на русском и английском языках) и копирования результата в буфер обмена.

## Зависимости / Dependencies
- Python 3.8+
- EasyOCR
- Pillow
- Keyboard
- Pyperclip
- Numpy

## Установка / Installation
1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/ImOneDollarBun/ScreenTxt/text-recognizer.git
   cd text-recognizer
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt

## Использование / Usage
1. Запуск приложения:
    ```bash
   py text_recognizer.py

2. Использование:
   ```text
   Используйте клавишу "END" для распознавания текста

   
## Создание запускаемого файла
Для удобного запуска можно использовать `pyinstaller` для упаковки в `.exe`:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --noconsole text_detect.py

    
