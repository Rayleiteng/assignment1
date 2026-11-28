# Assignment 1: report

## Team

**Team/Group number:** 4 (Group D)

| Name | Student ID | Main contributions |
|---|---|---|
| | | |
| | | |
| | | |

## Part A: search algorithms

**A2. IDA\*.** `ida_star_search` runs depth-first search with a bound on `f = g + h`, starting at the heuristic value of the initial state. It prunes nodes above the bound and skips states already on the current path. If a pass finds no goal, the smallest score that exceeded the bound becomes the next bound. If there is no such score, the search returns `None`.

**A3. Bidirectional search.** `bidirectional_search` runs breadth-first search forward from the start and backward from the goal using predecessor links. It expands the smaller frontier one full layer at a time. If several states connect the two searches in that layer, it chooses the one with the smallest sum of depths. It then follows the backward parent links toward the goal and adds the actual cost of each forward action, so the result reports the true cost of the minimum-step path.

**Tests.** All 11 Part A tests passed with `python -m unittest tests.test_informed tests.test_bidirectional`.

## Part B: the pancake problem

**B1. Problem model.** A state stores a tuple listing the pancakes from top to bottom. The initial state is the given tuple, and the unique goal is `(1, 2, ..., n)`. For every `k` from 2 to `n`, the action `flip k` reverses the first `k` pancakes. The same flip reverses that transition, so `get_predecessors` uses the same transitions. In the unit-cost variant every flip costs 1; in the second variant `flip k` costs `k`.

### Experiments, unit cost

Complete Group D output from `python experiments.py --team 4 --part pancakes`.

```
=== Pancakes, every flip costs 1

small stack: 4 2 7 5 3 1 6
  algorithm                        cost  flips     expanded  seconds
  breadth-first search                7      7        4,679     0.07
  iterative deepening                 7      7       13,583     0.20
  uniform-cost search                 7      7        4,679     0.06
  greedy, gap                         9      9           11     0.00
  A*, gap                             7      7           26     0.00
  A*, your heuristic                  7      7           23     0.00
  weighted A* (w = 2), gap            8      8           11     0.00
  IDA*, gap                           7      7           15     0.00
  bidirectional search                7      7          223     0.00

small stack: 1 6 3 5 2 4 7
  algorithm                        cost  flips     expanded  seconds
  breadth-first search                6      6        3,266     0.04
  iterative deepening                 6      6        3,098     0.04
  uniform-cost search                 6      6        3,266     0.05
  greedy, gap                         7      7            7     0.00
  A*, gap                             6      6           10     0.00
  A*, your heuristic                  6      6           10     0.00
  weighted A* (w = 2), gap            7      7            7     0.00
  IDA*, gap                           6      6           10     0.00
  bidirectional search                6      6           74     0.00

small stack: 7 3 2 6 5 4 1
  algorithm                        cost  flips     expanded  seconds
  breadth-first search                4      4          369     0.00
  iterative deepening                 4      4          100     0.00
  uniform-cost search                 4      4          369     0.00
  greedy, gap                         4      4            4     0.00
  A*, gap                             4      4            7     0.00
  A*, your heuristic                  4      4            7     0.00
  weighted A* (w = 2), gap            4      4            4     0.00
  IDA*, gap                           4      4            4     0.00
  bidirectional search                4      4           14     0.00

medium stack: 1 3 2 8 7 6 5 4
  algorithm                        cost  flips     expanded  seconds
  breadth-first search                5      5        5,705     0.10
  uniform-cost search                 5      5        5,705     0.16
  greedy, gap                         6      6            9     0.00
  A*, gap                             5      5           26     0.00
  A*, your heuristic                  5      5           21     0.00
  weighted A* (w = 2), gap            5      5           19     0.00
  IDA*, gap                           5      5           32     0.00
  bidirectional search                5      5           58     0.00

medium stack: 5 7 4 3 2 1 6 8
  algorithm                        cost  flips     expanded  seconds
  breadth-first search                4      4          462     0.02
  uniform-cost search                 4      4          462     0.01
  greedy, gap                         4      4            5     0.00
  A*, gap                             4      4            6     0.00
  A*, your heuristic                  4      4            5     0.00
  weighted A* (w = 2), gap            4      4            5     0.00
  IDA*, gap                           4      4            5     0.00
  bidirectional search                4      4           16     0.00

large stack: 8 2 14 6 12 5 1 11 7 13 4 3 9 10
  algorithm                        cost  flips     expanded  seconds
  greedy, gap                        14     14           16     0.00
  A*, gap                            12     12           53     0.00
  A*, your heuristic                 12     12           53     0.01
  weighted A* (w = 2), gap           14     14           16     0.00
  IDA*, gap                          12     12           33     0.00

large stack: 7 3 11 12 1 5 4 13 9 14 2 8 6 10
  algorithm                        cost  flips     expanded  seconds
  greedy, gap                        14     14           14     0.00
  A*, gap                            13     13          933     0.07
  A*, your heuristic                 13     13          933     0.06
  weighted A* (w = 2), gap           13     13           16     0.00
  IDA*, gap                          13     13          446     0.02
```

