import unittest
import os
from utils import write_result, get_local_path

class TestUtils(unittest.TestCase):
    def test_write_result(self):
        test_file = "test_output.txt"
        write_result(test_file, 0.85)

        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        self.assertEqual(content, "0.85")
        os.remove(test_file)  # 清理测试文件
    
    def test_get_local_path(self):
        test_file = "test_file.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("test content")

        self.assertTrue(os.path.exists(get_local_path(test_file)))
        os.remove(test_file)  # 清理测试文件

if __name__ == "__main__":
    unittest.main()
