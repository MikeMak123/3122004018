import sys
import os

# 识别项目根目录下的模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import os
import subprocess
from main import preprocess, compute_similarity, write_result

class TestMain(unittest.TestCase):
    def test_end_to_end(self):
        # 创建测试论文
        orig_content = "今天是星期天，天气晴，今天晚上我要去看电影。"
        plagiarized_content = "今天是周天，天气晴朗，我晚上要去看电影。"

        with open(r"orig_test.txt", "w", encoding="utf-8") as f:
            f.write(orig_content)

        with open(r"plagiarized_test.txt", "w", encoding="utf-8") as f:
            f.write(plagiarized_content)

        output_file = r"ans_test.txt"

        # 运行 main.py
        result = subprocess.run(
            ["python", "main.py", "orig_test.txt", "plagiarized_test.txt", output_file],
            capture_output=True,
            text=True
        )

        # 读取结果并检查
        with open(output_file, "r", encoding="utf-8") as f:
            result_value = float(f.read().strip())

        self.assertGreaterEqual(result_value, 0.0)
        self.assertLessEqual(result_value, 1.0)

        # 清理测试文件
        os.remove("orig_test.txt")
        os.remove("plagiarized_test.txt")
        os.remove(output_file)

if __name__ == "__main__":
    unittest.main()