### Proofs

Here `` is a pancake stack, `s'` is the stack after one flip, and `G(s) = gap_heuristic(s)`.

**B2. Gap heuristic (unit cost).** `G(s)` counts gaps between adjacent pancakes, including the plate `n + 1`. A prefix flip preserves all internal gaps; only the pair at the flip boundary can change. Thus `|G(s) - G(s')| <= 1` and `G(goal) = 0`. Therefore `G(s) <= 1 + G(s')` (consistency), and reaching the goal needs at least `G(s)` flips (admissibility).

**B3. Our heuristic (unit cost).** Let `T(s) = 3` if 1 is on top but `` is not the goal, and 0 otherwise. The code returns `max(G(s), T(s))`. If 1 starts on top, two flips that put it back on top must have the same length and undo each other. Solving a non-goal stack therefore requires at least three flips, so `T` and their maximum are admissible.

The maximum is also consistent. Only the case `T(s) = 3 > G(s)` needs checking. After one flip, 1 is no longer on top. The successor cannot have zero gaps. If it had exactly one, it would be `(k, k-1, ..., 1, k+1, ..., n)`: the sole gap follows 1, and all other adjacent sizes are consecutive. Reversing its first `k` pancakes would make `` the goal, a contradiction. Hence `G(s') >= 2`, giving `3 <= 1 + G(s') = 1 + my_heuristic(s')`. All other transitions follow the consistency of `G`.

**B4. Flip-cost heuristic.** When `flip k` costs `k`, `G` is still admissible: each flip removes at most one gap and costs at least 2. Our heuristic is `H(s) = 2G(s) + (n - 2)` if the bottom pancake is not `n`, and `H(s) = 2G(s)` otherwise (zero for an empty stack). Removing `G(s)` gaps needs at least `G(s)` flips, costing at least `2G(s)`. A gap at the plate also requires a full-stack flip costing `n`, which adds `n - 2` to that bound. Hence `H` is admissible and `H(s) >= G(s)`.

### Experiments, flip costs

Complete Group D output from `python experiments.py --team 4 --part flip-cost`.

```
=== Pancakes, flipping k pancakes costs k

stack: 4 2 7 5 3 1 6
  algorithm                        cost  flips     expanded  seconds
  uniform-cost search                30      7        5,700     0.09
  A*, gap                            30      7        3,151     0.05
  A*, flip-cost heuristic            30      7          312     0.01
  IDA*, flip-cost heuristic          30      7        1,161     0.02
  bidirectional search               30      7          223     0.00

stack: 1 6 3 5 2 4 7
  algorithm                        cost  flips     expanded  seconds
  uniform-cost search                24      7        2,552     0.04
  A*, gap                            24      7          764     0.01
  A*, flip-cost heuristic            24      7          224     0.00
  IDA*, flip-cost heuristic          24      7          865     0.01
  bidirectional search               25      6           74     0.00

stack: 7 3 2 6 5 4 1
  algorithm                        cost  flips     expanded  seconds
  uniform-cost search                20      4          897     0.01
  A*, gap                            20      4          228     0.00
  A*, flip-cost heuristic            20      4           22     0.00
  IDA*, flip-cost heuristic          20      4           56     0.00
  bidirectional search               20      4           14     0.00

stack: 1 3 2 8 7 6 5 4
  algorithm                        cost  flips     expanded  seconds
  uniform-cost search                27      6       10,312     0.20
  A*, gap                            27      6        2,717     0.08
  A*, flip-cost heuristic            27      6          201     0.01
  IDA*, flip-cost heuristic          27      6          595     0.01
  bidirectional search               35      5           58     0.00

stack: 5 7 4 3 2 1 6 8
  algorithm                        cost  flips     expanded  seconds
  uniform-cost search                20      4        1,308     0.03
  A*, gap                            20      4          293     0.01
  A*, flip-cost heuristic            20      4           65     0.00
  IDA*, flip-cost heuristic          20      4          213     0.00
  bidirectional search               20      4           16     0.00
```

