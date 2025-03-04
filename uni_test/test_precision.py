import sys
import os

# 识别项目根目录下的模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from preprocess import preprocess
from similarity import compute_similarity

def calculate_precision(similarity_func, orig_tokens, plagiarized_tokens, unrelated_tokens, threshold=0.5):
    """
    计算查重算法的识别率（Precision）。
    - similarity_func: 相似度计算方法
    - orig_tokens: 原始文本分词结果
    - plagiarized_tokens: 抄袭文本分词结果（应判为高相似度）
    - unrelated_tokens: 完全无关文本（应判为低相似度）
    - threshold: 判定为抄袭的阈值
    """
    # 计算相似度
    plagiarized_score = similarity_func(orig_tokens, plagiarized_tokens)  # 应高
    unrelated_score = similarity_func(orig_tokens, unrelated_tokens)  # 应低

    # 判定TP 和 FP
    TP = 1 if plagiarized_score >= threshold else 0
    FP = 1 if unrelated_score >= threshold else 0

    # 计算准确率
    return TP / (TP + FP) if (TP + FP) > 0 else 1.0  # 防止除0

class TestPrecision(unittest.TestCase):
    def setUp(self):
        """ 初始化测试数据 """
        self.orig_tokens = preprocess(r"test_data/orig.txt")
        self.plagiarized_tokens = preprocess(r"test_data/orig_add.txt")
        self.unrelated_tokens = preprocess(r"test_data/unrelated.txt")

    def test_jaccard_precision(self):
        precision = calculate_precision(lambda x, y: compute_similarity(x, y, "jaccard"),
                                        self.orig_tokens, self.plagiarized_tokens, self.unrelated_tokens)
        print(f"Jaccard Precision: {precision:.2f}")
        self.assertGreaterEqual(precision, 0.5)

    def test_levenshtein_precision(self):
        precision = calculate_precision(lambda x, y: compute_similarity(x, y, "levenshtein"),
                                        self.orig_tokens, self.plagiarized_tokens, self.unrelated_tokens)
        print(f"Levenshtein Precision: {precision:.2f}")
        self.assertGreaterEqual(precision, 0.5)

    def test_cosine_precision(self):
        precision = calculate_precision(lambda x, y: compute_similarity(x, y, "cosine"),
                                        self.orig_tokens, self.plagiarized_tokens, self.unrelated_tokens)
        print(f"Cosine Precision: {precision:.2f}")
        self.assertGreaterEqual(precision, 0.5)

    def test_overall_precision(self):
        """ 计算综合查重率指标 """
        jaccard_precision = calculate_precision(lambda x, y: compute_similarity(x, y, "jaccard"),
                                                self.orig_tokens, self.plagiarized_tokens, self.unrelated_tokens)
        levenshtein_precision = calculate_precision(lambda x, y: compute_similarity(x, y, "levenshtein"),
                                                    self.orig_tokens, self.plagiarized_tokens, self.unrelated_tokens)
        cosine_precision = calculate_precision(lambda x, y: compute_similarity(x, y, "cosine"),
                                               self.orig_tokens, self.plagiarized_tokens, self.unrelated_tokens)

        overall_precision = (jaccard_precision + levenshtein_precision + cosine_precision) / 3
        print(f"Overall Precision: {overall_precision:.2f}")
        self.assertGreaterEqual(overall_precision, 0.8)

if __name__ == "__main__":
    unittest.main()
