"""
Tests for complexity analysis
"""

import pytest
from app.analyzers.complexity_analyzer import ComplexityAnalyzer


def test_complexity_linear():
    """Test complexity analysis for linear algorithm"""
    analyzer = ComplexityAnalyzer()

    code = """
for i in range(n):
    print(i)
"""

    result = analyzer.analyze(code, "Loop")

    assert result.time_complexity == "O(N)"
    assert result.space_complexity == "O(1)"
    assert isinstance(result.reasoning, str)


def test_complexity_quadratic():
    """Test complexity analysis for quadratic algorithm"""
    analyzer = ComplexityAnalyzer()

    code = """
for i in range(n):
    for j in range(n):
        print(i, j)
"""

    result = analyzer.analyze(code, "Nested Loop")

    assert result.time_complexity == "O(N^2)"
    assert isinstance(result.space_complexity, str)


def test_complexity_binary_search():
    """Test complexity analysis for binary search"""
    analyzer = ComplexityAnalyzer()

    code = """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
"""

    result = analyzer.analyze(code, "Binary Search")

    assert result.time_complexity == "O(log N)"


def test_complexity_dp_with_array():
    """Test complexity analysis for DP with array"""
    analyzer = ComplexityAnalyzer()

    code = """
def fibonacci(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
"""

    result = analyzer.analyze(code, "Dynamic Programming")

    assert result.time_complexity == "O(N)"
    assert result.space_complexity == "O(N)"


def test_complexity_backtracking():
    """Test complexity analysis for backtracking"""
    analyzer = ComplexityAnalyzer()

    code = """
def permute(nums):
    result = []
    def backtrack(current):
        if len(current) == len(nums):
            result.append(current[:])
            return
        for num in nums:
            if num not in current:
                current.append(num)
                backtrack(current)
                current.pop()
    backtrack([])
    return result
"""

    result = analyzer.analyze(code, "Backtracking")

    assert result.time_complexity == "O(2^N)"
    assert result.space_complexity == "O(N)"


def test_complexity_graph():
    """Test complexity analysis for graph algorithm"""
    analyzer = ComplexityAnalyzer()

    code = """
def dfs(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node])
"""

    result = analyzer.analyze(code, "DFS")

    assert result.time_complexity == "O(V + E)"
