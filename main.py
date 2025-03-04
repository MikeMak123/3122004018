from preprocess import preprocess
from similarity import compute_similarity
from utils import parse_args, write_result, get_local_path

if __name__ == "__main__":
    # orig_file, plagiarized_file, output_file = parse_args()

    # 论文文件名（假设默认文件名）
    orig_file = get_local_path("orig.txt")
    plagiarized_file = get_local_path("orig_add.txt")
    output_file = get_local_path("ans.txt")

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
