from preprocess import preprocess
from similarity import compute_similarity
from utils import parse_args, write_result, get_local_path
import sys

def parse_args():
    """ 解析命令行参数 """
    if len(sys.argv) != 4:
        print("用法: python main.py [原文文件] [抄袭版论文] [答案文件]")
        exit(1)
    return sys.argv[1], sys.argv[2], sys.argv[3]

if __name__ == "__main__":
    orig_file, plagiarized_file, output_file = parse_args()

    # 运行命令： python main.py 'test_data\orig.txt' 'test_data\orig_add.txt' 'test_data\ans.txt' 

    # 论文文件名（假设默认文件名）
    # orig_file = get_local_path(r"test_data\orig.txt")
    # plagiarized_file = get_local_path(r"test_data\orig_add.txt")
    # output_file = get_local_path(r"test_data\ans.txt")

    # 预处理
    orig_tokens = preprocess(orig_file)
    plagiarized_tokens = preprocess(plagiarized_file)

    # 计算相似度
    similarity_score_1 = compute_similarity(orig_tokens, plagiarized_tokens, method="jaccard")
    similarity_score_2 = compute_similarity(orig_tokens, plagiarized_tokens, method="levenshtein")
    similarity_score_3 = compute_similarity(orig_tokens, plagiarized_tokens, method="cosine")

    # 输出结果
    write_result(output_file, similarity_score_1)
    write_result(output_file, similarity_score_2)
    write_result(output_file, similarity_score_3)

    print(f"jaccard相似度计算完成: {similarity_score_1:.2f}")
    print(f"levenshtein相似度计算完成: {similarity_score_2:.2f}")
    print(f"cosine相似度计算完成: {similarity_score_3:.2f}")
