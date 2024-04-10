import json

def read_json(file_path):
    '''读取json'''
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(file_path, data):
    '''写入json'''
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)