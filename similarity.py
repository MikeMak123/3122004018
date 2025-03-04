import math
from collections import Counter

def levenshtein_distance(s1, s2):
    """ 计算 Levenshtein 编辑距离 """
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]
    
    for i in range(len_s1 + 1):
        for j in range(len_s2 + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
    
    return dp[len_s1][len_s2]

def jaccard_similarity(set1, set2):
    """ 计算 Jaccard 相似度 """
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

def cosine_similarity(vec1, vec2):
    """ 计算余弦相似度 """
    dot_product = sum(vec1[key] * vec2.get(key, 0) for key in vec1)
    magnitude1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    magnitude2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
    return dot_product / (magnitude1 * magnitude2) if magnitude1 and magnitude2 else 0

def compute_similarity(text1, text2, method="jaccard"):
    """ 计算相似度，默认使用 jaccard """
    if method == "levenshtein":
        max_len = max(len(text1), len(text2))
        return 1 - levenshtein_distance(text1, text2) / max_len if max_len else 1
    elif method == "jaccard":
        return jaccard_similarity(set(text1), set(text2))
    elif method == "cosine":
        vec1, vec2 = Counter(text1), Counter(text2)
        return cosine_similarity(vec1, vec2)
    else:
        raise ValueError("未知的相似度计算方法")
