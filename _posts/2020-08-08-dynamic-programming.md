---
layout: post
title: Dynamic Programming 动态规划
categories: [C++, Algorithms]
description: 有关动态规划的一些总结与个人思考
keywords: DP, Algorithms, C++
---
## Intro
- 【最优子结构】每个阶段的最优状态可以从之前某个阶段的某个或某些状态直接得到 
    - 考虑所有之前阶段，所有状态
    - 压缩和并得到状态转移
    - 与贪心区别：贪心只考虑前一阶段的状态，动态规划隐含搜索全部之前阶段
- 【无后效性】而不管之前这个状态是如何得到的
- 分析：
    - 确定阶段状态表示
    - 状态转移：确定某一阶段状态来源/下一步可能状态
- **重要**：
    - 状态定义：**将原问题转化为对于状态的等价数学形式**
    - 状态转移：状态来源，以及转换关系，注意需要状态定义使得：来源状态阶段<当前状态阶段
    - 同一问题对应多种状态定义，一状态定义对应一种转移关系。不同定义复杂度不同: [309. 最佳买卖股票时机含冷冻期](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)

## Classification
1) Overlapping Subproblems
2) Optimal Substructure
## Step
1. Decide a **state** expression with 
   least parameters
2. Formulate **state relationship**

## Overlapping Subproblems
e.g. Fibonachi
## Optimal Substructure
- If optimal solution of the given problem can be obtained by using optimal solutions of its subproblems. 问题的最优解包含的子问题的解也是最优的。

### 最长单调子序列
- d[i] = max{ d[j] | j < i && a[j] < a[i] } + 1
- d[i] 为以a[i]为结尾的最长单调子序列长度


### Examples:
----
#### 115. [Distinct Subsequences](https://leetcode-cn.com/problems/distinct-subsequences/) [hard]
- Given a string S and a string T, count the number of distinct subsequences of S which equals T.
- DP on strings
- string index on 2 strings as state
- string letter comparasion as action

$$
f(i, j) = \\
f(i-1, j)+f(i-1, j-1)  [(S[i]==T[j]) ]\\
f(i-1, j) [(S[i]!=T[j]) ]
$$

```cpp
int numDistinct(string s, string t) {
        size_t m = s.size(), n = t.size();
        vector<vector<uint32_t>> dp(m+1, vector<uint32_t>(n+1, 0));

        dp[0][0] = 1;
        for(size_t i = 1; i<=n; i++){
            dp[0][i] = 0;
        }
        for(size_t i =1; i<=m; i++){
            dp[i][0] = 1;
        }
        for(size_t i = 1; i<=m; i++){
            for(size_t j = 1; j<=n; j++){
                if(s[i-1]==t[j-1]) dp[i][j] = dp[i-1][j]+dp[i-1][j-1];
                else dp[i][j] = dp[i-1][j];
            }
        }
        return dp[m][n];
    }
```

#### 72. [Edit Distance](https://leetcode-cn.com/problems/edit-distance/solution/72-edit-distance-by-fa-tiao-xiong/) [medium]
- Given two words word1 and word2, find the minimum number of operations required to convert word1 to word2.

    You have the following 3 operations permitted on a word:

        1. Insert a character
        2. Delete a character
        3. Replace a character


- DP on strings
```cpp
int minDistance(string word1, string word2) {
        vector<vector<int>> dp(word1.size()+1, vector<int>(word2.size()+1, 0));

        for(size_t i = 0; i<=word1.size(); i++){
            for(size_t j = 0; j<=word2.size(); j++){
                if(i==0){
                    dp[i][j] = j;
                }
                else if(j==0){
                    dp[i][j] = i;
                }
                else if(word1[i-1]==word2[j-1]){
                    dp[i][j] = dp[i-1][j-1];
                }
                else{
                    dp[i][j] = dp[i-1][j];
                    dp[i][j] = min(dp[i][j], dp[i][j-1]);
                    dp[i][j] = min(dp[i][j], dp[i-1][j-1]);
                    dp[i][j] ++;
                }
            }
        }

        return dp[word1.size()][word2.size()];
    }
```
#### 309. [Best Time to Buy and Sell Stock with Cooldown](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) [medium]
- Say you have an array for which the ith element is the price of a given stock on day i.

    Design an algorithm to find the maximum profit. You may complete as many transactions as you like (ie, buy one and sell one share of the stock multiple times) with the following restrictions:

    You may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).
    After you sell your stock, you cannot buy stock on next day. (ie, cooldown 1 day)

- 3 states: 3 states, 0-not hold, 1-hold, 2-freeze
```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        if(prices.size() == 0) return 0;
        vector<vector<int>> memo(prices.size(), vector<int>(3, 0));
        memo[0][0] = 0;
        memo[0][1] = -prices[0];
        for(size_t i = 1; i<prices.size();i++){
            memo[i][0] = max(memo[i-1][0], memo[i-1][2]);
            memo[i][1] = max(memo[i-1][1], memo[i-1][0]-prices[i]);
            memo[i][2] = memo[i-1][1]+prices[i];
        }
        return max(memo[prices.size()-1][0], memo[prices.size()-1][2]);
    }
};
```
#### 300. [Longest Increasing Subsequence](https://leetcode-cn.com/problems/longest-increasing-subsequence/) [medium]
- Given an unsorted array of integers, find the length of longest increasing subsequence.
- f(i) = max{f(j)| j<i && nums[j] < nums[i]}+1

- Note:memo need to set to 1 at first:decreasing, j doesn't exist

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> memo(nums.size(), 1);
        for(size_t i = 1; i<nums.size(); i++){
            //important: set to 1 at first.
            int ans = 1;
            for(size_t j = 0; j<i; j++){
                if(nums[j]<nums[i])
                    ans = max(ans, memo[j]+1);
            }
            memo[i] = ans;
        }
        int res = 0;
        for(int i = 0; i<nums.size(); i++){
            res = max(res, memo[i]);
        }
        return res;
    }
};
```