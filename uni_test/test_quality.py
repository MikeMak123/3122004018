import sys
import os
import subprocess

'''使用性能分析工具Studio Profiling Tools来找出代码中的性能瓶颈并进行改进。'''

# 识别项目根目录下的模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import main

# 性能分析相关库
import cProfile
import pstats

if __name__ == "__main__":
    with cProfile.Profile() as pr:
        # main.main()      
        subprocess.run(
                ["python", "main.py", r'test_data\orig.txt', r'test_data\orig_add.txt', r'test_data\ans.txt'])
        
    # 运行命令： python main.py 'test_data\orig.txt' 'test_data\orig_add.txt' 'test_data\ans.txt' 

    # 保存性能分析结果到文件
    pr.dump_stats("profile_results.prof")

    # 打印分析结果
    stats = pstats.Stats("profile_results.prof")
    stats.strip_dirs().sort_stats("cumulative").print_stats(20)  # 显示前 20 个函数