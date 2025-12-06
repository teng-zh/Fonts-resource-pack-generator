import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageDraw, ImageFont
import zipfile
import json
import os
import tempfile
import uuid
from io import BytesIO

class FontCraftClassic:
    def __init__(self, root):
        self.root = root
        self.root.title("FontCraft Classic")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # 语言配置
        self.language = 1  # 默认简体中文
        self.uitexts = self.load_uitexts()
        
        # 字体参数
        self.font_path = ""
        self.font_name = "monospace"
        self.font_size = tk.IntVar(value=60)
        self.grid_size = tk.IntVar(value=64)
        self.y_offset = tk.IntVar(value=0)
        self.meta_mode = tk.StringVar(value="je")
        self.pack_format_je = tk.StringVar(value="1")
        self.description_format = tk.StringVar(value=self.uitexts[self.language]["desc"])
        
        # 状态变量
        self.preview_info = tk.StringVar(value=self.uitexts[self.language]["status_ready"])
        self.gen_btn_text = tk.StringVar(value=self.uitexts[self.language]["generate"])
        self.is_generating = False
        
        # 创建界面
        self.create_widgets()
        
    def load_uitexts(self):
        return [
            {
                "params": ["Font File", "Font Size", "Grid Size", "Vertical Offset", "Platform", "Game Version (JE)", "Pack Description Format"],
                "redirect": "This tool is for Java Edition 1.13- and BE, for JE 1.13+ please check here",
                "desc": "Custom Font Pack!φ(゜▽゜*)♪ %s %dx(%d)",
                "je": "Java Edition (Before 1.13)",
                "be": "Bedrock Edition",
                "generate": "Generate!",
                "stop": "Stop!",
                "reset": "Reset",
                "status_ready": "Ready.",
                "status_start": "Starting...",
                "status_store_size": "Storing glyph_sizes.bin...",
                "status_create_meta": "Creating metafile...",
                "status_finish": "Finishing and zipping file...",
                "status_lang": "Interface switched to English"
            },
            {
                "params": ["字体文件", "字体尺寸", "网格尺寸", "垂直偏移", "平台", "游戏版本 (Java版)", "字体包描述格式"],
                "redirect": "本工具适用于Java版1.13-及基岩版，Java版1.13+请点这里",
                "desc": "自定义字体包！φ(゜▽゜*)♪ %s %dx(%d)",
                "je": "Java版 (1.13前)",
                "be": "基岩版",
                "generate": "生成！",
                "stop": "停止！",
                "reset": "重置",
                "status_ready": "已就绪.",
                "status_start": "开始中...",
                "status_store_size": "正在保存glyph_sizes.bin...",
                "status_create_meta": "正在创建元文件...",
                "status_finish": "打包中...",
                "status_lang": "界面已切换为简体中文"
            },
            {
                "params": ["字體文件", "字體尺寸", "網格尺寸", "垂直偏移", "平臺", "遊戲版本 (Java版)", "字體包描述格式"],
                "redirect": "本工具適用於Java版1.13-及基巖版，Java版1.13+請點這裏",
                "desc": "自訂字體包！φ(゜▽゜*)♪ %s %dx(%d)",
                "je": "Java版 (1.13前)",
                "be": "基巖版",
                "generate": "生成！",
                "stop": "停止！",
                "reset": "重置",
                "status_ready": "已就緒.",
                "status_start": "開始中...",
                "status_store_size": "正在保存glyph_sizes.bin...",
                "status_create_meta": "正在創建元文件...",
                "status_finish": "打包中...",
                "status_lang": "界面已切換為繁體中文"
            },
            {
                "params": ["フォントファイル", "フォントサイズ", "グリッドサイズ", "垂直オフセット", "プラットホーム", "ゲームバージョン (JE向け)", "パックの説明のフォーマット"],
                "redirect": "このツールはJava Edition 1.13以前またはBE用、JE 1.13以降はここを確認してください。",
                "desc": "フォントパック！φ(゜▽゜*)♪ %s %dx(%d)",
                "je": "Java Edition (1.13以前)",
                "be": "Bedrock Edition",
                "generate": "生成する!",
                "stop": "終了する!",
                "reset": "リセット",
                "status_ready": "準備完了.",
                "status_start": "始動中...",
                "status_store_size": "glyph_sizes.binを生成している...",
                "status_create_meta": "メタファイルを作成している...",
                "status_finish": "パッキング...",
                "status_lang": "インターフェース言語を日本語に切り替えた"
            }
        ]
    
    def create_widgets(self):
        # 头部
        header_frame = tk.Frame(self.root, bg="#ccc", height=64)
        header_frame.pack(fill="x", side="top")
        
        header_label = tk.Label(header_frame, text="𝕱𝖔𝖓𝖙𝕮𝖗𝖆𝖋𝖙 𝕮𝖑𝖆𝖘𝖘𝖎𝖈", font=("Arial", 24), bg="#ccc")
        header_label.pack(pady=10, padx=20, anchor="w")
        
        # 主内容区
        content_frame = tk.Frame(self.root, bg="#aaa")
        content_frame.pack(fill="both", expand=True, padx=32, pady=32)
        
        # 左侧预览区
        preview_frame = tk.Frame(content_frame, bg="#ccc", width=300)
        preview_frame.pack(side="left", padx=10, pady=10, fill="y")
        
        # 预览画布
        self.preview_canvas = tk.Canvas(preview_frame, width=256, height=256, bg="black", highlightbackground="#ddd", highlightthickness=16)
        self.preview_canvas.pack(pady=20, padx=20)
        
        # 预览信息
        self.preview_info_label = tk.Label(preview_frame, textvariable=self.preview_info, bg="#ccc", font=("Courier", 10), justify="left", anchor="w")
        self.preview_info_label.pack(fill="x", padx=20, pady=10)
        
        # 右侧面板
        panel_frame = tk.Frame(content_frame, bg="#bbb", width=450)
        panel_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)
        
        panel_content = tk.Frame(panel_frame, bg="#f7f7f7")
        panel_content.pack(fill="both", expand=True, padx=16, pady=16)
        
        # 表单
        form_frame = tk.Frame(panel_content, bg="#f7f7f7")
        form_frame.pack(fill="x", padx=8)
        
        # 字体文件选择
        self.create_form_row(form_frame, 0, self.uitexts[self.language]["params"][0], self.create_font_input)
        
        # 字体尺寸
        self.create_form_row(form_frame, 1, self.uitexts[self.language]["params"][1], self.create_fontsize_input)
        
        # 网格尺寸
        self.create_form_row(form_frame, 2, self.uitexts[self.language]["params"][2], self.create_gridsize_input)
        
        # 垂直偏移
        self.create_form_row(form_frame, 3, self.uitexts[self.language]["params"][3], self.create_yoffset_input)
        
        # 平台选择
        self.create_form_row(form_frame, 4, self.uitexts[self.language]["params"][4], self.create_platform_input)
        
        # 游戏版本
        self.create_form_row(form_frame, 5, self.uitexts[self.language]["params"][5], self.create_version_input)
        
        # 描述格式
        self.create_form_row(form_frame, 6, self.uitexts[self.language]["params"][6], self.create_description_input)
        
        # 分隔线
        separator = tk.Frame(panel_content, bg="#bbb", height=16)
        separator.pack(fill="x", pady=10)
        
        # 按钮栏
        button_frame = tk.Frame(panel_content, bg="#f7f7f7")
        button_frame.pack(fill="x", padx=8, pady=8)
        
        # 生成按钮
        self.generate_btn = tk.Button(button_frame, textvariable=self.gen_btn_text, command=self.click_gen, font=("Arial", 16), height=2)
        self.generate_btn.pack(side="left", fill="x", expand=True, padx=8, pady=8)
        
        # 重置按钮
        self.reset_btn = tk.Button(button_frame, text=self.uitexts[self.language]["reset"], command=self.click_reset, font=("Arial", 16), height=2)
        self.reset_btn.pack(side="right", fill="x", expand=True, padx=8, pady=8)
        
        # 语言选择
        lang_frame = tk.Frame(self.root, bg="#aaa")
        lang_frame.pack(fill="x", padx=10, pady=10, side="bottom")
        
        # 语言按钮
        lang_buttons = [
            ("En", 0, 0),
            ("简", 1, 1),
            ("繁", 2, 2),
            ("日", 3, 3)
        ]
        
        for text, lang_id, column in lang_buttons:
            btn = tk.Button(lang_frame, text=text, command=lambda lid=lang_id: self.lang(lid), width=8, height=2)
            btn.grid(row=0, column=column, padx=5, pady=5)
        
        # 链接
        link_label = tk.Label(self.root, text=self.uitexts[self.language]["redirect"], fg="blue", cursor="hand2", font=("Arial", 12))
        link_label.pack(pady=10, side="bottom")
        link_label.bind("<Button-1>", lambda e: self.open_link())
    
    def create_form_row(self, parent, row, label_text, input_creator):
        row_frame = tk.Frame(parent, bg="#f7f7f7")
        row_frame.pack(fill="x", pady=10)
        
        label = tk.Label(row_frame, text=label_text, width=20, font=("Arial", 14), bg="#f7f7f7", anchor="w")
        label.pack(side="left", padx=5)
        
        input_frame = tk.Frame(row_frame, bg="#f7f7f7")
        input_frame.pack(side="right", fill="x", expand=True, padx=5)
        
        input_creator(input_frame)
    
    def create_font_input(self, parent):
        def browse_font():
            file_path = filedialog.askopenfilename(
                filetypes=[("Font Files", "*.ttf *.otf *.woff *.woff2"), ("All Files", "*.*")]
            )
            if file_path:
                self.font_path = file_path
                self.font_name = os.path.splitext(os.path.basename(file_path))[0]
                font_label.config(text=self.font_name)
        
        frame = tk.Frame(parent, bg="#f7f7f7")
        frame.pack(fill="x", expand=True)
        
        font_label = tk.Label(frame, text=self.font_name, bg="#bbb", font=("Arial", 12), anchor="w", relief="solid", borderwidth=1)
        font_label.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        browse_btn = tk.Button(frame, text="Browse...", command=browse_font, bg="#fff", font=("Arial", 12))
        browse_btn.pack(side="right", padx=5, pady=5)
    
    def create_fontsize_input(self, parent):
        spinbox = tk.Spinbox(parent, from_=6, to=200, textvariable=self.font_size, font=("Arial", 12), width=10)
        spinbox.pack(fill="x", expand=True, padx=5, pady=5)
    
    def create_gridsize_input(self, parent):
        spinbox = tk.Spinbox(parent, from_=8, to=256, textvariable=self.grid_size, font=("Arial", 12), width=10)
        spinbox.pack(fill="x", expand=True, padx=5, pady=5)
    
    def create_yoffset_input(self, parent):
        spinbox = tk.Spinbox(parent, from_=-50, to=50, textvariable=self.y_offset, font=("Arial", 12), width=10)
        spinbox.pack(fill="x", expand=True, padx=5, pady=5)
    
    def create_platform_input(self, parent):
        def on_platform_change(): 
            self.set_ver_sel(self.meta_mode.get() == "je")
        
        frame = tk.Frame(parent, bg="#f7f7f7")
        frame.pack(fill="x", expand=True)
        
        je_radio = tk.Radiobutton(frame, text=self.uitexts[self.language]["je"], variable=self.meta_mode, value="je", command=on_platform_change, bg="#f7f7f7", font=("Arial", 12))
        je_radio.pack(side="left", padx=5, pady=5)
        
        be_radio = tk.Radiobutton(frame, text=self.uitexts[self.language]["be"], variable=self.meta_mode, value="be", command=on_platform_change, bg="#f7f7f7", font=("Arial", 12))
        be_radio.pack(side="left", padx=5, pady=5)
    
    def create_version_input(self, parent):
        self.version_combo = ttk.Combobox(parent, textvariable=self.pack_format_je, values=["1", "2", "3"], state="readonly", font=("Arial", 12))
        self.version_combo.pack(fill="x", expand=True, padx=5, pady=5)
        self.version_combo.current(0)
    
    def create_description_input(self, parent):
        entry = tk.Entry(parent, textvariable=self.description_format, font=("Arial", 12))
        entry.pack(fill="x", expand=True, padx=5, pady=5)
    
    def set_ver_sel(self, active):
        if active:
            self.version_combo.config(state="readonly")
        else:
            self.version_combo.config(state="disabled")
    
    def lang(self, ln):
        self.language = ln
        self.preview_info.set(self.uitexts[ln]["status_lang"])
        self.gen_btn_text.set(self.uitexts[ln]["stop"] if self.is_generating else self.uitexts[ln]["generate"])
        self.description_format.set(self.uitexts[ln]["desc"])
        # 更新界面文本
        self.update_ui_texts()
    
    def update_ui_texts(self):
        # 这里需要更新所有界面文本，由于Tkinter的限制，我们需要重新创建表单
        # 简化处理，只更新动态文本
        self.reset_btn.config(text=self.uitexts[self.language]["reset"])
    
    def open_link(self):
        import webbrowser
        webbrowser.open("https://codepen.io/devbobcorn/full/YzZMZvV")
    
    def click_gen(self):
        if self.is_generating:
            self.stop_generation()
        else:
            self.start_generation()
    
    def start_generation(self):
        if not self.font_path:
            self.preview_info.set("Please select a font file first!")
            return
        
        self.is_generating = True
        self.preview_info.set(self.uitexts[self.language]["status_start"])
        self.gen_btn_text.set(self.uitexts[self.language]["stop"])
        
        # 在后台线程中生成资源包，避免UI阻塞
        import threading
        threading.Thread(target=self.generate_resource_pack, daemon=True).start()
    
    def stop_generation(self):
        self.is_generating = False
        self.preview_info.set(self.uitexts[self.language]["status_ready"])
        self.gen_btn_text.set(self.uitexts[self.language]["generate"])
    
    def generate_resource_pack(self):
        try:
            # 创建临时目录
            with tempfile.TemporaryDirectory() as temp_dir:
                # 准备字体
                font = ImageFont.truetype(self.font_path, self.font_size.get())
                
                # 根据平台选择格式
                if self.meta_mode.get() == "je":
                    formatstring = os.path.join("assets", "minecraft", "textures", "font", "unicode_page_%02x.png")
                    glyph_sizes_bin = os.path.join("assets", "minecraft", "font", "glyph_sizes.bin")
                else:
                    formatstring = os.path.join("font", "glyph_%02X.png")
                    glyph_sizes_bin = None
                
                # 生成glyph_sizes数组
                glyph_sizes = bytearray(64 * 1024)
                
                # 生成字符页面
                for page in range(256):
                    if not self.is_generating:
                        return
                    
                    # 创建图像
                    img = Image.new("RGBA", (self.grid_size.get() * 16, self.grid_size.get() * 16), color="white")
                    draw = ImageDraw.Draw(img)
                    
                    # 绘制字符
                    for i in range(16):
                        for j in range(16):
                            char_code = (page << 8) + (i * 16 + j)
                            char = chr(char_code)
                            
                            # 计算位置
                            x = j * self.grid_size.get()
                            y = i * self.grid_size.get() + self.y_offset.get()
                            
                            # 绘制字符
                            draw.text((x, y), char, font=font, fill="black")
                            
                            # 计算字符宽度
                            bbox = draw.textbbox((x, y), char, font=font)
                            char_width = bbox[2] - bbox[0]
                            glyph_size = min(15, int((char_width / self.grid_size.get()) * 15))
                            glyph_sizes[char_code] = glyph_size
                    
                    # 保存图像
                    img_path = os.path.join(temp_dir, formatstring % page)
                    os.makedirs(os.path.dirname(img_path), exist_ok=True)
                    img.save(img_path, format="PNG")
                    
                    # 更新预览
                    self.update_preview(img)
                    
                    # 更新状态
                    self.preview_info.set(f"Processing page {page:02x}...")
                
                if not self.is_generating:
                    return
                
                # 保存glyph_sizes.bin（仅JE）
                if glyph_sizes_bin:
                    self.preview_info.set(self.uitexts[self.language]["status_store_size"])
                    bin_path = os.path.join(temp_dir, glyph_sizes_bin)
                    os.makedirs(os.path.dirname(bin_path), exist_ok=True)
                    with open(bin_path, "wb") as f:
                        f.write(glyph_sizes)
                
                if not self.is_generating:
                    return
                
                # 创建元文件
                self.preview_info.set(self.uitexts[self.language]["status_create_meta"])
                
                if self.meta_mode.get() == "je":
                    # Java Edition
                    pack_format = int(self.pack_format_je.get())
                    description = self.description_format.get() % (self.font_name, self.grid_size.get(), self.font_size.get())
                    
                    mcmeta = {
                        "pack": {
                            "pack_format": pack_format,
                            "description": description
                        }
                    }
                    
                    mcmeta_path = os.path.join(temp_dir, "pack.mcmeta")
                    with open(mcmeta_path, "w", encoding="utf-8") as f:
                        json.dump(mcmeta, f, indent=4, ensure_ascii=False)
                else:
                    # Bedrock Edition
                    manifest = {
                        "format_version": 1,
                        "header": {
                            "uuid": str(uuid.uuid4()),
                            "name": f"{self.font_name} x{self.grid_size.get()}({self.font_size.get()})",
                            "version": [0, 0, 1],
                            "min_engine_version": [0, 0, 1],
                            "description": self.description_format.get() % (self.font_name, self.grid_size.get(), self.font_size.get())
                        },
                        "modules": [
                            {
                                "description": self.description_format.get() % (self.font_name, self.grid_size.get(), self.font_size.get()),
                                "version": [0, 0, 1],
                                "uuid": str(uuid.uuid4()),
                                "type": "resources"
                            }
                        ]
                    }
                    
                    manifest_path = os.path.join(temp_dir, "manifest.json")
                    with open(manifest_path, "w", encoding="utf-8") as f:
                        json.dump(manifest, f, indent=4, ensure_ascii=False)
                
                if not self.is_generating:
                    return
                
                # 打包成最终文件
                self.preview_info.set(self.uitexts[self.language]["status_finish"])
                
                # 生成文件名
                if self.meta_mode.get() == "je":
                    file_ext = "zip"
                else:
                    file_ext = "mcpack"
                
                output_filename = f"{self.font_name} x{self.grid_size.get()}({self.font_size.get()}) {self.meta_mode.get()}.{file_ext}"
                output_path = filedialog.asksaveasfilename(
                    defaultextension=f".{file_ext}",
                    filetypes=[(f"{file_ext.upper()} Files", f"*.{file_ext}"), ("All Files", "*.*")],
                    initialfile=output_filename
                )
                
                if not output_path or not self.is_generating:
                    return
                
                # 创建zip文件
                with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arcname)
                
                if self.is_generating:
                    self.preview_info.set(self.uitexts[self.language]["status_ready"])
                    self.is_generating = False
                    self.gen_btn_text.set(self.uitexts[self.language]["generate"])
                    
        except Exception as e:
            self.preview_info.set(f"Error: {str(e)}")
            self.is_generating = False
            self.gen_btn_text.set(self.uitexts[self.language]["generate"])
    
    def update_preview(self, img):
        # 调整图像大小以适应预览画布
        preview_img = img.resize((224, 224))  # 256 - 16*2 = 224
        
        # 将PIL图像转换为Tkinter PhotoImage
        photo = self.pil_to_tk(preview_img)
        
        # 更新画布
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(128, 128, image=photo)
        self.preview_canvas.image = photo  # 保持引用，防止被垃圾回收
    
    def pil_to_tk(self, img):
        # 将PIL图像转换为Tkinter PhotoImage
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        photo = tk.PhotoImage(data=buffer.getvalue())
        return photo
    
    def click_reset(self):
        # 重置所有参数
        self.font_path = ""
        self.font_name = "monospace"
        self.font_size.set(60)
        self.grid_size.set(64)
        self.y_offset.set(0)
        self.meta_mode.set("je")
        self.pack_format_je.set("1")
        self.description_format.set(self.uitexts[self.language]["desc"])
        self.preview_info.set(self.uitexts[self.language]["status_ready"])
        self.set_ver_sel(True)
        
        # 清除预览
        self.preview_canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = FontCraftClassic(root)
    root.mainloop()
