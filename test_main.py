import unittest
import os
from main import preprocess, compute_similarity, write_result

class TestMain(unittest.TestCase):
    def test_end_to_end(self):
        # 创建测试论文
        with open("orig.txt", "w", encoding="utf-8") as f:
            f.write("今天是星期天，天气晴，今天晚上我要去看电影。")

        with open("orig_add.txt", "w", encoding="utf-8") as f:
            f.write("今天是周天，天气晴朗，我晚上要去看电影。")

        # 预处理
        orig_tokens = preprocess("orig.txt")
        plagiarized_tokens = preprocess("orig_add.txt")

        # 计算相似度
        similarity_score = compute_similarity(orig_tokens, plagiarized_tokens, method="jaccard")

        # 写入结果
        output_file = "ans.txt"
        write_result(output_file, similarity_score)

        # 读取结果并检查
        with open(output_file, "r", encoding="utf-8") as f:
            result = float(f.read().strip())

        self.assertAlmostEqual(result, similarity_score, places=2)

        # 清理测试文件
        os.remove("orig.txt")
        os.remove("orig_add.txt")
        os.remove(output_file)

if __name__ == "__main__":
    unittest.main()
