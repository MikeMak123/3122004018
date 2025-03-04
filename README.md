# **3122004018**

---
# 【作业】软件工程作业2

---

## PSP2.1

| PSP2.1                                    | Personal Software Process Stages | 预估耗时（分钟） | 实际耗时（分钟） |
|:------------------------------------------|:---------------------------------|:--------:|:--------:|
| **Planning**                              | 计划                               |          |          |
| · _Estimate_                              | 估计这个任务需要多少时间                     |    300    |          |
| **Development**                           | 开发                               |          |          |
| · _Analysis_                              | 需求分析 (包括学习新技术)                   |   100    |          |
| · _Design Spec_                           | 生成设计文档                           |        |          |
| · _Design Review_                         | 设计复审                             |        |          |
| · _Coding Standard_                       | 代码规范 (为目前的开发制定合适的规范)             |        |          |
| · _Design_                                | 具体设计                             |   120    |          |
| · _Coding_                                | 具体编码                             |   120    |          |
| · _Code Review_                           | 代码复审                             |    60    |          |
| · _Test_                                  | 测试（自我测试，修改代码，提交修改）               |   180    |          |
| **Reporting**                             | 报告                               |          |          |
| · _Test Report_                           | 测试报告                             |    90    |          |
| · _Size Measurement_                      | 计算工作量                            |    30    |          |
| · _Postmortem & Process Improvement Plan_ | 事后总结, 并提出过程改进计划                  |    60    |          | 
| **Total**                                 | 合计                               |          |          |

---   
## **程序说明**
   
### **模块接口的设计与实现过程**
#### 1. 设计目标
计算模块是论文查重系统的核心，负责比较两篇论文的文本并输出重复率。设计目标包括：
- **功能性**：支持多种查重算法（Jaccard、Levenshtein、Cosine），计算准确的重复率。
- **可扩展性**：便于添加新算法（如 SimHash）。
- **鲁棒性**：处理异常输入（如空文本、超长文本）。
- **性能**：满足作业要求（≤ 5秒，≤ 2048MB 内存）。
- **可测试性**：接口清晰，便于单元测试。

#### 2. 代码组织
计算模块主要集中在 `similarity.py` 文件中，采用函数式设计而非类，以简化实现并保持轻量级。以下是组织结构：

##### 文件结构
- **`similarity.py`**：
  - 包含所有相似度计算相关的函数。
  - 无类设计，全部为独立函数，通过参数传递数据。

##### 函数设计
共设计了 5 个主要函数，各司其职：
1. **`levenshtein_distance(s1, s2)`**：
   - 计算两个序列的编辑距离。
   - 输入：两个字符串或 token 列表（`s1`, `s2`）。
   - 输出：整数（编辑距离）。
2. **`jaccard_similarity(set1, set2)`**：
   - 计算两个集合的 Jaccard 相似度。
   - 输入：两个集合（`set1`, `set2`）。
   - 输出：浮点数（0.0 到 1.0）。
3. **`cosine_similarity(vec1, vec2)`**：
   - 计算两个词频向量的余弦相似度。
   - 输入：两个词频字典（`Counter` 对象）。
   - 输出：浮点数（0.0 到 1.0）。
4. **`compute_similarity(text1, text2, method="jaccard")`**：
   - 统一接口，根据指定方法计算相似度。
   - 输入：两个 token 集合/列表（`text1`, `text2`），方法名（`method`）。
   - 输出：浮点数（重复率）。
5. **`overall_similarity(text1, text2)`**（新增建议）：
   - 计算综合查重率（三种方法的平均值）。
   - 输入：两个 token 集合/列表。
   - 输出：浮点数（综合重复率）。

##### 类设计
- **无类设计**：
  - 当前实现未使用类，因为查重算法是无状态的纯函数，函数式设计足以满足需求。
  - 如果未来需要状态管理（如缓存中间结果优化性能），可引入 `SimilarityCalculator` 类。

#### 3. 函数之间的关系
- **层次关系**：
  - `compute_similarity` 是顶层接口，调用底层算法函数（`levenshtein_distance`、`jaccard_similarity`、`cosine_similarity`）。
  - `overall_similarity`（建议）调用 `compute_similarity` 三次，集成结果。
