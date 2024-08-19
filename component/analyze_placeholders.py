import re
import os
from component.setting import load_setting_file, replace_placeholders

# グローバル変数でプレースホルダ、setting、folder_pathの値を保存
global_placeholders = None
global_settings = None
global_folder_path = None

def analyze_placeholders(yaml_content, folder_path):
    """
    YAMLコンテンツ内のプレースホルダを分析し、プレースホルダのリストを返す関数
    :param yaml_content: YAMLファイルの内容の配列
    :param folder_path: YAMLファイルが存在するフォルダのパス
    :return: プレースホルダのリストの配列
    """
    global global_placeholders, global_settings, global_folder_path
    
    # プレースホルダのパターンを定義
    placeholder_pattern = re.compile(r'\{\{(.*?)\}\}')
    
    all_placeholders = []
    
    for content in yaml_content:
        # プレースホルダを検索
        placeholders = placeholder_pattern.findall(content)
        all_placeholders.extend(placeholders)
    
    # 重複を除外
    unique_placeholders = list(set(all_placeholders))
    
    # 設定ファイルのパスを指定
    setting_file_path = os.path.join(folder_path, 'setting.yaml')
    
    # デバッグ用にパスを出力
    # print(f"設定ファイルのパス: {setting_file_path}")

    # 設定ファイルを読み込む
    settings = load_setting_file(setting_file_path)

    # 設定内容を表示（デバッグ用）
    print(settings)

    # グローバル変数に保存
    global_placeholders = unique_placeholders
    global_settings = settings
    global_folder_path = folder_path

# 他の関数からグローバル変数にアクセスするための関数
def get_global_placeholders():
    return global_placeholders

def get_global_settings():
    return global_settings

def get_global_folder_path():
    return global_folder_path