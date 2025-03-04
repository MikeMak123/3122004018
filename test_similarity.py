import unittest
from similarity import levenshtein_distance, jaccard_similarity, compute_similarity
from preprocess import n_gram_split

class TestSimilarity(unittest.TestCase):
    def test_levenshtein_distance(self):
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("hello", "hello"), 0)
    
    def test_jaccard_similarity(self):
        set1 = n_gram_split(["abc", "def", "ghi"], 2)  # {"abcdef", "defghi"}
        set2 = n_gram_split(["abc", "def", "xyz"], 2)  # {"abcdef", "defxyz"}
        self.assertAlmostEqual(jaccard_similarity(set1, set2), 1/3)

    def test_compute_similarity(self):
        set1 = n_gram_split(["abc", "def", "ghi"], 2)
        set2 = n_gram_split(["abc", "def", "xyz"], 2)
        self.assertAlmostEqual(compute_similarity(set1, set2, "jaccard"), 1/2)

if __name__ == "__main__":
    unittest.main()