### Questions 1 to 4

**1. Unit-cost pancakes.** BFS, iterative deepening, UCS, A*, IDA*, and bidirectional BFS found minimum-flip solutions. BFS and bidirectional BFS minimize steps; UCS minimizes the same unit cost; A* and IDA* use admissible heuristics. The five small/medium results agree, and A* and IDA* returned 12 and 13 flips on the large stacks. Greedy was nonoptimal on five of seven stacks, and weighted A* on three. A* with gap expanded only 6–26 states on small/medium stacks, versus 369–5,705 for BFS. Iterative deepening may repeat much work (13,583 versus 4,679 expansions) or find the goal early in its final layer (100 versus 369).

**2. Weighted A*.** For `w = 2`, the admissible gap heuristic gives the bound `cost <= 2 * C*`, where `C*` is the optimum. All results satisfy it; the largest observed ratio was `7/6`. Weighted A* expanded fewer states than A* with gap on every stack, but sometimes returned a longer solution (for example, 14 rather than 12 flips).

**3. Our heuristic.** Both A* variants returned the same optimal costs. Our heuristic raised the gap lower bound when 1 was on top, reducing expansions on three stacks (for example, 26 to 21); the other four tied.

**4. Flip costs.** UCS and both A* variants returned the same minimum costs: 30, 24, 20, 27, and 20. The stronger flip-cost heuristic reduced A* expansions on every stack; for example, from 2,717 to 201. Bidirectional BFS minimizes flips rather than total cost, so it returned 6 flips costing 25 instead of 7 costing 24 on one stack, and 5 costing 35 instead of 6 costing 27 on another.

## Part C: local search and genetic algorithms

Paste here the tables printed by `python experiments.py --team N --part knapsack` and
`--part coloring`.

```

```

### Questions 5 and 6

## Part D: logic programming

`move/3` enumerates the legal prefix lengths from 2 through the stack length
and passes each one to `flip/3`. `gaps/2` appends the plate of size `N + 1`.
`nadjCount/2` then walks the adjacent pairs, and `pair_gap/3` counts a gap
whenever the sizes differ by more than 1. On legal stacks the sizes are
distinct, so testing for a difference of 1 identifies the pairs with no gap.

### Question 7

1. **Depth-first search.** With `Moves` unbound, `solve([3,1,2,4], Moves)`
   takes `flip(2)` first and reaches `[1,3,2,4]`. The next call tries
   `flip(2)` first as well, returning to `[3,1,2,4]`. Both states fail
   the goal test. Prolog keeps descending into this cycle before it can
   backtrack to a larger flip. The query reached the time limit in a bounded run.
2. **Iterative deepening.** With `Moves` unbound, `length(Moves, _)` generates
   lists of length 0, 1, 2, and so on. Each move in `solve/2` consumes one
   list element. With a fixed length and finitely many legal flips at every
   state, each round of search is finite. Every valid stack has a finite
   solution. For each largest pancake still out of place, bring it to the top
   when needed, then flip the unsorted prefix to put it in its final position.
   Repeat on shorter prefixes. Some finite length therefore succeeds. All
   smaller lengths have already been exhausted by that point, so the first
   answer uses the fewest flips. On `[3,1,2,4]` it is `[flip(3), flip(2)]`.
   Backtracking can produce further answers at the same or greater lengths.
3. **Backward flip.** `flip(2, X, [1,3,2])` gives `X = [3,1,2]`.
   `length/2` fixes the prefix length at two. The final `append/3` fixes
   the reversed prefix to `[1,3]` and the shared suffix to `[2]`.
   `reverse/2` relates the reversed prefix to `[3,1]`. Together these
   relations determine `X` through the first `append/3`.

### Verification

`swipl check.pl` passed all 12 checks on SWI-Prolog 10.0.2. An independent
breadth-first search and direct calculations agreed on all 154 stacks of
size 0 through 5, covering minimum flip counts, solution replay, legal moves,
inverse flips, and gap counts including the plate.

## Use of AI tools

For Part D, OpenAI Codex provided an initial Prolog implementation,
explained the predicates, helped diagnose arithmetic and recursion issues,
verified the submitted version, and drafted the Part D report.
