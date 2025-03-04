import unittest
from preprocess import clean_text, tokenize, n_gram_split

class TestPreprocess(unittest.TestCase):
    def test_clean_text(self):
        self.assertEqual(clean_text("Hello, World!"), "hello world")
        self.assertEqual(clean_text("Python3.9 is great."), "python39 is great")
    
    def test_tokenize(self):
        self.assertEqual(tokenize("今天是星期天"), ["今天", "是", "星期天"])
    
    def test_n_gram_split(self):
        tokens = ["今天", "天气", "晴朗"]
        ngram_set = n_gram_split(tokens, 2)
        self.assertIn("今天天气", ngram_set)
        self.assertIn("天气晴朗", ngram_set)
    
if __name__ == "__main__":
    unittest.main()
