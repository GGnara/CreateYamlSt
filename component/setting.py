import yaml
import os
import re

def load_setting_file(file_path):
    """
    設定ファイルを読み込む関数
    :param file_path: 設定ファイルのパス
    :return: 設定内容を格納した辞書
    """
    # 絶対パスに変換
    abs_file_path = os.path.abspath(file_path)
    
    with open(abs_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # プレースホルダのせいでyamlとして読み込めないので、PLACEHOLDER以下を削除
    filtered_lines = []
    skip = False
    for line in lines:
        if line.strip().startswith('PLACEHOLDER:'):
            skip = True
        if not skip:
            filtered_lines.append(line)
    
    filtered_content = ''.join(filtered_lines)
    
    try:
        varoables = yaml.safe_load(filtered_content)
    except yaml.YAMLError as e:
        print(f"Error loading YAML file: {e}")
        return None
        
    Rtsetting = replace_placeholders(varoables, lines)  
    format_yaml_for_setting_placeholders(Rtsetting)

    return format_yaml_for_setting_placeholders(Rtsetting)


def replace_placeholders(varoables, settings):
    """
    設定ファイル内のプレースホルダを置換する関数
    :param varoables: 設定ファイルの変数辞書
    :param settings: 設定ファイルの内容
    :return: プレースホルダが置換された設定ファイルの内容
    """

    # プレースホルダの値で置き換え
    variables = varoables.get('VARIABLE', {})
    for key, value in variables.items():
        placeholder_pattern = re.compile(r'\{\{' + re.escape(key) + r'\}\}')
        for i, line in enumerate(settings):
            settings[i] = placeholder_pattern.sub(str(value), line)

    # Setting => Yamlファイル 変更前に行わないといけない処理
    process_formula(settings)

    # lineをyamlとして読み込む
    try:
        yaml_content = yaml.safe_load('\n'.join(settings))
    except yaml.YAMLError as e:
        print(f"Error loading YAML content: {e}")
        return settings

    # TYPEを含むkeyを出力
    def find_keys_with_type(yaml_dict):
        keys_with_type = []
        for key, value in yaml_dict.items():
            if isinstance(value, dict):
                if 'Type' in value:
                    type_value = value.get('TypeValue', None)
                    keys_with_type.append((key, value['Type'], type_value))
                keys_with_type.extend(find_keys_with_type(value))
        return keys_with_type

    keys_with_type = find_keys_with_type(yaml_content)

    for item in keys_with_type:
        key, type_value, type_value_extra = item  # 3つの値をアンパック
        # print(f"item: {item}, type_value: {type_value}, type_value_extra: {type_value_extra}")  # type_value を出力して確認

        if 'zeroPadding' == type_value:
            if key is not None:
                yaml_content = process_zero_padding(key, value, type_value_extra, yaml_content)
            else:
                print(f"Warning: Key '{key}' not found in yaml_content")

    return yaml_content

# TYPEがzeroPaddingの場合の処理
def process_zero_padding(key, value, type_value, yaml_content):
    def set_default_value(yaml_content, key, type_value):
        """
        yaml_contentの中から 引数のkeyとkeyが合致するものの中の Default の値を書き換える
        :param yaml_content: YAMLファイルの内容の辞書
        :param key: 検索するキー
        :param type_value: 0パッティングの値
        """
        if not isinstance(yaml_content, dict):
            return False
        if key in yaml_content and 'Default' in yaml_content[key]:
            yaml_content[key]['Default'] = str(yaml_content[key]['Default']).zfill(type_value)
            return True
        for k, v in yaml_content.items():
            if isinstance(v, dict):
                result = set_default_value(v, key, type_value)
                if result:
                    return True
        return False

    set_default_value(yaml_content, key, type_value)
    return yaml_content

# Yaml生成前・計算作業
def process_formula(settings):

    # settingsの中に[]で囲まれたものがあるかどうかチェック
    bracket_pattern = re.compile(r'\[(.*?)\]')
    for i, line in enumerate(settings):
        while True:
            match = bracket_pattern.search(line)
            if not match:
                break
            expression = match.group(1)
            try:
                # 四則演算を実行
                result = eval(expression)
                # 計算結果で置き換え
                line = line[:match.start()] + str(result) + line[match.end():]
            except Exception as e:
                print(f"Error evaluating expression '{expression}': {e}")
                break
        settings[i] = line
    return settings

def format_yaml_for_setting_placeholders(Rtsetting):
        # TYPEを含むkeyを出力
    def find_keys_with_default(yaml_dict):
        keys_with_default = []
        for key, value in yaml_dict.items():
            if isinstance(value, dict):
                if 'Default' in value:
                    keys_with_default.append((key, value['Default']))
                keys_with_default.extend(find_keys_with_default(value))
        return keys_with_default

    return find_keys_with_default(Rtsetting)