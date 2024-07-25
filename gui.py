import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image

def is_image_file(filename):
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
    return filename.lower().endswith(valid_extensions)

def process_images(source_folder, canvas_width, canvas_height, padding, progress_var, progress_bar):
    # Create output folder inside the source folder
    output_folder = os.path.join(source_folder, 'output')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the total number of files
    total_files = len([name for name in os.listdir(source_folder) if is_image_file(name)])
    processed_files = 0

    # Loop through all files in the source folder
    for filename in os.listdir(source_folder):
        if is_image_file(filename):
            file_path = os.path.join(source_folder, filename)
            if os.path.isfile(file_path):
                # Open an image file
                try:
                    with Image.open(file_path) as img:
                        # Get the size of the image
                        img_width, img_height = img.size

                        # Calculate the scaling factor to fit the image inside the canvas
                        scale_factor = min((canvas_width - 2 * padding) / img_width, (canvas_height - 2 * padding) / img_height)
                        new_width = int(img_width * scale_factor)
                        new_height = int(img_height * scale_factor)

                        # Resize the image with the calculated scale factor
                        img_resized = img.resize((new_width, new_height), Image.LANCZOS)

                        # Create a new image with white background
                        new_image = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))

                        # Calculate position to paste the resized image on the new canvas
                        paste_x = (canvas_width - new_width) // 2
                        paste_y = (canvas_height - new_height) // 2

                        # Paste the resized image onto the new canvas
                        new_image.paste(img_resized, (paste_x, paste_y))

                        # Save the new image
                        new_image.save(os.path.join(output_folder, filename))
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

            # Update progress bar
            processed_files += 1
            progress_var.set((processed_files / total_files) * 100)
            progress_bar.update_idletasks()

    messagebox.showinfo("Успіх", "Зображення успішно оброблено!")

def select_source_folder():
    folder = filedialog.askdirectory()
    source_folder_entry.delete(0, tk.END)
    source_folder_entry.insert(0, folder)

def start_processing():
    source_folder = source_folder_entry.get()
    canvas_width = int(canvas_width_entry.get())
    canvas_height = int(canvas_height_entry.get())
    padding = int(padding_entry.get())

    if not source_folder:
        messagebox.showerror("Помилка", "Будь ласка, оберіть папку зображень")
        return

    if canvas_width <= 0 or canvas_height <= 0 or padding < 0:
        messagebox.showerror("Помилка", "Неправильні розміри полотна або відступу")
        return

    # Start processing images with a progress bar
    process_images(source_folder, canvas_width, canvas_height, padding, progress_var, progress_bar)

# Set up the GUI
root = tk.Tk()
root.title("Обробка Зображень")

tk.Label(root, text="Папка зображень:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
source_folder_entry = tk.Entry(root, width=50)
source_folder_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Обрати...", command=select_source_folder).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Ширина полотна:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
canvas_width_entry = tk.Entry(root, width=10)
canvas_width_entry.insert(0, "1035")
canvas_width_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

tk.Label(root, text="Висота полотна:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
canvas_height_entry = tk.Entry(root, width=10)
canvas_height_entry.insert(0, "1440")
canvas_height_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

tk.Label(root, text="Відступ:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
padding_entry = tk.Entry(root, width=10)
padding_entry.insert(0, "65")
padding_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

tk.Button(root, text="Почати обробку", command=start_processing).grid(row=4, column=0, columnspan=3, pady=20)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W+tk.E)

root.mainloop()

