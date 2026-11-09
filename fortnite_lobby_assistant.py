
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
import numpy as np
import pyautogui
import ctypes

pyautogui.FAILSAFE = True

class FortniteAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Fortnite Assistant")
        self.root.geometry("440x300")

        self.running = False
        self.paused = False
        self.template = None
        self.last_click = 0

        tk.Label(
            root, text="FORTNITE ASSISTANT",
            font=("Arial", 17, "bold")
        ).pack(pady=15)

        self.status = tk.Label(
            root, text="Ожидание",
            font=("Arial", 12)
        )
        self.status.pack(pady=10)

        tk.Button(
            root, text="Выбрать кнопку ИГРАТЬ",
            command=self.choose_template, width=30
        ).pack(pady=7)

        tk.Button(
            root, text="СТАРТ",
            command=self.start, width=30
        ).pack(pady=7)

        tk.Button(
            root, text="ПАУЗА (F7)",
            command=self.pause, width=30
        ).pack(pady=7)

        tk.Button(
            root, text="СТОП (F8)",
            command=self.stop, width=30
        ).pack(pady=7)

        self.info = tk.Label(root, text="Выбери изображение кнопки")
        self.info.pack(pady=10)

        threading.Thread(
            target=self.hotkeys, daemon=True
        ).start()

    def choose_template(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg")]
        )
        if path:
            self.template = cv2.imread(path)
            self.info.config(text="Шаблон загружен!")

    def start(self):
        if self.template is None:
            messagebox.showwarning(
                "Ошибка", "Сначала выбери изображение кнопки!"
            )
            return

        if not self.running:
            self.running = True
            self.paused = False
            threading.Thread(
                target=self.loop, daemon=True
            ).start()

    def pause(self):
        if self.running:
            self.paused = not self.paused
            self.status.config(
                text="Пауза" if self.paused else "Работает"
            )

    def stop(self):
        self.running = False
        self.paused = False
        self.status.config(text="Остановлено")

    def hotkeys(self):
        user32 = ctypes.windll.user32
        old7 = old8 = False

        while True:
            f7 = bool(user32.GetAsyncKeyState(0x76) & 0x8000)
            f8 = bool(user32.GetAsyncKeyState(0x77) & 0x8000)

            if f7 and not old7:
                self.root.after(0, self.pause)

            if f8 and not old8:
                self.root.after(0, self.stop)

            old7, old8 = f7, f8
            time.sleep(0.12)

    def loop(self):
        while self.running:
            if self.paused:
                time.sleep(0.3)
                continue

            try:
                screen = cv2.cvtColor(
                    np.array(pyautogui.screenshot()),
                    cv2.COLOR_RGB2BGR
                )

                h, w = self.template.shape[:2]

                if h <= screen.shape[0] and w <= screen.shape[1]:
                    result = cv2.matchTemplate(
                        screen, self.template,
                        cv2.TM_CCOEFF_NORMED
                    )

                    _, confidence, _, location = cv2.minMaxLoc(result)

                    if confidence >= 0.88:
                        if time.time() - self.last_click > 20:
                            x = location[0] + w // 2
                            y = location[1] + h // 2
                            pyautogui.click(x, y)
                            self.last_click = time.time()
                            self.root.after(
                                0, lambda: self.info.config(
                                    text="Кнопка Играть нажата"
                                )
                            )
                    else:
                        self.root.after(
                            0, lambda: self.info.config(
                                text="Ожидание кнопки Играть"
                            )
                        )

            except Exception as e:
                self.root.after(
                    0, lambda: self.info.config(text=str(e))
                )

            time.sleep(2)

root = tk.Tk()
app = FortniteAssistant(root)
root.mainloop()
