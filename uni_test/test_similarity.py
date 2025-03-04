import sys
import os

# 识别项目根目录下的模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from preprocess import n_gram_split
from similarity import levenshtein_distance, jaccard_similarity, cosine_similarity, compute_similarity 

class TestSimilarity(unittest.TestCase):
    def test_n_gram(self):
        tokens = ["今天", "天气", "晴朗"]
        ngram_set = n_gram_split(tokens, 2)
        self.assertIn("今天天气", ngram_set)
        self.assertIn("天气晴朗", ngram_set)

    def test_levenshtein_distance(self):
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("hello", "hello"), 0)
    
    def test_jaccard_similarity(self):
        set1 = n_gram_split(["abc", "def", "ghi"], 2)  # 生成 {"abcdef", "defghi"}
        set2 = n_gram_split(["abc", "def", "xyz"], 2)  # 生成 {"abcdef", "defxyz"}
        self.assertAlmostEqual(jaccard_similarity(set1, set2), 1/3)

    def test_jaccard_similarity(self):
        set1 = {"今天天气", "天气晴朗", "晴朗很好"}
        set2 = {"天气晴朗", "晴朗很好", "很好真好"}
        self.assertAlmostEqual(compute_similarity(set1, set2, "jaccard"), 1/2)
    
    def test_cosine_similarity(self):
        vec1, vec2 = {"a": 1, "b": 1}, {"a": 1, "c": 1}
        self.assertAlmostEqual(cosine_similarity(vec1, vec2), 0.5)

if __name__ == "__main__":
    unittest.main()
