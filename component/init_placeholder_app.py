import tkinter as tk
from tkinter import ttk
from component.folder_operations import update_folder_list, folder_selected 
from component.display_gui import PlaceholderFrame
from component.analyze_placeholders import get_global_placeholders, get_global_settings

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("CloudFormation YAML プレースホルダー設定")
        self.root.geometry("800x600")
        self.root.configure(bg="#2e3f4f")
        
        self.init_main_frame()
        self.placeholder_frame = PlaceholderFrame(self.root, self.show_main_frame)

    def init_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg="#2e3f4f")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.folder_path = tk.StringVar()
        self.folder_var = tk.StringVar()
        
        self.folder_frame = tk.Frame(self.main_frame, bg="#2e3f4f")
        self.folder_frame.pack(pady=20)
        
        self.folder_label = tk.Label(self.folder_frame, text="フォルダを選択", fg="white", bg="#2e3f4f", font=("Helvetica", 14, "bold"))
        self.folder_label.pack(pady=10)
        
        self.folder_menu = ttk.OptionMenu(self.folder_frame, self.folder_var, "")
        self.folder_menu.pack(pady=10)
        
        self.placeholder_button = tk.Button(self.folder_frame, text="プレースホルダ設定", bg="#4CAF50", fg="white", font=("Helvetica", 12), command=self.show_placeholder_frame)
        self.placeholder_button.pack(pady=10)
        
        self.update_folder_list = update_folder_list.__get__(self)
        self.folder_selected = folder_selected.__get__(self)
        self.update_folder_list()

    def show_placeholder_frame(self):
        self.main_frame.pack_forget()
        self.placeholder_frame.pack(fill=tk.BOTH, expand=True)
        self.placeholder_frame.display_placeholders_in_gui(get_global_placeholders(), get_global_settings())

    def show_main_frame(self):
        self.placeholder_frame.pack_forget()
        self.main_frame.pack(fill=tk.BOTH, expand=True)

def init_placeholder_app(root):
    return MainApplication(root)