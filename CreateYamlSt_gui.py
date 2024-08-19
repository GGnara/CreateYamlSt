import tkinter as tk
from tkinter import ttk
import os
from component.folder_operations import update_folder_list, folder_selected
from component.display_gui import PlaceholderFrame
from component.analyze_placeholders import get_global_placeholders, get_global_settings,get_global_folder_path
from component.create_yaml_from_placeholders import generate_yaml_from_placeholders


class MainApplication:
    def __init__(self, root):
        # メインウィンドウの設定
        self.root = root
        self.root.title("CloudFormation YAML プレースホルダー設定")
        self.root.geometry("550x600")  
        self.root.configure(bg="#2e3f4f")
        
        self.init_main_frame()
        self.placeholder_frame = PlaceholderFrame(self.root, self.show_main_frame)

    def init_main_frame(self):
        # メインフレームの初期化
        self.main_frame = tk.Frame(self.root, bg="#2e3f4f", width=800)  # 幅を2/3に変更
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.pack_propagate(False)  # フレームのサイズを固定
        
        self.folder_path = tk.StringVar()
        self.folder_var = tk.StringVar()
        
        # フォルダ選択用フレームの設定
        self.folder_frame = tk.Frame(self.main_frame, bg="#2e3f4f")
        self.folder_frame.pack(pady=20)
        
        self.folder_label = tk.Label(self.folder_frame, text="フォルダを選択", fg="white", bg="#2e3f4f", font=("Helvetica", 14, "bold"))
        self.folder_label.pack(pady=10)
        
        self.folder_menu = ttk.OptionMenu(self.folder_frame, self.folder_var, "")
        self.folder_menu.pack(pady=10)
        
        self.placeholder_button = tk.Button(self.folder_frame, text="プレースホルダ設定", bg="#4CAF50", fg="white", font=("Helvetica", 12), command=self.show_placeholder_frame)
        self.placeholder_button.pack(pady=10)
        
        # フォルダ操作関数のバインド
        self.update_folder_list = update_folder_list.__get__(self)
        self.folder_selected = folder_selected.__get__(self)
        self.update_folder_list()

    def show_placeholder_frame(self):
        # プレースホルダ設定画面の表示
        self.main_frame.pack_forget()
        self.placeholder_frame.pack(fill=tk.BOTH, expand=True)
        self.placeholder_frame.display_placeholders_in_gui(get_global_placeholders(), get_global_settings())

    def show_main_frame(self, placeholders=None):
        if placeholders:
            # プレースホルダが設定された場合の処理
            self.process_placeholders(placeholders)
        self.placeholder_frame.pack_forget()
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    
    def process_placeholders(self, placeholders):
        # 既存のプレースホルダ表示フレームを削除
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                if widget.winfo_children()[0].cget("text") == "設定されたプレースホルダ":
                    widget.destroy()
                    break

        # プレースホルダ表示用のフレームを作成
        placeholder_frame = tk.Frame(self.main_frame, bg="#2e3f4f", padx=20, pady=20)
        placeholder_frame.pack(fill=tk.BOTH, expand=True)

        # タイトルラベルの設定
        title_label = tk.Label(placeholder_frame, text="設定されたプレースホルダ", fg="#FFD700", bg="#2e3f4f", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # スクロール可能なフレームの設定
        canvas = tk.Canvas(placeholder_frame, bg="#2e3f4f", highlightthickness=0)
        scrollable_frame = tk.Frame(canvas, bg="#2e3f4f")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # プレースホルダの表示
        for placeholder, value in placeholders.items():
            frame = tk.Frame(scrollable_frame, bg="#3a4f63", padx=10, pady=5, relief=tk.RAISED, borderwidth=1)
            frame.pack(fill=tk.X, padx=5, pady=3)
            
            key_label = tk.Label(frame, text=placeholder, fg="#ADD8E6", bg="#3a4f63", font=("Helvetica", 12, "bold"), width=20, anchor="e")
            key_label.pack(side=tk.LEFT, padx=(0, 10))
            
            value_label = tk.Label(frame, text=value, fg="white", bg="#3a4f63", font=("Helvetica", 12), wraplength=400, justify=tk.LEFT)
            value_label.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # スクロールバーとキャンバスの配置
        scrollbar = ttk.Scrollbar(placeholder_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Yaml生成ボタンの追加
        def generate_yaml():
            export_folder = os.path.join(os.path.dirname(__file__), 'export')
            generate_yaml_from_placeholders(placeholders, get_global_folder_path(), export_folder)

        yaml_button = tk.Button(placeholder_frame, text="Yaml生成", bg="#4CAF50", fg="white", font=("Helvetica", 12), command=generate_yaml)
        yaml_button.pack(side=tk.LEFT, pady=10, padx=(0, 10))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def init_placeholder_app(root):
    # アプリケーションの初期化
    return MainApplication(root)

if __name__ == "__main__":
    # メインプログラムの実行
    root = tk.Tk()
    app = init_placeholder_app(root)
    root.mainloop()