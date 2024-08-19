import tkinter as tk
from tkinter import ttk

class PlaceholderFrame(tk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master)
        self.master = master
        self.return_callback = return_callback

    def display_placeholders_in_gui(self, all_placeholders, settings):
        # 既存のウィジェットをクリア
        for widget in self.winfo_children():
            widget.destroy()

        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        entries = {}

        for placeholder in all_placeholders:
            label = tk.Label(scrollable_frame, text=placeholder)
            label.pack(side=tk.TOP, anchor='w')
            entry = tk.Entry(scrollable_frame, width=80)
            for key, value in settings:
                if placeholder == key:
                    entry.insert(0, value)
                    break
            entry.pack(side=tk.TOP, anchor='w')
            entries[placeholder] = entry

        def save_placeholders():
            placeholders = {placeholder: entry.get() for placeholder, entry in entries.items()}
            print("プレースホルダが保存されました")
            print("保存されたプレースホルダ:")
            for placeholder, value in placeholders.items():
                print(f"{placeholder}: {value}")
            self.return_callback(placeholders)

        save_button = tk.Button(scrollable_frame, text="プレースホルダ保存", command=save_placeholders)
        save_button.pack(side=tk.BOTTOM, pady=10)

        return_button = tk.Button(scrollable_frame, text="戻る", command=self.return_callback)
        return_button.pack(side=tk.BOTTOM, pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")