# -*- coding: utf-8 -*-
# @File : chunk_split.py
# @Author : zh
# @Time : 2024/4/9 15:38
# @Desc : 数据处理过程中涉及到的文件操作
import json
import os


def process_txt_file(filepath, encodings=['utf-8', 'gb18030', 'gbk', 'gb2312', 'latin-1', 'ascii']):
    """
    尝试使用不同的编码读取和转换文本文件。
    @param filepath:  待处理的txt文件路径
    @param encodings:  尝试的编码列表
    @return:  返回处理后的文本数据
    """
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
            # 成功读取后转换编码到utf-8（如果已经是utf-8则不需要转换）
            return content.encode('utf-8').decode('utf-8')
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Failed to decode {filepath} with given encodings.")

def process_folder_and_save_to_jsonl(folder_path, output_file):
    """
    递归遍历文件夹，处理每个txt文件，然后将数据保存为一整个JSONL格式。
    @param folder_path: 待转换的txt文本路径
    @param output_file: 输出文件路径
    @return:
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                try:
                    text_data = process_txt_file(filepath)
                    with open(output_file, 'a', encoding='utf-8') as fp:
                        fp.write(json.dumps({"text": text_data}, ensure_ascii=False) + '\n')
                    print(f"Processed and saved {file} successfully.")
                except UnicodeDecodeError as e:
                    print(e)



