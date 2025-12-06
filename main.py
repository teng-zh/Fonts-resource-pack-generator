import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import json
import zipfile
import os
import sys
import base64
from io import BytesIO
import threading

class FontCraftModern:
    def __init__(self, root):
        self.root = root
        self.root.title("FontCraft")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # 初始化变量
        self.pagetitle = "𝔽𝕠𝕟𝕥𝕮𝖗𝖆𝖋𝖙"
        self.id = "test_font"
        self.ready = False
        self.language = 1
        self.packver = 4
        self.shiftL = tk.IntVar(value=0)
        self.shiftD = tk.IntVar(value=0)
        self.size = tk.IntVar(value=11)
        self.oversample = tk.IntVar(value=4)
        self.pack_desc = tk.StringVar(value="自定义字体包！φ(゜▽゜*)♪")
        
        # 资源包图标
        self.default_icon = "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TxSItDnYQKZihOtlFRRxLFYtgobQVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4BQqvGVLMvDqiaZWSSCTFfWBUHXhGAHyGMISIxU09lF3PwHF/38PH1LsazvM/9OUJK0WSATySOM92wiDeIZzctnfM+cZhVJIX4nHjSoAsSP3JddvmNc9lhgWeGjVxmnjhMLJZ7WO5hVjFU4hniqKJqlC/kXVY4b3FWaw3WuSd/YbCorWS5TjOCJJaQQhoiZDRQRQ0WYrRqpJjI0H7Cwz/q+NPkkslVBSPHAupQITl+8D/43a1Zmp5yk4IJoP/Ftj/GgYFdoN207e9j226fAP5n4Err+ustYO6T9GZXix4BQ9vAxXVXk/eAyx1g5EmXDMmR/DSFUgl4P6NvKgDDt8DgmttbZx+nD0COulq+AQ4OgYkyZa97vDvQ29u/Zzr9/QCNB3Kxtb/9yQAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAAuIwAALiMBeKU/dgAAAAd0SU1FB+gIAw0iKI7ZqukAAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAB10lEQVR42u3d7amCUBzA4b/2QoO0QF8aIKgPQfs0QCsJUTs0QdAeCcc7wH3jmN26+jzgp7Rjh58pElZERBMMVmkKBIAAEAACQAAIAAEgAASAABAAAkAACAABIAAEgAAQAAJAAPxz45yVj8djrFarXk9ISilms9nD75M7V12N+9QAyrKMyWTS6wDquu7mqzVzrroa1ykAASAABIAAEAACQAAIAAHwWdat4Mvl8rQdWa/XWevfbre4Xq+d70dKaXARNO+w5KqqqnmXff9qOZ1OWZ/nfr+/ZD+dAlwDIAAEgAAQAAJAAAzH2BR873A4xGKxaLXtfD7POxLLMqqqajVWSil2u50AurZcLrNvUbc1Go1iu9222vaRXxQ7BbgGQAAIAAEgAASAABAAAkAACGDINptNFEXRajmfz1lj1XXdeqzpdCoABIAAEAACQAAIAAEgAASAABAAAkAACAABIAAEgAAQgAAQAAJAAAgAASAABIAAEAACoN88K/hdjkQPix42D4vGNQACwEVgP/z2P8t/9UcUAniR/X7/4+tN0zgFIAAEgAAQAALgBYqIaEyDbwAEgAAQAAJAAAgAASAABIAAEAACQAAIAAEgAASAABAAAkAACAAB8P98AHnmEbJ9AFQHAAAAAElFTkSuQmCC"
        self.pack_icon = self.default_icon
        self.pack_icon_image = None
        
        # 语言文本
        self.uitexts = self.load_uitexts()
        self.dragareatxt = tk.StringVar(value=self.uitexts[self.language]["tip1"])
        
        # 字体文件
        self.fontfile = None
        self.font_name = ""
        self.font_ext = ""
        
        # 创建界面
        self.create_widgets()
    
    def load_uitexts(self):
        return [
            {
                "tip1": "Drag & Drop a Font File!\n (or Click to upload)",
                "tip2": "Drop it!",
                "tip3": ".ttf/.otf file only!",
                "tip4": "Generate!",
                "tip5": "Support for .otf font format was dropped by Minecraft Java Edition since 1.20.5, and font pack containing .otf fonts will fail to load. In this case please use a .ttf font instead.",
                "redirect": "This tool is for Java Edition 1.13+, for JE 1.13- or BE please check here",
                "params": ["Left shift", "Down shift", "Size", "OverSample", "Icon", "Description"],
                "paramtips": [
                    "Horizontal distance by which the characters are shifted",
                    "Distance by which the characters are shifted",
                    "Font size",
                    "Font resolution",
                    "Pack icon",
                    "Pack description"
                ],
                "desc": "Custom Font Pack!φ(゜▽゜*)♪",
                "zipname": " Font Pack"
            },
            {
                "tip1": "把字体文件拖放到这里!\n （或点击上传）",
                "tip2": "松开鼠标",
                "tip3": "仅支持.ttf/.otf文件",
                "tip4": "点此生成!",
                "tip5": "Minecraft Java版从1.20.5起取消了对.otf字体的支持，含有.otf的字体包会导致游戏资源加载失败。若遇到此种情况，请使用.ttf字体替代原来的.otf字体。",
                "redirect": "本工具适用于Java版1.13+，Java版1.13以下及基岩版请点这里",
                "params": ["左侧偏移", "下侧偏移", "大小", "分辨率", "图标", "描述"],
                "paramtips": [
                    "字体的水平分隔距离",
                    "字体的竖直分隔距离",
                    "字号",
                    "字体的清晰度",
                    "资源包图标",
                    "资源包描述"
                ],
                "desc": "自定义字体包！φ(゜▽゜*)♪",
                "zipname": "字体包"
            },
            {
                "tip1": "把字體文件拖放到這裏!\n （或點擊上傳）",
                "tip2": "松開鼠標",
                "tip3": "僅支持.ttf/.otf文件",
                "tip4": "點此生成!",
                "tip5": "Minecraft Java版從1.20.5起取消了對.otf字體的支持，含有.otf的字體包會導致遊戲資源加載失敗。若遇到此種情況，請使用.ttf字體替代原來的.otf字體。",
                "redirect": "本工具適用於Java版1.13+，Java版1.13以下及基巖版請點這裏",
                "params": ["左側偏移", "下側偏移", "大小", "分辨率", "圖示", "描述"],
                "paramtips": [
                    "字體的水平分隔距離",
                    "字體的豎直分隔距離",
                    "字號",
                    "字體的清晰度",
                    "資源包圖示",
                    "資源包描述"
                ],
                "desc": "自訂字體包！φ(゜▽゜*)♪",
                "zipname": "字體包"
            },
            {
                "tip1": "フォントをここにドラッグしてください\n （またはクリックしてアップロード）",
                "tip2": "マウスを放してください",
                "tip3": ".ttf/.otfフォントのみ",
                "tip4": "生成します!",
                "tip5": ".otfフォント形式のサポートはMinecraft Java Edition 1.20.5以降で廃止され、.otfフォントを含むフォント パックはロードできなくなります。この場合は、代わりに.ttfフォントを使用してください。",
                "redirect": "このツールはJava Edition 1.13以降用、JE 1.13以前またはBE用はここを確認してください",
                "params": ["シフト（左）", "シフト（下）", "サイズ", "解像度", "アイコン", "テキスト"],
                "paramtips": [
                    "描画位置をずらす場合、どれくらいずらすか。",
                    "描画位置をずらす場合、どれくらいずらすか。",
                    "描画サイズ",
                    "解像度",
                    "パックアイコン",
                    "パックテキスト"
                ],
                "desc": "フォントパック！φ(゜▽゜*)♪",
                "zipname": "フォントパック"
            }
        ]
    
    def create_widgets(self):
        # 标题
        title_label = tk.Label(self.root, text=self.pagetitle, font=("Arial", 32, "bold"), pady=20)
        title_label.pack(fill="x", padx=20)
        
        # 主内容区
        self.content_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 初始显示拖放面板
        self.create_drop_panel()
        
        # 经典链接区
        self.classic_link_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.classic_link_frame.pack(fill="x", padx=20, pady=10)
        
        self.classic_link = tk.Label(self.classic_link_frame, text=self.uitexts[self.language]["redirect"], 
                                   fg="blue", cursor="hand2", font=("Arial", 14), underline=True)
        self.classic_link.pack()
        self.classic_link.bind("<Button-1>", self.run_under_py)
        
        # 语言选择
        self.lang_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.lang_frame.pack(side="left", padx=20, pady=10)
        
        lang_options = [
            ("En", 0),
            ("简", 1),
            ("繁", 2),
            ("日", 3)
        ]
        
        for text, lang_id in lang_options:
            btn = tk.Button(self.lang_frame, text=text, command=lambda lid=lang_id: self.lang(lid), 
                           width=8, height=2, font=("Arial", 12))
            btn.pack(side="top", pady=5)
        
        # 版本选择
        self.ver_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.ver_frame.pack(side="right", padx=20, pady=10)
        
        ver_options = [
            ("1.20.2 ~ 1.21", 18),
            ("1.20 ~ 1.20.1", 15),
            ("1.19.4", 13),
            ("1.19.3", 12),
            ("1.19 ~ 1.19.2", 9),
            ("1.18 ~ 1.18.2", 8),
            ("1.17 ~ 1.17.1", 7),
            ("1.16.2 ~ 1.16.5", 6),
            ("1.15 ~ 1.16.1", 5),
            ("1.13 ~ 1.14.4", 4)
        ]
        
        for text, ver in ver_options:
            btn = tk.Button(self.ver_frame, text=text, command=lambda v=ver: self.pack_format(v), 
                           width=15, height=2, font=("Arial", 12))
            btn.pack(side="top", pady=5)
    
    def create_drop_panel(self):
        # 清除现有内容
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # 创建拖放区域
        self.drop_panel = tk.Frame(self.content_frame, bg="#ffffff", width=560, height=320, relief="groove", bd=2)
        self.drop_panel.pack(expand=True)
        
        # 拖放提示
        self.drag_area = tk.Label(self.drop_panel, textvariable=self.dragareatxt, font=("Arial", 16), 
                                 bg="#ffffff", justify="center", pady=50, padx=20)
        self.drag_area.pack(expand=True)
        
        # 绑定事件
        self.drop_panel.bind("<Button-1>", lambda e: self.sel_file())
        self.drop_panel.bind("<DragEnter>", self.on_drag_enter)
        self.drop_panel.bind("<DragLeave>", self.on_drag_leave)
        self.drop_panel.bind("<Drop>", self.on_drop)
        self.drop_panel.bind("<DragOver>", self.on_drag_over)
    
    def create_pack_panel(self):
        # 清除现有内容
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # 创建资源包面板
        self.pack_panel = tk.Frame(self.content_frame, bg="#ffffff", width=560, height=320, relief="groove", bd=2)
        self.pack_panel.pack(expand=True, padx=20, pady=20)
        
        # 选项框架
        opt_frame = tk.Frame(self.pack_panel, bg="#ffffff")
        opt_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)
        
        # 左侧偏移
        self.create_option(opt_frame, 0, self.uitexts[self.language]["params"][0], 
                          self.shiftL, -10, 10, 1)
        
        # 下侧偏移
        self.create_option(opt_frame, 1, self.uitexts[self.language]["params"][1], 
                          self.shiftD, -10, 10, 1)
        
        # 大小
        self.create_option(opt_frame, 2, self.uitexts[self.language]["params"][2], 
                          self.size, 1, 50, 1)
        
        # 分辨率
        self.create_option(opt_frame, 3, self.uitexts[self.language]["params"][3], 
                          self.oversample, 1, 16, 1)
        
        # 图标
        icon_frame = tk.Frame(opt_frame, bg="#ffffff")
        icon_frame.grid(row=4, column=0, sticky="w", pady=10)
        
        icon_label = tk.Label(icon_frame, text=self.uitexts[self.language]["params"][4], font=("Arial", 12), bg="#ffffff", width=15, anchor="w")
        icon_label.grid(row=0, column=0, padx=5, pady=5)
        
        # 加载图标
        self.pack_icon_image = self.base64_to_image(self.pack_icon)
        self.icon_label = tk.Label(icon_frame, image=self.pack_icon_image, bg="#ffffff", relief="groove", bd=1)
        self.icon_label.grid(row=0, column=1, padx=5, pady=5)
        self.icon_label.bind("<Button-1>", lambda e: self.sel_icon_file())
        
        # 描述
        desc_frame = tk.Frame(opt_frame, bg="#ffffff")
        desc_frame.grid(row=5, column=0, sticky="w", pady=10)
        
        desc_label = tk.Label(desc_frame, text=self.uitexts[self.language]["params"][5], font=("Arial", 12), bg="#ffffff", width=15, anchor="w")
        desc_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.desc_entry = tk.Entry(desc_frame, textvariable=self.pack_desc, font=("Arial", 12), width=30)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # OTF提示
        otf_hint_frame = tk.Frame(self.pack_panel, bg="#ffffff")
        otf_hint_frame.pack(side="right", padx=20, pady=20)
        
        otf_hint = tk.Label(otf_hint_frame, text=self.uitexts[self.language]["tip5"], font=("Arial", 10), 
                           bg="#ffffff", justify="left", wraplength=300)
        otf_hint.pack()
        
        # 生成按钮
        self.generate_btn = tk.Button(self.pack_panel, text=self.uitexts[self.language]["tip4"], command=self.generate_res_pack, 
                                    font=("Arial", 24, "bold"), bg="#4CAF50", fg="white", padx=20, pady=10)
        self.generate_btn.pack(side="bottom", pady=20)
    
    def create_option(self, parent, row, label_text, variable, min_val, max_val, step):
        frame = tk.Frame(parent, bg="#ffffff")
        frame.grid(row=row, column=0, sticky="w", pady=10)
        
        label = tk.Label(frame, text=label_text, font=("Arial", 12), bg="#ffffff", width=15, anchor="w")
        label.grid(row=0, column=0, padx=5, pady=5)
        
        spinbox = tk.Spinbox(frame, from_=min_val, to=max_val, increment=step, textvariable=variable, 
                            font=("Arial", 12), width=10)
        spinbox.grid(row=0, column=1, padx=5, pady=5)
    
    def on_drag_enter(self, event):
        self.dragareatxt.set(self.uitexts[self.language]["tip2"])
        return event.action
    
    def on_drag_leave(self, event):
        self.dragareatxt.set(self.uitexts[self.language]["tip1"])
        return event.action
    
    def on_drag_over(self, event):
        event.preventDefault()
        return "copy"
    
    def on_drop(self, event):
        event.preventDefault()
        files = event.data.split()
        if files:
            file_path = files[0]
            self.process_font_file(file_path)
        self.dragareatxt.set(self.uitexts[self.language]["tip1"])
    
    def sel_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Font Files", "*.ttf *.otf"), ("All Files", "*.*")]
        )
        if file_path:
            self.process_font_file(file_path)
    
    def process_font_file(self, file_path):
        # 检查文件扩展名
        ext = os.path.splitext(file_path)[1].lower()[1:]  # 去掉点
        if ext == "ttf" or ext == "otf":
            self.fontfile = file_path
            self.font_name = os.path.splitext(os.path.basename(file_path))[0]
            self.font_ext = ext
            self.ready = True
            self.create_pack_panel()
        else:
            messagebox.showwarning("Warning", self.uitexts[self.language]["tip3"])
    
    def sel_icon_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
        )
        if file_path:
            self.process_icon_file(file_path)
    
    def process_icon_file(self, file_path):
        # 读取PNG文件并转换为base64
        with open(file_path, "rb") as f:
            icon_data = f.read()
        self.pack_icon = base64.b64encode(icon_data).decode("utf-8")
        
        # 更新图标显示
        self.pack_icon_image = self.base64_to_image(self.pack_icon)
        self.icon_label.config(image=self.pack_icon_image)
    
    def base64_to_image(self, base64_str):
        # 将base64字符串转换为PIL图像
        image_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_data))
        image = image.resize((128, 128))
        return ImageTk.PhotoImage(image)
    
    def run_under_py(self, event):
        # 运行under.py或under.exe
        under_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "under.py")
        under_exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "under.exe")
        
        if os.path.exists(under_exe_path):
            # 优先运行exe文件
            os.startfile(under_exe_path)
        elif os.path.exists(under_py_path):
            # 运行py文件
            os.system(f"python {under_py_path}")
        else:
            messagebox.showerror("Error", "under.py or under.exe not found!")
    
    def lang(self, ln):
        self.language = ln
        self.dragareatxt.set(self.uitexts[ln]["tip1"])
        self.pack_desc.set(self.uitexts[ln]["desc"])
        
        # 更新界面文本
        self.update_ui_texts()
    
    def update_ui_texts(self):
        # 更新经典链接文本
        self.classic_link.config(text=self.uitexts[self.language]["redirect"])
        
        # 如果已经在资源包面板，更新面板文本
        if self.ready:
            self.create_pack_panel()
    
    def pack_format(self, ver):
        self.packver = ver
    
    def generate_res_pack(self):
        if not self.fontfile:
            messagebox.showwarning("Warning", "Please select a font file first!")
            return
        
        # 显示进度
        self.generate_btn.config(text="Generating...", state="disabled")
        self.root.update_idletasks()
        
        # 在后台线程中生成资源包
        threading.Thread(target=self._generate_res_pack_thread, daemon=True).start()
    
    def _generate_res_pack_thread(self):
        try:
            # 生成文件名
            zip_filename = f"{self.font_name}{self.uitexts[self.language]['zipname']}.zip"
            
            # 选择保存位置
            output_path = filedialog.asksaveasfilename(
                defaultextension=".zip",
                filetypes=[("Zip Files", "*.zip"), ("All Files", "*.*")],
                initialfile=zip_filename
            )
            
            if not output_path:
                self.generate_btn.config(text=self.uitexts[self.language]["tip4"], state="normal")
                return
            
            # 创建临时目录
            import tempfile
            with tempfile.TemporaryDirectory() as temp_dir:
                # 创建pack.mcmeta
                mcmeta_data = {
                    "pack": {
                        "pack_format": self.packver,
                        "supported_formats": {
                            "min_inclusive": 4,
                            "max_inclusive": 34
                        },
                        "description": self.pack_desc.get()
                    }
                }
                
                with open(os.path.join(temp_dir, "pack.mcmeta"), "w", encoding="utf-8") as f:
                    json.dump(mcmeta_data, f, indent=4, ensure_ascii=False)
                
                # 创建pack.png
                pack_png_path = os.path.join(temp_dir, "pack.png")
                with open(pack_png_path, "wb") as f:
                    f.write(base64.b64decode(self.pack_icon))
                
                # 创建字体目录
                font_dir = os.path.join(temp_dir, "assets", "minecraft", "font")
                os.makedirs(font_dir, exist_ok=True)
                
                # 创建default.json
                default_data = {
                    "providers": [
                        {
                            "type": "ttf",
                            "file": f"minecraft:custom.{self.font_ext}",
                            "shift": [self.shiftL.get(), self.shiftD.get()],
                            "size": self.size.get(),
                            "oversample": self.oversample.get()
                        }
                    ]
                }
                
                with open(os.path.join(font_dir, "default.json"), "w", encoding="utf-8") as f:
                    json.dump(default_data, f, indent=4, ensure_ascii=False)
                
                # 复制字体文件
                import shutil
                shutil.copy2(self.fontfile, os.path.join(font_dir, f"custom.{self.font_ext}"))
                
                # 创建zip文件
                with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arcname)
            
            # 更新按钮状态
            self.root.after(0, lambda: self.generate_btn.config(text=self.uitexts[self.language]["tip4"], state="normal"))
            messagebox.showinfo("Success", "Resource pack generated successfully!")
            
        except Exception as e:
            self.root.after(0, lambda: self.generate_btn.config(text=self.uitexts[self.language]["tip4"], state="normal"))
            messagebox.showerror("Error", f"Failed to generate resource pack: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FontCraftModern(root)
    root.mainloop()