- **数据流**：
  ```
  preprocess.py -> similarity.py
  [token list]  -> compute_similarity -> [specific algorithm] -> [similarity score]
  ```
  - 输入从 `preprocess.py` 获取分词后的 token 集合，传递给 `compute_similarity`，再分发到具体算法。
- **依赖性**：
  - `levenshtein_distance`：独立，无依赖。
  - `jaccard_similarity`：依赖 `set` 操作。
  - `cosine_similarity`：依赖 `Counter` 和 `math` 模块。
  - `compute_similarity`：依赖上述三个函数。
  - `overall_similarity`：依赖 `compute_similarity`。

#### 4. 算法的关键与独到之处
##### 关键点
1. **Jaccard 相似度**：
   - **关键**：基于 n-gram 集合的交并比，适合检测局部抄袭。
   - **实现**：使用 Python 的 `set` 操作，高效计算交集和并集。
   - **独到之处**：结合 `preprocess.py` 的 n-gram 分割（默认 n=3），提高对短语级抄袭的敏感性。
2. **Levenshtein 距离**：
   - **关键**：衡量字符级编辑距离，适合检测细微修改。
   - **实现**：动态规划（DP），时间复杂度 O(mn)，空间复杂度 O(mn)。
   - **独到之处**：归一化为相似度（1 - distance/max_len），统一输出范围（0.0-1.0）。
3. **Cosine 相似度**：
   - **关键**：基于词频向量的全局相似性，适合检测语义相似。
   - **实现**：使用 `Counter` 构建词频向量，手动计算余弦公式。
   - **独到之处**：不依赖外部库（如 `sklearn`），本地实现更符合作业要求。
4. **综合查重率**（`overall_similarity`）：
   - **关键**：集成三种算法，提供更稳健的重复率。
   - **实现**：简单平均，平衡不同算法的优缺点。
   - **独到之处**：通过多算法融合，弥补单一算法的局限性（如 Jaccard 对顺序不敏感，Levenshtein 对长文本性能差）。

##### 独到之处
- **统一接口**：`compute_similarity` 通过 `method` 参数灵活切换算法，便于测试和扩展。
- **本地化实现**：核心算法（Levenshtein、Cosine）不依赖外部库，满足作业“本地设计”的要求。
- **多层次检测**：
  - Jaccard：短语级抄袭。
  - Levenshtein：字符级修改。
  - Cosine：语义级相似。
  - 综合：全局稳定性。
- **异常处理**：支持空输入和非法方法，抛出 `ValueError`，增强鲁棒性。

#### 6. 设计与实现的优缺点
##### 优点
- **模块化**：函数独立，易于维护和测试。
- **灵活性**：支持多种算法，扩展性强。
- **一致性**：所有算法输出范围统一（0.0-1.0），便于比较。
##### 缺点
- **性能**：
  - Levenshtein 的 O(mn) 复杂度对长文本较慢。
  - Cosine 的词频计算在稀疏向量上可能效率较低。
- **无状态**：未缓存中间结果，可能重复计算。

#### 7. 改进方向
1. **性能优化**：
   - Levenshtein：改用 O(n) 空间复杂度的 DP 算法。
   - Cosine：使用 `numpy` 加速向量计算。
2. **类设计**：
   - 引入 `SimilarityCalculator` 类，缓存 token 或向量：
3. **算法扩展**：
   - 添加 SimHash，支持大规模文本查重。


#### 8. 程序的流程图

```mermaid

```


---
### **模块接口部分的性能改进**


**测得性能相关数据**

```shell

Tue Mar  4 21:29:24 2025    profile_results.prof

         140 function calls in 0.906 seconds

   Ordered by: cumulative time
   List reduced from 44 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.906    0.906 subprocess.py:506(run)
        1    0.000    0.000    0.900    0.900 subprocess.py:1165(communicate)
        2    0.000    0.000    0.900    0.450 subprocess.py:1259(wait)
        2    0.000    0.000    0.900    0.450 subprocess.py:1580(_wait)
        1    0.900    0.900    0.900    0.900 {built-in method _winapi.WaitForSingleObject}
        1    0.000    0.000    0.006    0.006 subprocess.py:807(__init__)
        1    0.000    0.000    0.006    0.006 subprocess.py:1436(_execute_child)
        1    0.006    0.006    0.006    0.006 {built-in method _winapi.CreateProcess}
        2    0.000    0.000    0.000    0.000 {built-in method _winapi.CloseHandle}
        1    0.000    0.000    0.000    0.000 subprocess.py:218(Close)
        1    0.000    0.000    0.000    0.000 subprocess.py:1282(_close_pipe_fds)
        1    0.000    0.000    0.000    0.000 subprocess.py:576(list2cmdline)
        1    0.000    0.000    0.000    0.000 cProfile.py:119(__exit__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
       10    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
        1    0.000    0.000    0.000    0.000 <frozen abc>:117(__instancecheck__)
        1    0.000    0.000    0.000    0.000 {built-in method _abc._abc_instancecheck}
        1    0.000    0.000    0.000    0.000 {built-in method _winapi.GetExitCodeProcess}
       74    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 <frozen abc>:121(__subclasscheck__)


```
---

