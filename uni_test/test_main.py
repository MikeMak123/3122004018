import sys
import os

# 识别项目根目录下的模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import os
import subprocess
from main import preprocess, compute_similarity, write_result

class TestMain(unittest.TestCase):
    def setUp(self):
        """ 创建测试论文 """
        self.orig_file = "orig_test.txt"
        self.plagiarized_file = "plagiarized_test.txt"
        self.output_file = "ans_test.txt"

        with open(self.orig_file, "w", encoding="utf-8") as f:
            f.write("今天是星期天，天气晴，今天晚上我要去看电影。")

        with open(self.plagiarized_file, "w", encoding="utf-8") as f:
            f.write("今天是周天，天气晴朗，我晚上要去看电影。")

    def tearDown(self):
        """ 清理测试文件 """
        os.remove(self.orig_file)
        os.remove(self.plagiarized_file)
        os.remove(self.output_file)

    def test_main_cli(self):
        """ 测试正常文件 """
        result = subprocess.run(
            ["python", "main.py", self.orig_file, self.plagiarized_file, self.output_file],
            capture_output=True,
            text=True
        )

        # 读取结果
        with open(self.output_file, "r", encoding="utf-8") as f:
            result_value = float(f.read().strip())

        self.assertGreaterEqual(result_value, 0.0)
        self.assertLessEqual(result_value, 1.0)

    def test_main_empty_files(self):
        """ 测试空文件 """
        with open(self.orig_file, "w", encoding="utf-8") as f:
            f.write("")

        with open(self.plagiarized_file, "w", encoding="utf-8") as f:
            f.write("")

        result = subprocess.run(
            ["python", "main.py", self.orig_file, self.plagiarized_file, self.output_file],
            capture_output=True,
            text=True
        )

        with open(self.output_file, "r", encoding="utf-8") as f:
            result_value = float(f.read().strip())

        self.assertEqual(result_value, 0.0)  # 空文件相似度应为 0

if __name__ == "__main__":
    unittest.main()
