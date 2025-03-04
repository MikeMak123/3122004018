import jieba
import re

def load_text(file_path):
    """ 读取文本文件 """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到")
        exit(1)
    except Exception as e:
        print(f"读取文件 {file_path} 失败: {e}")
        exit(1)

def clean_text(text):
    """ 清洗文本，去除标点符号，转为小写 """
    text = re.sub(r'[^\w\s]', '', text)  # 仅保留文字和空格
    text = re.sub(r'\s+', ' ', text).strip()  # 替换多个空格为单个空格，并去掉首尾空格
    return text.lower()

def tokenize(text):
    """ 分词，去除空格 """
    return [word for word in jieba.cut(text) if word.strip()]

def preprocess(file_path):
    """ 预处理文本：读取 -> 清洗 -> 分词 """
    raw_text = load_text(file_path)
    clean_text_data = clean_text(raw_text)
    return tokenize(clean_text_data)

def n_gram_split(tokens, n=3):
    """ 生成 n-gram 片段 """
    return {"".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)}