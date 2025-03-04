import sys
import os

# 识别项目根目录下的模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from preprocess import clean_text, tokenize, n_gram_split

class TestPreprocess(unittest.TestCase):
    def test_clean_text(self):
        self.assertEqual(clean_text("Hello, World!"), "hello world")
        self.assertEqual(clean_text("Python3.9 is great."), "python39 is great")
        self.assertEqual(clean_text("你好，世界！"), "你好世界")  # 中文符号清除
        self.assertEqual(clean_text("   多个    空格  "), "多个 空格")  # 多空格处理
        self.assertEqual(clean_text(""), "")  # 处理空字符串
    
    def test_tokenize(self):
        self.assertEqual(tokenize("今天是星期天"), ["今天", "是", "星期天"])
        self.assertEqual(tokenize("Python3 是很棒的语言"), ["Python3", "是", "很棒", "的", "语言"])
        self.assertEqual(tokenize(" "), [])  # 处理纯空格输入
        self.assertEqual(tokenize(""), [])  # 处理空字符串
        self.assertEqual(tokenize("Python 语言"), ["Python", "语言"])  # 确保去掉中间空格
    
    def test_n_gram_split(self):
        tokens = ["今天", "天气", "晴朗"]
        self.assertEqual(n_gram_split(tokens, 2), {"今天天气", "天气晴朗"})
        self.assertEqual(n_gram_split(tokens, 3), {"今天天气晴朗"})
        self.assertEqual(n_gram_split(tokens, 4), set())  # 过大 n 值应该返回空集合
        self.assertEqual(n_gram_split([], 2), set())  # 空输入
    
if __name__ == "__main__":
    unittest.main()
