import sys
import os

def parse_args():
    """ 解析命令行参数 """
    if len(sys.argv) != 4:
        print("用法: python main.py [原文文件] [抄袭版论文] [答案文件]")
        exit(1)
    return sys.argv[1], sys.argv[2], sys.argv[3]

def write_result(file_path, similarity):
    """ 将相似度结果写入文件 """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"{similarity:.2f}\n")
    except Exception as e:
        print(f"写入文件 {file_path} 失败: {e}")
        exit(1)

def get_local_path(filename):
    """ 获取当前目录下的论文文件路径 """
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录
    file_path = os.path.join(base_dir, filename)
    
    if not os.path.exists(file_path):
        print(f"错误: 文件 {filename} 未找到")
        exit(1)
    return file_path