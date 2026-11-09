
import tkinter as tk
import time

class KeyboardTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Fortnite Assistant 2.0")
        self.root.geometry("460x440")
        self.root.resizable(False, False)

        self.pressed = set()
        self.running = True

        tk.Label(
            root,
            text="FORTNITE ASSISTANT 2.0",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        self.status = tk.Label(
            root, text="ТЕСТ КЛАВИАТУРЫ",
            font=("Arial", 12)
        )
        self.status.pack(pady=5)

        self.keys = tk.Label(
            root,
            text="W     A     S     D\n\nSPACE",
            font=("Arial", 23, "bold"),
            justify="center"
        )
        self.keys.pack(pady=20)

        tk.Label(
            root,
            text="Нажимай клавиши на клавиатуре",
            font=("Arial", 11)
        ).pack(pady=5)

        tk.Label(
            root,
            text="Длительность теста (секунды):"
        ).pack(pady=5)

        self.duration = tk.IntVar(value=5)

        tk.Scale(
            root,
            from_=1,
            to=15,
            orient="horizontal",
            variable=self.duration,
            length=260
        ).pack()

        tk.Button(
            root,
            text="НАЧАТЬ ТЕСТ",
            width=25,
            command=self.start_test
        ).pack(pady=8)

        tk.Button(
            root,
            text="СТОП",
            width=25,
            command=self.stop_test
        ).pack(pady=5)

        self.result = tk.Label(
            root, text="Ожидание",
            font=("Arial", 11)
        )
        self.result.pack(pady=12)

        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.root.focus_force()

    def key_down(self, event):
        key = event.keysym.upper()
        self.pressed.add(key)
        self.update_keys()

    def key_up(self, event):
        key = event.keysym.upper()
        self.pressed.discard(key)
        self.update_keys()

    def update_keys(self):
        names = ["W", "A", "S", "D", "SPACE"]
        active = [
            key for key in names
            if key in self.pressed
            or (key == "SPACE" and "SPACE" in self.pressed)
        ]

        self.keys.config(
            text="   ".join(active) if active else
            "W     A     S     D\n\nSPACE"
        )

    def start_test(self):
        self.running = True
        self.status.config(text="ТЕСТ АКТИВЕН")
        self.result.config(
            text=f"Длительность: {self.duration.get()} сек."
        )
        self.root.after(
            self.duration.get() * 1000,
            self.finish_test
        )

    def finish_test(self):
        if self.running:
            self.status.config(text="ТЕСТ ЗАВЕРШЁН")
            self.result.config(text="Проверка окончена")

    def stop_test(self):
        self.running = False
        self.status.config(text="ОСТАНОВЛЕНО")
        self.result.config(text="Тест остановлен")

root = tk.Tk()
app = KeyboardTester(root)
root.mainloop()
