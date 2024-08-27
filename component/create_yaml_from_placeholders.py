import os
import sys
import yaml

def generate_yaml_from_placeholders(placeholders, template_path, output_folder_name='export'):
    """
    プレースホルダをもとにYAMLを生成する関数

    :param placeholders: プレースホルダと値の辞書
    :param template_path: テンプレートYAMLファイルのパス
    :param output_folder_name: 出力フォルダ名（デフォルトは'export'）
    """
    # exeファイルまたはスクリプトのディレクトリを取得
    if getattr(sys, 'frozen', False):
        # exeファイルの場合
        base_path = os.path.dirname(sys.executable)
    else:
        # スクリプトの場合
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 出力フォルダのパスを設定
    output_path = os.path.join(base_path, output_folder_name)
    
    # 出力フォルダが存在しない場合は作成
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # テンプレートパス内のYAMLファイルを取得（setting.yamlを除く）
    yaml_files = [f for f in os.listdir(template_path) if f.endswith('.yaml') and f != 'setting.yaml']

    yaml_contents = []

    for yaml_file in yaml_files:
        file_path = os.path.join(template_path, yaml_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                template_content = file.read()
            
            yaml_contents.append([yaml_file, template_content])
            print(f"読み込んだYAMLファイル: {yaml_file}")
        except Exception as e:
            print(f"{yaml_file}の読み込み中にエラーが発生しました: {e}")
    
    # プレースホルダーを置き換える
    for i, (yaml_file, content) in enumerate(yaml_contents):
        for placeholder, value in placeholders.items():
            content = content.replace(f"{{{{{placeholder}}}}}", str(value))
        yaml_contents[i] = [yaml_file, content]
    
    # 置き換えた内容を出力ファイルに書き込む
    for yaml_file, content in yaml_contents:
        output_file_name = os.path.splitext(yaml_file)[0] + "Replaced.yaml"
        output_file_path = os.path.join(output_path, output_file_name)
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(content)
        print(f"生成されたYAMLファイル: {output_file_path}")
