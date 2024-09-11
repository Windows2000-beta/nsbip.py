import tkinter as tk
import subprocess
import threading


class PingWindow:
    def __init__(self, ip):
        self.ip = ip
        self.root = tk.Toplevel()  # Создаем новое окно для каждого IP
        self.root.title(f"Ping Monitor - {self.ip}")
        self.root.geometry("200x200")
        self.root.resizable(True, True)  # Позволяем изменять размер окна

        self.canvas = tk.Canvas(self.root, width=200, height=200)
        self.canvas.pack(fill="both", expand=True)

        self.monitoring = True
        self.monitoring_thread = threading.Thread(target=self.monitor_ip)
        self.monitoring_thread.daemon = True  # Поток-демон, чтобы не блокировать закрытие программы
        self.monitoring_thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.monitoring = False  # Останавливаем мониторинг
        self.root.destroy()

    def monitor_ip(self):
        while self.monitoring:
            response = self.ping_device(self.ip)
            if response:
                self.update_window("green")
            else:
                self.update_window("red")
            self.root.after(5)  # Обновляем окно каждые 5 мс для мигания

    def ping_device(self, ip):
        try:
            # Команда пинга в зависимости от ОС
            command = ["ping", "-n", "1", "-w", "1000", ip]  # Windows
            response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return response.returncode == 0  # Успешный ответ от устройства
        except Exception as e:
            print(f"Ошибка пинга: {e}")
            return False

    def update_window(self, color):
        self.canvas.configure(bg=color)
        self.canvas.update_idletasks()


class PingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Monitor - Ввод IP")
        self.root.geometry("300x150")

        self.entry_label = tk.Label(root, text="Введите IP-адрес:")
        self.entry_label.pack(pady=10)

        self.ip_entry = tk.Entry(root, width=25)
        self.ip_entry.pack(pady=5)

        self.start_button = tk.Button(root, text="Начать мониторинг", command=self.start_monitoring)
        self.start_button.pack(pady=10)

    def start_monitoring(self):
        ip_address = self.ip_entry.get()
        if ip_address:
            PingWindow(ip_address)  # Создаем новое окно для каждого IP


def main():
    root = tk.Tk()
    app = PingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
    # da da da da