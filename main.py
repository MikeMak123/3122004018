from preprocess import preprocess
from similarity import compute_similarity
from utils import parse_args, write_result

if __name__ == "__main__":
    orig_file, plagiarized_file, output_file = parse_args()

    # 预处理
    orig_tokens = preprocess(orig_file)
    plagiarized_tokens = preprocess(plagiarized_file)

    # 计算相似度
    similarity_score = compute_similarity(orig_tokens, plagiarized_tokens, method="levenshtein")

    # 输出结果
    write_result(output_file, similarity_score)

    print(f"相似度计算完成: {similarity_score:.2f}")
