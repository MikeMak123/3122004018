import sys

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
