import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import shutil
import os
import zipfile
import base64

# 定义语言字典
LANGUAGES = {
    "中文": {
        "title": "字体资源包创建工具",
        "font_label": "选择字体文件:",
        "font_browse": "浏览",
        "icon_label": "选择图标文件:",
        "icon_browse": "浏览",
        "desc_label": "输入描述:",
        "desc_preview": "预览描述",
        "output_folder_label": "选择输出文件夹:",
        "output_folder_browse": "浏览",
        "zip_name_label": "输入压缩包名称:",
        "output_format_label": "选择输出格式:",
        "create_button": "创建资源包",
        "description_default": "自定义字体包！φ(゜▽゜*)♪",
        "error_font": "未选择字体文件，请选择字体文件。",
        "error_output_folder": "未选择输出文件夹，请选择输出文件夹。",
        "error_zip_name": "请输入压缩包名称。",
        "complete_folder": "字体资源包创建成功，输出为文件夹: {0}。",
        "complete_zip": "字体资源包创建成功，文件名为 {0}。",
        "preview_title": "描述和图片预览",
        "error_image": "无法加载图片: {0}",
        "language": "语言",
        "language_chinese": "中文",
        "language_english": "英文",
        "version_label": "选择游戏版本:",
        "output_format_folder": "文件夹",
        "output_format_zip": "ZIP",
        "left_shift_label": "左侧偏移:",
        "bottom_shift_label": "下侧偏移:",
        "font_size_label": "字体大小:",
        "resolution_label": "分辨率:"
    },
    "英文": {
        "title": "Font Resource Pack Creator",
        "font_label": "Select Font File:",
        "font_browse": "Browse",
        "icon_label": "Select Icon File:",
        "icon_browse": "Browse",
        "desc_label": "Enter Description:",
        "desc_preview": "Preview Description",
        "output_folder_label": "Select Output Folder:",
        "output_folder_browse": "Browse",
        "zip_name_label": "Enter Zip Package Name:",
        "output_format_label": "Select Output Format:",
        "create_button": "Create Resource Pack",
        "description_default": "Custom Font Pack!",
        "error_font": "No font file selected. Please select a font file.",
        "error_output_folder": "No output folder selected. Please select an output folder.",
        "error_zip_name": "Please enter the zip package name.",
        "complete_folder": "The font resource pack was created successfully. Output as folder: {0}.",
        "complete_zip": "The font resource pack was created successfully. File name: {0}.",
        "preview_title": "Description and Image Preview",
        "error_image": "Failed to load image: {0}",
        "language": "Language",
        "language_chinese": "Chinese",
        "language_english": "English",
        "version_label": "Select Game Version:",
        "output_format_folder": "Folder",
        "output_format_zip": "ZIP",
        "left_shift_label": "Left Shift:",
        "bottom_shift_label": "Bottom Shift:",
        "font_size_label": "Font Size:",
        "resolution_label": "Resolution:"
    }
}

# 版本与pack_format映射
VERSION_FORMAT_MAP = {
    "1.20.2 ~ 1.21": 18,
    "1.20 ~ 1.20.1": 15,
    "1.19.4": 13,
    "1.19.3": 12,
    "1.19~1.19.2": 9,
    "1.18 ~ 1.18.2": 8,
    "1.17~1.17.1": 7,
    "1.16.2 ~ 1.16.5": 6,
    "1.15 ~ 1.16.1": 5,
    "1.13 ~ 1.14.4": 4
}

current_language = "英文"  # 默认语言设置为英文


def select_font_file():
    file_path = filedialog.askopenfilename(filetypes=[("Font files", "*.ttf;*.otf")])
    if file_path:
        font_entry.delete(0, tk.END)
        font_entry.insert(0, file_path)


def select_icon_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    if file_path:
        icon_entry.delete(0, tk.END)
        icon_entry.insert(0, file_path)


