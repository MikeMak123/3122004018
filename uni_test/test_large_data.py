import sys
import os

# 识别项目根目录下的模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import os
from preprocess import preprocess
from similarity import compute_similarity

class TestLargeDataSet(unittest.TestCase):
    def test_large_texts(self):
        """ 测试 5000 字大数据集的识别率 """
        orig_file = r"test_data/orig.txt"
        plag_file = r"test_data/orig_add.txt"

        if not os.path.exists(orig_file) or not os.path.exists(plag_file):
            self.skipTest("大数据集文件不存在，跳过此测试")

        # 预处理大文本
        orig_tokens = preprocess(orig_file)
        plagiarized_tokens = preprocess(plag_file)

        # 计算相似度
        similarity_score_1 = compute_similarity(orig_tokens, plagiarized_tokens, method="jaccard")
        similarity_score_2 = compute_similarity(orig_tokens, plagiarized_tokens, method="levenshtein")
        similarity_score_3 = compute_similarity(orig_tokens, plagiarized_tokens, method="cosine") 

        print(f"[Large Data Jaccard] Similarity: {(similarity_score_1 + similarity_score_2 + similarity_score_3)/3:.2f}")

        # 设定一个合理的相似度阈值，比如 0.5 以上认为抄袭
        self.assertGreaterEqual(similarity_score_1 + similarity_score_2 + similarity_score_3, 0.5)

if __name__ == "__main__":
    unittest.main()
