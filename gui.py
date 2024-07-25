import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import requests
import json

class ImageProcessorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.settings_file = 'settings.json'
        self.load_settings()

        self.title("Обробка Зображень")
        self.geometry("743x292")
        self.resizable(False, False)

        self.create_widgets()
        self.create_menu()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        if self.settings.get('check_for_updates', False):
            self.check_for_updates()

    def create_widgets(self):
        tk.Label(self, text="Папка зображень:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.source_folder_entry = tk.Entry(self, width=50)
        self.source_folder_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="Обрати...", command=self.select_source_folder).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self, text="Ширина полотна:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.canvas_width_entry = tk.Entry(self, width=10)
        self.canvas_width_entry.insert(0, "1035")
        self.canvas_width_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        tk.Label(self, text="Висота полотна:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.canvas_height_entry = tk.Entry(self, width=10)
        self.canvas_height_entry.insert(0, "1440")
        self.canvas_height_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        tk.Label(self, text="Відступ:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.padding_entry = tk.Entry(self, width=10)
        self.padding_entry.insert(0, "65")
        self.padding_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        tk.Button(self, text="Почати обробку", command=self.start_processing).grid(row=4, column=0, columnspan=3, pady=20)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W+tk.E)

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Налаштування", command=self.open_settings)
        menubar.add_cascade(label="Меню", menu=settings_menu)

    def open_settings(self):
        settings_dialog = tk.Toplevel(self)
        settings_dialog.title("Налаштування")
        settings_dialog.geometry("300x150")
        settings_dialog.resizable(False, False)

        check_var = tk.BooleanVar(value=self.settings.get('check_for_updates', False))

        check_button = tk.Checkbutton(settings_dialog, text="Перевіряти оновлення", variable=check_var)
        check_button.pack(pady=10)

        button_frame = tk.Frame(settings_dialog)
        button_frame.pack(pady=20)

        save_button = tk.Button(button_frame, text="Зберегти", command=lambda: self.save_settings(check_var.get(), settings_dialog))
        save_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Скасувати", command=settings_dialog.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def save_settings(self, check_for_updates, dialog):
        self.settings['check_for_updates'] = check_for_updates
        self.save_settings_to_file()
        dialog.destroy()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                'check_for_updates': False,
                'update_url': 'https://example.com/check_for_updates',
                'window_position': '200x200+100+100'
            }

    def save_settings_to_file(self):
        self.settings['window_position'] = self.geometry()
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

    def check_for_updates(self):
        update_url = self.settings.get('update_url', '')
        if update_url:
            response = requests.get(update_url)
            if response.status_code == 200:
                latest_version = response.json().get('latest_version')
                # Add logic to compare versions and update if needed

    def on_closing(self):
        self.save_settings_to_file()
        self.destroy()

    def select_source_folder(self):
        folder = filedialog.askdirectory()
        self.source_folder_entry.delete(0, tk.END)
        self.source_folder_entry.insert(0, folder)

    def start_processing(self):
        source_folder = self.source_folder_entry.get()
        canvas_width = int(self.canvas_width_entry.get())
        canvas_height = int(self.canvas_height_entry.get())
        padding = int(self.padding_entry.get())

        if not source_folder:
            messagebox.showerror("Помилка", "Будь ласка, оберіть папку зображень")
            return

        if canvas_width <= 0 or canvas_height <= 0 or padding < 0:
            messagebox.showerror("Помилка", "Неправильні розміри полотна або відступу")
            return

        self.process_images(source_folder, canvas_width, canvas_height, padding)

    def is_image_file(self, filename):
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
        return filename.lower().endswith(valid_extensions)

    def process_images(self, source_folder, canvas_width, canvas_height, padding):
        output_folder = os.path.join(source_folder, 'output')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        total_files = len([name for name in os.listdir(source_folder) if self.is_image_file(name)])
        processed_files = 0

        for filename in os.listdir(source_folder):
            if self.is_image_file(filename):
                file_path = os.path.join(source_folder, filename)
                if os.path.isfile(file_path):
                    try:
                        with Image.open(file_path) as img:
                            img_width, img_height = img.size
                            scale_factor = min((canvas_width - 2 * padding) / img_width, (canvas_height - 2 * padding) / img_height)
                            new_width = int(img_width * scale_factor)
                            new_height = int(img_height * scale_factor)
                            img_resized = img.resize((new_width, new_height), Image.LANCZOS)
                            new_image = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))
                            paste_x = (canvas_width - new_width) // 2
                            paste_y = (canvas_height - new_height) // 2
                            new_image.paste(img_resized, (paste_x, paste_y))
                            new_image.save(os.path.join(output_folder, filename))
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

                processed_files += 1
                self.progress_var.set((processed_files / total_files) * 100)
                self.progress_bar.update_idletasks()

        messagebox.showinfo("Успіх", "Зображення успішно оброблено!")

if __name__ == "__main__":
    app = ImageProcessorApp()
    app.mainloop()