def preview_description():
    description = desc_entry.get()
    icon_path = icon_entry.get()

    preview_window = tk.Toplevel(root)
    preview_window.title(LANGUAGES[current_language]["preview_title"])

    # 显示描述
    desc_label = tk.Label(preview_window, text=f"{LANGUAGES[current_language]['desc_label']}: {description}")
    desc_label.pack(pady=10)

    # 显示图片
    if icon_path:
        try:
            img = Image.open(icon_path)
            img = img.resize((200, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(preview_window, image=photo)
            img_label.image = photo
            img_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror(LANGUAGES[current_language]["error_image"].format(str(e)),
                                 LANGUAGES[current_language]["error_image"].format(str(e)))
    else:
        base64_image = "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TxSItDnYQKZihOtlFRRxLFYtgobQVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4BQqvGVLMvDqiaZWSSCTFfWBUHXhGAHyGMISIxU09lF3PwHF/38PH1LsazvM/9OUJK0WSATySOM92wiDeIZzctnfM+cZhVJIX4nHjSoAsSP3JddvmNc9lhgWeGjVxmnjhMLJZ7WO5hVjFU4hniqKJqlC/kXVY4b3FWaw3WuSd/YbCorWS5TjOCJJaQQhoiZDRQRQ0WYrRqpJjI0H7Cwz/q+NPkkslVBSPHAupQITl+8D/43a1Zmp5yk4IJoP/Ftj/GgYFdoN207e9j226fAP5n4Err+ustYO6T9GZXix4BQ9vAxXVXk/eAyx1g5EmXDMmR/DSFUgl4P6NvKgDDt8DgmttbZx+nD0COulq+AQ4OgYkyZa97vDvQ29u/Zzr9/QCNB3Kxtb/9yQAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAAuIwAALiMBeKU/dgAAAAd0SU1FB+gIAw0iKI7ZqukAAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAB10lEQVR42u3d7amCUBzA4b/2QoO0QF8aIKgPQfs0QCsJUTs0QdAeCcc7wH3jmN26+jzgp7Rjh58pElZERBMMVmkKBIAAEAACQAAIAAEgAASAABAAAkAACAABIAAEgAAQAAJAAPxz45yVj8djrFarXk9ISilms9nD75M7V12N+9QAyrKMyWTS6wDquu7mqzVzrroa1ykAASAABIAAEAACQAAIAAHwWdat4Mvl8rQdWa/XWevfbre4Xq+d70dKaXARNO+w5KqqqnmXff9qOZ1OWZ/nfr+/ZD+dAlwDIAAEgAAQAAJAAAzH2BR873A4xGKxaLXtfD7POxLLMqqqajVWSil2u50AurZcLrNvUbc1Go1iu9222vaRXxQ7BbgGQAAIAAEgAASAABAAAkAACGDINptNFEXRajmfz1lj1XXdeqzpdCoABIAAEAACQAAIAAEgAASAABAAAkAACAABIAAEgAAQgAAQAAJAAAgAASAABIAAEAACoN88K/hdjkQPix42D4vGNQACwEVgP/z2P8t/9UcUAniR/X7/4+tN0zgFIAAEgAAQAALgBYqIaEyDbwAEgAAQAAJAAAgAASAABIAAEAACQAAIAAEgAASAABAAAkAACAAB8P98AHnmEbJ9AFQHAAAAAElFTkSuQmCC"
        # 填充 Base64 字符串
        while len(base64_image) % 4 != 0:
            base64_image += "="
        img_data = base64.b64decode(base64_image)
        with open("temp_icon.png", "wb") as f:
            f.write(img_data)
        img = Image.open("temp_icon.png")
        img = img.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(preview_window, image=photo)
        img_label.image = photo
        img_label.pack(pady=10)
        os.remove("temp_icon.png")


def update_progress(progress):
    progress_bar['value'] = progress
    root.update_idletasks()


def select_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder)


def create_pack():
    font_path = font_entry.get()
    icon_path = icon_entry.get()
    description = desc_entry.get()
    output_folder = output_folder_entry.get()
    zip_name = zip_name_entry.get()
    output_format = output_format_var.get()
    selected_version = version_var.get()
    left_shift = int(left_shift_entry.get())
    bottom_shift = int(bottom_shift_entry.get())
    font_size = int(font_size_entry.get())
    oversample = int(resolution_entry.get())

    if not font_path:
        messagebox.showerror(LANGUAGES[current_language]["error_font"], LANGUAGES[current_language]["error_font"])
        return
    if not output_folder:
        messagebox.showerror(LANGUAGES[current_language]["error_output_folder"],
                             LANGUAGES[current_language]["error_output_folder"])
        return
    if not zip_name:
        messagebox.showerror(LANGUAGES[current_language]["error_zip_name"], LANGUAGES[current_language]["error_zip_name"])
        return

    # 使用用户主目录创建临时文件夹
    user_home = os.path.expanduser("~")
    temp_dir = os.path.join(user_home, "temp_pack")
    os.makedirs(temp_dir, exist_ok=True)
    update_progress(10)

    # 创建 assets 文件夹
    assets_dir = os.path.join(temp_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    print(f"创建 assets 文件夹: {assets_dir}")
    update_progress(20)

    # 创建 minecraft 文件夹
    minecraft_dir = os.path.join(assets_dir, "minecraft")
    os.makedirs(minecraft_dir, exist_ok=True)
    print(f"创建 minecraft 文件夹: {minecraft_dir}")
    update_progress(30)

    # 创建 font 文件夹
    font_dir = os.path.join(minecraft_dir, "font")
    os.makedirs(font_dir, exist_ok=True)
    print(f"创建 font 文件夹: {font_dir}")
    update_progress(40)

    # 复制字体文件并重命名为 custom
    font_extension = os.path.splitext(font_path)[1]
    custom_font_path = os.path.join(font_dir, f"custom{font_extension}")
    shutil.copy2(font_path, custom_font_path)
    print(f"复制字体文件到: {custom_font_path}")
    update_progress(50)

    # 创建 default.json 文件
    default_json_path = os.path.join(font_dir, "default.json")
    default_json_content = f"""{{
        "providers": [
            {{
                "type": "ttf",
                "file": "minecraft:custom{font_extension}",
                "shift": [
                    {left_shift},
                    {bottom_shift}
                ],
                "size": {font_size},
                "oversample": {oversample}
            }}
        ]
    }}"""
    with open(default_json_path, "w", encoding="utf - 8") as f:
        f.write(default_json_content)
    print(f"创建 default.json 文件: {default_json_path}")
    update_progress(60)

    # 处理图标
    icon_extension = ".png"
    if icon_path:
        pack_icon_path = os.path.join(temp_dir, f"pack{icon_extension}")
        shutil.copy2(icon_path, pack_icon_path)
        print(f"复制图标文件到: {pack_icon_path}")
    else:
        base64_image = "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TxSItDnYQKZihOtlFRRxLFYtgobQVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4BQqvGVLMvDqiaZWSSCTFfWBUHXhGAHyGMISIxU09lF3PwHF/38PH1LsazvM/9OUJK0WSATySOM92wiDeIZzctnfM+cZhVJIX4nHjSoAsSP3JddvmNc9lhgWeGjVxmnjhMLJZ7WO5hVjFU4hniqKJqlC/kXVY4b3FWaw3WuSd/YbCorWS5TjOCJJaQQhoiZDRQRQ0WYrRqpJjI0H7Cwz/q+NPkkslVBSPHAupQITl+8D/43a1Zmp5yk4IJoP/Ftj/GgYFdoN207e9j226fAP5n4Err+ustYO6T9GZXix4BQ9vAxXVXk/eAyx1g5EmXDMmR/DSFUgl4P6NvKgDDt8DgmttbZx+nD0COulq+AQ4OgYkyZa97vDvQ29u/Zzr9/QCNB3Kxtb/9yQAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAAuIwAALiMBeKU/dgAAAAd0SU1FB+gIAw0iKI7ZqukAAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAB10lEQVR42u3d7amCUBzA4b/2QoO0QF8aIKgPQfs0QCsJUTs0QdAeCcc7wH3jmN26+jzgp7Rjh58pElZERBMMVmkKBIAAEAACQAAIAAEgAASAABAAAkAACAABIAAEgAAQAAJAAPxz45yVj8djrFarXk9ISilms9nD75M7V12N+9QAyrKMyWTS6wDquu7mqzVzrroa1ykAASAABIAAEAACQAAIAAHwWdat4Mvl8rQdWa/XWevfbre4Xq+d70dKaXARNO+w5KqqqnmXff9qOZ1OWZ/nfr+/ZD+dAlwDIAAEgAAQAAJAAAzH2BR873A4xGKxaLXtfD7POxLLMqqqajVWSil2u50AurZcLrNvUbc1Go1iu9222vaRXxQ7BbgGQAAIAAEgAASAABAAAkAACGDINptNFEXRajmfz1lj1XXdeqzpdCoABIAAEAACQAAIAAEgAASAABAAAkAACAABIAAEgAAQgAAQAAJAAAgAASAABIAAEAACoN88K/hdjkQPix42D4vGNQACwEVgP/z2P8t/9UcUAniR/X7/4+tN0zgFIAAEgAAQAALgBYqIaEyDbwAEgAAQAAJAAAgAASAABIAAEAACQAAIAAEgAASAABAAAkAACAAB8P98AHnmEbJ9AFQHAAAAAElFTkSuQmCC"
        # 填充 Base64 字符串
        while len(base64_image) % 4 != 0:
            base64_image += "="
        img_data = base64.b64decode(base64_image)
        pack_icon_path = os.path.join(temp_dir, f"pack{icon_extension}")
        with open(pack_icon_path, 'wb') as f:
            f.write(img_data)
        print(f"使用默认图标并保存到: {pack_icon_path}")
    update_progress(70)

    # 创建 pack.mcmeta 文件
    mcmeta_path = os.path.join(temp_dir, "pack.mcmeta")
    pack_format = VERSION_FORMAT_MAP.get(selected_version, 4)  # 默认值为 4
    mcmeta_content = f"""{{
        "pack": {{
            "pack_format": {pack_format},
            "supported_formats": {{
                "min_inclusive": {pack_format},
                "max_inclusive": {pack_format}
            }},
            "description": "{description}"
        }}
    }}"""
    with open(mcmeta_path, "w", encoding="utf - 8") as f:
        f.write(mcmeta_content)
    print(f"创建 pack.mcmeta 文件: {mcmeta_path}")
    update_progress(80)

    final_output_path = os.path.join(output_folder, zip_name)
    if output_format == LANGUAGES[current_language]["output_format_folder"]:
        shutil.copytree(temp_dir, final_output_path, dirs_exist_ok=True)
        print(f"输出文件夹: {final_output_path}")
    else:
        if not zip_name.endswith('.zip'):
            zip_name += '.zip'
        zip_file_path = os.path.join(output_folder, zip_name)
        with zipfile.ZipFile(zip_file_path, "w") as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, temp_dir))
        print(f"创建压缩包: {zip_file_path}")

    # 删除临时文件夹
    shutil.rmtree(temp_dir)
    print(f"删除临时文件夹: {temp_dir}")
    update_progress(100)

    if output_format == LANGUAGES[current_language]["output_format_folder"]:
        messagebox.showinfo(LANGUAGES[current_language]["create_button"],
                            LANGUAGES[current_language]["complete_folder"].format(final_output_path))
    else:
        messagebox.showinfo(LANGUAGES[current_language]["create_button"],
                            LANGUAGES[current_language]["complete_zip"].format(zip_file_path))