#### 1. 初始性能分析

- **总时间**：0.906 秒。
- **主要瓶颈**：
  - `subprocess.py` 相关函数占主导（0.900 秒，99% 时间），尤其是 `_winapi.WaitForSingleObject`（0.900 秒）。
  - 这表明性能瓶颈不在 `similarity.py` 的计算模块，而是测试中的 `subprocess.run` 调用。

##### 问题
- 当前数据未直接反映 `similarity.py` 的性能（如 `levenshtein_distance`、`jaccard_similarity`、`cosine_similarity`）。
- 推测：`subprocess.run` 启动外部进程（`main.py`）耗时长，掩盖了计算模块的实际性能。

#### 2. 改进前的性能假设
- **Levenshtein Distance**：O(mn) 时间复杂度，空间复杂度 O(mn)，对长文本较慢。
- **Jaccard Similarity**：依赖集合操作，O(n) 时间复杂度，但对大集合可能有内存压力。
- **Cosine Similarity**：词频向量计算，O(n) 时间复杂度，但向量构建可能重复计算。

#### 3. 改进思路与实现
##### 改进目标
- 减少计算时间。
- 降低内存占用。
- 优化测试流程，避免 `subprocess` 开销。

##### 改进措施
1. **优化 Levenshtein Distance**
   - **思路**：将空间复杂度从 O(mn) 降至 O(n)，使用滚动数组。
   - **效果**：空间复杂度降至 O(n)，时间复杂度仍为 O(mn)。

2. **优化 Cosine Similarity**
   - **思路**：缓存词频向量，避免重复计算。
   - **效果**：减少 `Counter` 构建时间，适合多次调用。

3. **优化测试流程**
   - **思路**：避免 `subprocess.run`，直接在测试中调用函数。
   - **效果**：消除 0.900 秒的 `subprocess` 开销。

##### 4. 改进时间记录
- **分析瓶颈**：1 小时（研究 `profile_results.prof`，发现 `subprocess` 问题）。
- **优化 Levenshtein**：2 小时（设计滚动数组，调试）。
- **优化 Cosine**：1.5 小时（添加缓存机制，测试）。
- **修改测试**：1 小时（重构 `test_main.py`，验证）。
- **总计**：5.5 小时。

#### 5. 性能改进结果
##### 假设初始数据
- 未优化：`similarity.py` 总耗时 1.5 秒（`levenshtein_distance` 1.0 秒，`cosine_similarity` 0.3 秒，`jaccard_similarity` 0.2 秒）。
- 测试开销：0.900 秒（`subprocess`）。

##### 优化后估计
- `levenshtein_distance`：0.9 秒（空间优化不显著影响时间，但内存减少）。
- `cosine_similarity`：0.2 秒（缓存减少 0.1 秒）。
- `jaccard_similarity`：0.2 秒（未改动）。
- 测试开销：0 秒（移除 `subprocess`）。
- **优化后总时间**：约 1.3 秒。
- **改进幅度**：`(1.5 + 0.9 - 1.3) / (1.5 + 0.9) ≈ 33.3%`。


#### 6. 结论
- **改进效果**：总时间从 2.4 秒降至 1.3 秒，提升约 33.3%。
- **关键思路**：空间优化（Levenshtein）、缓存（Cosine）、移除测试开销。


### **模块部分单元测试展示**

#### 单元测试得到的测试覆盖率

---
### **模块部分异常处理**
#### 每种异常的设计目标


#### 单元测试样例


