import os
import tkinter as tk
from tkinter import messagebox
from component.analyze_placeholders import analyze_placeholders  

# yamlファイル配下のフォルダセットを取得、プルダウンに生成
def update_folder_list(self):
    # yaml配下のフォルダの名前を一斉に取得
    yaml_folder = os.path.join(os.path.dirname(__file__), '..', 'yaml')  # 修正: 一つ上のディレクトリに変更
    print(f"YAMLフォルダのパス: {yaml_folder}")  # 変更: YAMLフォルダのパスをコンソールに出力
    if os.path.exists(yaml_folder):
        yaml_subfolders = [f for f in os.listdir(yaml_folder) if os.path.isdir(os.path.join(yaml_folder, f))]
        # プルダウンメニューをクリア
        self.folder_menu['menu'].delete(0, 'end')
        for folder in yaml_subfolders:
            folder_path = os.path.join(yaml_folder, folder)
            try:
                # プルダウンメニューにフォルダ名を追加
                self.folder_menu['menu'].add_command(label=folder, command=tk._setit(self.folder_var, folder, self.folder_selected)) 
            except Exception as exc:
                print("エラーが発生しました。")  # 追加: エラーメッセージの前に適当なメッセージを出力
                messagebox.showerror("エラー", f"フォルダの取得中にエラーが発生しました: {exc}")
    else:
        print(f"YAMLフォルダが存在しません: {yaml_folder}")  # 追加: YAMLフォルダが存在しない場合のメッセージをコンソールに出力

# プルダウンが選択されたときの処理
def folder_selected(self, value):
    
    # フォルダが選択されたときの処理
    self.folder_path.set(value)
    self.update_folder_list()
    
    # フォルダの中身にあるyamlファイルをすべて読み取る（setting.yamlを除く）
    folder_path = os.path.join(os.path.dirname(__file__), '..', 'yaml', value)  # 修正: 一つ上のディレクトリに変更
    if os.path.exists(folder_path):
        yaml_files = [f for f in os.listdir(folder_path) if f.endswith('.yaml') and f != 'setting.yaml']
        yaml_contents = []  # 追加: YAMLコンテンツを格納する配列
        for yaml_file in yaml_files:
            file_path = os.path.join(folder_path, yaml_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    yaml_contents.append(content) 
                    print(f"ローディングYaml:{yaml_file}")
            except Exception as exc:
                print(f"{yaml_file}の読み取り中にエラーが発生しました: {exc}")
    else:
        print(f"フォルダが存在しません: {folder_path}")
    # YAMLコンテンツを配列のままanalyze_placeholdersに引き渡し、プレースホルダを分析
    analyze_placeholders(yaml_contents, folder_path)
    
    # print("プレースホルダのリスト:")
    # for placeholders in all_placeholders:
    #     print(placeholders)