def change_language(*args):
    global current_language
    current_language = language_var.get()
    # 更新界面文本
    root.title(LANGUAGES[current_language]["title"])
    font_label.config(text=LANGUAGES[current_language]["font_label"])
    font_browse_button.config(text=LANGUAGES[current_language]["font_browse"])
    icon_label.config(text=LANGUAGES[current_language]["icon_label"])
    icon_browse_button.config(text=LANGUAGES[current_language]["icon_browse"])
    desc_label.config(text=LANGUAGES[current_language]["desc_label"])
    desc_preview_button.config(text=LANGUAGES[current_language]["desc_preview"])
    output_folder_label.config(text=LANGUAGES[current_language]["output_folder_label"])
    output_folder_browse_button.config(text=LANGUAGES[current_language]["output_folder_browse"])
    zip_name_label.config(text=LANGUAGES[current_language]["zip_name_label"])
    output_format_label.config(text=LANGUAGES[current_language]["output_format_label"])
    create_button.config(text=LANGUAGES[current_language]["create_button"])
    language_label.config(text=LANGUAGES[current_language]["language"])
    version_label.config(text=LANGUAGES[current_language]["version_label"])
    left_shift_label.config(text=LANGUAGES[current_language]["left_shift_label"])
    bottom_shift_label.config(text=LANGUAGES[current_language]["bottom_shift_label"])
    font_size_label.config(text=LANGUAGES[current_language]["font_size_label"])
    resolution_label.config(text=LANGUAGES[current_language]["resolution_label"])


