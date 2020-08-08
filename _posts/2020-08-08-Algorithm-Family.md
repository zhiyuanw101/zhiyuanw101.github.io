---
layout: post
title: 算法家族 Algorithm Families
categories: [Algorithms]
description: 有关算法的一些总结与个人思考，部分内容摘自EECS281
keywords: Algorithms, C++
---
常见算法的归类整理，绝大多数算法都有比较明确的特征，从而可以归类抽象。

了解抽象出的几类算法，在解决新问题即可代入。不至于面试面对leetcode一时语塞，总是能墨迹出一个答案的嘛（笑。

纯英文因为抄slides方便，不喜勿喷。
## Outline

- [Outline](#outline)
- [Brute-Force](#brute-force)
- [Greedy](#greedy)
- [Divide and Conquer](#divide-and-conquer)
- [Dynamic Programming](#dynamic-programming)
- [Backtracking](#backtracking)
- [Branch and Bound](#branch-and-bound)

## Brute-Force

- consider entire solution set
- straight-forward
- time consuming

## Greedy

- make local, best decision at a time, don't look back
- must prove give **global optimal** solution
  - can **global optimal** found by series of **local optimal** choices?
- Example:
  - Selection Sort
  - Prim/Kruskal in MST
  - Dijkstra's algorithm

## Divide and Conquer

- Divide into smaller subproblems
- Example:
  - Binary Search
  - Quick Sort
  - Merge Sort

## Dynamic Programming

- similar to Divide and Conquer, but remember partial solutions
- must have overlapping subspaces
- $O(e^n)$ to $O(n^c)$
- Types:
  - Top down
  - Bottom up

## Backtracking

- Systematically consider all possible solution, **prune** searches that do not satisfy constraint
  - think as **DFS** on solution tree, with **pruning**
  - Basic **DFS**: Generating Permutation
- Often take form of **resursion + loop**:
  - loop over possibilities, in the loop: do-branch-undo
  - **backtrack** if not possible or already valid
- Example:
  - N-Queen
- A General form:
```c++
Algorithm checknode(node v){
    if(solution(v))
        return solution
    else
        for(child node u of v)
            if(promising(u))
                add u to solution       //do 
                checknode(u)            //branch
                remove u from solution  //undo
}
```

## Branch and Bound

- extend idea of **backtracking** to **optimization** problem: more **pruning**
- Key in B&B:
  - **current best**: record current best solution
  - **lower bound**: estimate *best case* of an unexplored path, estimation must be faster than completing the path
  - **prune**: estimation shows lower bound *worse than* current best.
- Example:
  - optimal TSP
- General form:
  - similar to **Backtracking**
  - add estimation of bound and pruning to `promising`
- Comparison:
  - **DFS** is the Brute-force approach of enumerating(search) all solutions in solution set. 
  - **Backtracking** add `promising` to check constraint at each node. Can **prune** entire subtree(subset of solution set) if not satisfied.
  - **Branch and Bound** add `bound` estimation in `promising` to **prune** more, if already worse than current best.