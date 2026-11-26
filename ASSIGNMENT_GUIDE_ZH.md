# Assignment 1 中文导读

正式题目见 [README.md](README.md)，报告填在 [REPORT.md](REPORT.md)。下面按题号列出每题的代码、证明和实验要求。

## A 搜索算法（25 分）

| 小题 | 要做什么 |
| --- | --- |
| A1 Best-first、Greedy、A*、Weighted A* | 在 [algorithms/informed.py](algorithms/informed.py) 里写一个通用的 best-first search，用优先队列先扩展评分最低的节点。三个变体分别用 `h`、`g + h`、`g + w*h` 排序。这里 `g` 是从起点走到当前节点的实际代价，`h` 是到目标的估计代价。 |
| A2 IDA* | 在同一文件中实现按 `g + h` 限制的深度优先搜索。首轮阈值是起点的 `h`，下一轮用上一轮遇到的最小超限值。搜索时避开当前路径上重复的状态。 |
| A3 双向搜索 | 在 [algorithms/bidirectional.py](algorithms/bidirectional.py) 里从起点和目标两端做 BFS，每次完整扩展节点数更少的一层。相遇后拼出翻转次数最少的完整路径，并累计路径的实际代价。 |

## B 煎饼排序（25 分）

栈从顶到底表示。每一步可以把顶部 `k` 张煎饼反转，目标是让煎饼从小到大排列。四题都在 [problems/pancakes.py](problems/pancakes.py)。

| 小题 | 要做什么 |
| --- | --- |
| B1 问题建模 | 定义目标状态、目标判断、后继、前驱和动作代价。动作名是 `flip k`。两种计价规则分别是每次翻转花费 1，以及翻转 `k` 张花费 `k`。 |
| B2 Gap 启发式 | 数相邻大小差超过 1 的位置，栈底的盘子也算一张大小为 `n + 1` 的煎饼。在报告中证明单位代价下的可采纳性和一致性。可采纳性要求估计值至多等于到目标的最小代价。一致性要求沿一步移动，估计值下降的幅度至多等于该步代价。 |
| B3 自创启发式 | 实现 `my_heuristic`，用证明或反例分别判断其可采纳性和一致性，再用 A* 实验和 gap 启发式比较。 |
| B4 按翻转长度计费 | 判断 gap 在这个规则下是否仍可采纳。实现逐状态都至少与 gap 一样大的 `flip_cost_heuristic`，并证明它可采纳。 |

## C 局部搜索和遗传算法（25 分）

| 小题 | 要做什么 |
| --- | --- |
| C1 背包和图着色 | 在 [problems/knapsack.py](problems/knapsack.py) 用 0/1 列表表示选哪些物品，合法解的适应度是总价值，超重解的适应度是负的超重重量。在 [problems/coloring.py](problems/coloring.py) 用颜色列表表示各节点的颜色，以同色边数为代价、异色边数为适应度。按各文件说明补齐随机初始解、邻居、交叉和变异等操作。 |
| C2 局部搜索 | 在 [algorithms/local_search.py](algorithms/local_search.py) 实现三种方法。随机爬山每步随机选一个更好的邻居。随机重启从不同的随机起点多跑几轮，保留最好结果。局部束搜索同时维护 `k` 个候选，每轮从它们的全部邻居里选出最好的 `k` 个不同状态。 |
| C3 遗传算法 | 在 [algorithms/genetic.py](algorithms/genetic.py) 实现按名次分配选择权重的 `rank_selection`，以及保留精英、选择父母、交叉、按概率变异的 `evolve`。后者仅调用 `GeneticProblem` 的四个方法，能直接用于两个问题，并返回最终最优个体及各代的最佳适应度。 |

## D Prolog（10 分）

在 [prolog/pancakes.pl](prolog/pancakes.pl) 用关系谓词描述同一个煎饼排序问题。

- `flip/3` 描述一次前缀翻转，使用 `append/3` 和 `reverse/2` 等谓词。
- `move/3` 枚举当前栈的合法翻转动作和结果。
- `solve/2` 用深度优先搜索找翻转序列，`solve_id/2` 用迭代加深优先尝试较短的序列。
- `gaps/2` 计算包括盘子在内的 gap 数。

## 报告（15 分）

用 Moodle 上的组号替换命令中的 `N`。实验表格来自 `python experiments.py --team N`，也可加 `--part pancakes`、`--part flip-cost`、`--part knapsack` 或 `--part coloring` 分开运行。填写组员及分工、A2/A3 的设计与测试情况、B2/B3/B4 的证明、实验表格以及 AI 工具使用说明。然后回答以下七问。

1. 单位代价下，哪些算法得到最优解，为什么？比较扩展量，解释为什么迭代加深有时比 BFS 扩展得更少，有时更多。
2. Weighted A* 的解是否落在预期的代价界内？写清楚这个界并解释依据。
3. A* 搭配自创启发式和 gap 启发式分别得到什么结果？结合 B3 的分析解释差异。
4. 按翻转长度计费时，比较 UCS 和使用两种启发式的 A*，并解释双向 BFS 为什么可能返回更贵的路径。
5. 比较背包和图着色实验中的算法，解释重启、束宽 5 和 20、锦标赛选择和排名选择的影响。
6. 解释背包给超重解设置负适应度的作用，讨论给定的轮盘赌选择能否直接使用这个分数。
7. 分析 `solve([3,1,2,4], Moves)` 的行为、`solve_id/2` 的终止性和最少步数保证，以及 `flip(2, X, [1,3,2])` 如何反向求解。

Python 用 `python -m unittest` 检查，Prolog 进入 `prolog/` 后运行 `swipl check.pl`。按课程说明，3 至 5 人组队，由一名组员在 **2026 年 11 月 30 日 23:59** 前在 Moodle 上传包含代码与报告的 `team-N.zip`。每位组员都要能现场解释全部内容并修改代码。
