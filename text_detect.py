import tkinter as tk
from PIL import ImageGrab
import keyboard
import pyperclip
from easyocr import Reader
import numpy as np
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')


class TextRecognizerApp:
    def __init__(self, languages=['ru', 'en'], hotkey='end', exit_key='esc'):
        """
        Инициализация приложения.

        :param languages: Языки для распознавания текста
        :param hotkey: Горячая клавиша для запуска распознавания
        :param exit_key: Горячая клавиша для выхода из программы
        """
        self.languages = languages
        self.hotkey = hotkey
        self.exit_key = exit_key
        self.reader = Reader(self.languages)

    def select_area(self):
        """
        Открывает окно для выделения области экрана.
        :return: Координаты выделенной области (x1, y1, x2, y2)
        """
        root = tk.Tk()
        root.attributes("-fullscreen", True)
        root.attributes("-alpha", 0.3)
        root.config(cursor="cross")

        canvas = tk.Canvas(root, bg="gray", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        start_x, start_y = None, None
        rect_id = None
        bbox = []

        def on_click(event):
            nonlocal start_x, start_y, rect_id
            start_x, start_y = event.x, event.y
            rect_id = canvas.create_rectangle(
                start_x, start_y, start_x, start_y,
                outline="red", width=2
            )

        def on_drag(event):
            nonlocal rect_id
            canvas.coords(rect_id, start_x, start_y, event.x, event.y)

        def on_release(event):
            nonlocal bbox
            bbox = [start_x, start_y, event.x, event.y]
            root.quit()

        canvas.bind("<Button-1>", on_click)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

        root.mainloop()
        root.destroy()

        if bbox:
            x1, y1, x2, y2 = bbox
            return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
        else:
            return None

    def recognize_and_copy_text(self):
        """
        Захватывает выделенную область, распознает текст и копирует его в буфер обмена.
        """
        logging.info("Ожидание выбора области...")
        bbox = self.select_area()

        if bbox:
            logging.info(f"Захваченная область: {bbox}")
            screenshot = ImageGrab.grab(bbox=bbox)
            screenshot_np = np.array(screenshot)
            logging.info("Распознавание текста...")

            result = self.reader.readtext(screenshot_np)
            recognized_text = "\n".join([detection[1] for detection in result])
            logging.info(f"Распознанный текст:\n{recognized_text}")

            pyperclip.copy(recognized_text)
            logging.info("Текст скопирован в буфер обмена!")
        else:
            logging.warning("Область не выбрана.")

    def run(self):
        """
        Запускает приложение и связывает горячие клавиши.
        """
        logging.info(f"Программа запущена. Нажмите '{self.hotkey}' для распознавания текста.")
        logging.info(f"Нажмите '{self.exit_key}' для выхода.")
        keyboard.add_hotkey(self.hotkey, self.recognize_and_copy_text)
        keyboard.wait(self.exit_key)
        logging.info("Программа завершена.")


if __name__ == "__main__":
    app = TextRecognizerApp()
    app.run()
