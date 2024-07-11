import tkinter as tk
from tkinter import messagebox, filedialog
import os
import re
import yaml

class PlaceholderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CloudFormation YAML プレースホルダー設定")
        self.root.geometry("600x400")
        
        self.file_var = tk.StringVar()
        self.file_menu = tk.OptionMenu(root, self.file_var, "")
        self.file_menu.pack(pady=20)
        
        self.load_button = tk.Button(root, text="YAMLファイルを読み込む", command=self.load_yaml_file)
        self.load_button.pack(pady=20)
        
        self.placeholder_frame = tk.Frame(root)
        self.placeholder_frame.pack(pady=20)
        
        self.update_file_list()
    
    def update_file_list(self):
        files = [f for f in os.listdir('yaml') if f.endswith(('.yaml', '.yml'))]
        self.file_var.set(files[0] if files else '')
        self.file_menu['menu'].delete(0, 'end')
        for file in files:
            self.file_menu['menu'].add_command(label=file, command=tk._setit(self.file_var, file))
    
    def load_yaml_file(self):
        selected_file = self.file_var.get()
        file_path = os.path.join('yaml', selected_file)
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.yaml_content = file.read()
                    placeholders = self.find_placeholders(self.yaml_content)
                    self.display_placeholders(placeholders)
            except Exception as exc:
                messagebox.showerror("エラー", f"YAMLの読み込み中にエラーが発生しました: {exc}")
    
    def find_placeholders(self, yaml_content):
        pattern = re.compile(r"\{\{(.*?)\}\}")
        return list(set(pattern.findall(yaml_content)))  # 重複を削除してリストに変換
    
    def display_placeholders(self, placeholders):
        for widget in self.placeholder_frame.winfo_children():
            widget.destroy()
        
        self.entries = {}
        
        for placeholder in placeholders:
            frame = tk.Frame(self.placeholder_frame)
            frame.pack(fill='x', pady=5)
            label = tk.Label(frame, text=placeholder, width=30, anchor='w')
            label.pack(side='left')
            entry = tk.Entry(frame)
            entry.pack(side='left', fill='x', expand=True)
            self.entries[placeholder] = entry
        
        self.save_button = tk.Button(self.root, text="YAMLファイルをエクスポート", command=self.export_yaml)
        self.save_button.pack(pady=20)
    
    def export_yaml(self):
        updated_content = self.yaml_content
        for placeholder, entry in self.entries.items():
            value = entry.get()
            if value:
                updated_content = updated_content.replace(f"{{{{{placeholder}}}}}", value)
        
        file_path = filedialog.asksaveasfilename(defaultextension=".yaml", filetypes=[("YAML files", "*.yaml")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_content)
                messagebox.showinfo("成功", "YAMLファイルがエクスポートされました。")
            except Exception as exc:
                messagebox.showerror("エラー", f"YAMLファイルのエクスポート中にエラーが発生しました: {exc}")
    
root = tk.Tk()
app = PlaceholderApp(root)
root.mainloop()
