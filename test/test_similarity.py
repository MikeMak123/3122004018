import unittest
from similarity import levenshtein_distance, jaccard_similarity, cosine_similarity

class TestSimilarity(unittest.TestCase):
    def test_levenshtein_distance(self):
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("hello", "hello"), 0)
    
    def test_jaccard_similarity(self):
        self.assertAlmostEqual(jaccard_similarity(set("abc"), set("abd")), 2/3)
    
    def test_cosine_similarity(self):
        vec1, vec2 = {"a": 1, "b": 1}, {"a": 1, "c": 1}
        self.assertAlmostEqual(cosine_similarity(vec1, vec2), 0.5)

if __name__ == "__main__":
    unittest.main()