# 创建主窗口
root = tk.Tk()
root.title(LANGUAGES[current_language]["title"])

# 字体文件选择
font_label = tk.Label(root, text=LANGUAGES[current_language]["font_label"])
font_label.grid(row=0, column=0, padx=10, pady=5)
font_entry = tk.Entry(root, width=50)
font_entry.grid(row=0, column=1, padx=10, pady=5)
font_browse_button = tk.Button(root, text=LANGUAGES[current_language]["font_browse"], command=select_font_file)
font_browse_button.grid(row=0, column=2, padx=10, pady=5)

# 图标文件选择
icon_label = tk.Label(root, text=LANGUAGES[current_language]["icon_label"])
icon_label.grid(row=1, column=0, padx=10, pady=5)
icon_entry = tk.Entry(root, width=50)
icon_entry.grid(row=1, column=1, padx=10, pady=5)
icon_browse_button = tk.Button(root, text=LANGUAGES[current_language]["icon_browse"], command=select_icon_file)
icon_browse_button.grid(row=1, column=2, padx=10, pady=5)

# 描述输入
desc_label = tk.Label(root, text=LANGUAGES[current_language]["desc_label"])
desc_label.grid(row=2, column=0, padx=10, pady=5)
desc_entry = tk.Entry(root, width=50)
desc_entry.grid(row=2, column=1, padx=10, pady=5)
# 设置默认描述
desc_entry.insert(0, LANGUAGES[current_language]["description_default"])
desc_preview_button = tk.Button(root, text=LANGUAGES[current_language]["desc_preview"], command=preview_description)
desc_preview_button.grid(row=2, column=2, padx=10, pady=5)

# 输出文件夹选择
output_folder_label = tk.Label(root, text=LANGUAGES[current_language]["output_folder_label"])
output_folder_label.grid(row=3, column=0, padx=10, pady=5)
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=3, column=1, padx=10, pady=5)
output_folder_browse_button = tk.Button(root, text=LANGUAGES[current_language]["output_folder_browse"],
                                        command=select_output_folder)
output_folder_browse_button.grid(row=3, column=2, padx=10, pady=5)

# 压缩包名称输入
zip_name_label = tk.Label(root, text=LANGUAGES[current_language]["zip_name_label"])
zip_name_label.grid(row=4, column=0, padx=10, pady=5)
zip_name_entry = tk.Entry(root, width=50)
zip_name_entry.grid(row=4, column=1, padx=10, pady=5)

# 输出格式选择
output_format_label = tk.Label(root, text=LANGUAGES[current_language]["output_format_label"])
output_format_label.grid(row=5, column=0, padx=10, pady=5)
output_format_var = tk.StringVar(root)
output_format_var.set(LANGUAGES[current_language]["output_format_folder"])
output_format_menu = tk.OptionMenu(root, output_format_var, LANGUAGES[current_language]["output_format_folder"],
                                   LANGUAGES[current_language]["output_format_zip"])
output_format_menu.grid(row=5, column=1, padx=10, pady=5)

# 版本选择
version_label = tk.Label(root, text=LANGUAGES[current_language]["version_label"])
version_label.grid(row=6, column=0, padx=10, pady=5)
version_var = tk.StringVar(root)
version_var.set(list(VERSION_FORMAT_MAP.keys())[0])
version_menu = tk.OptionMenu(root, version_var, *VERSION_FORMAT_MAP.keys())
version_menu.grid(row=6, column=1, padx=10, pady=5)

# 语言选择
language_label = tk.Label(root, text=LANGUAGES[current_language]["language"])
language_label.grid(row=7, column=0, padx=10, pady=5)
language_var = tk.StringVar(root)
language_var.set(current_language)
language_var.trace("w", change_language)
language_menu = tk.OptionMenu(root, language_var, "中文", "英文")
language_menu.grid(row=7, column=1, padx=10, pady=5)

# 左侧偏移输入
left_shift_label = tk.Label(root, text=LANGUAGES[current_language]["left_shift_label"])
left_shift_label.grid(row=8, column=0, padx=10, pady=5)
left_shift_entry = tk.Entry(root, width=20)
left_shift_entry.insert(0, "0")
left_shift_entry.grid(row=8, column=1, padx=10, pady=5)

# 下侧偏移输入
bottom_shift_label = tk.Label(root, text=LANGUAGES[current_language]["bottom_shift_label"])
bottom_shift_label.grid(row=9, column=0, padx=10, pady=5)
bottom_shift_entry = tk.Entry(root, width=20)
bottom_shift_entry.insert(0, "0")
bottom_shift_entry.grid(row=9, column=1, padx=10, pady=5)

# 字体大小输入
font_size_label = tk.Label(root, text=LANGUAGES[current_language]["font_size_label"])
font_size_label.grid(row=10, column=0, padx=10, pady=5)
font_size_entry = tk.Entry(root, width=20)
font_size_entry.insert(0, "11")
font_size_entry.grid(row=10, column=1, padx=10, pady=5)

# 分辨率输入
resolution_label = tk.Label(root, text=LANGUAGES[current_language]["resolution_label"])
resolution_label.grid(row=11, column=0, padx=10, pady=5)
resolution_entry = tk.Entry(root, width=20)
resolution_entry.insert(0, "4")
resolution_entry.grid(row=11, column=1, padx=10, pady=5)

# 创建按钮
create_button = tk.Button(root, text=LANGUAGES[current_language]["create_button"], command=create_pack)
create_button.grid(row=12, column=1, padx=10, pady=20)

# 进度条
progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.grid(row=13, column=0, columnspan=3, padx=10, pady=10)

# 运行主循环
root.mainloop()
    
