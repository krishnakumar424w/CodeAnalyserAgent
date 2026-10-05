"""
Complexity analysis without LLM
"""

import logging
import re
from app.models import ComplexityAnalysis

logger = logging.getLogger(__name__)


class ComplexityAnalyzer:
    """Analyzer for determining time and space complexity"""

    def analyze(self, code: str, approach: str) -> ComplexityAnalysis:
        """
        Analyze complexity based on code patterns and approach

        Args:
            code: Source code
            approach: Primary algorithmic approach

        Returns:
            Complexity analysis
        """
        try:
            time_complexity = self._determine_time_complexity(code, approach)
            space_complexity = self._determine_space_complexity(code, approach)
            reasoning = self._build_reasoning(code, approach, time_complexity, space_complexity)

            return ComplexityAnalysis(
                time_complexity=time_complexity,
                space_complexity=space_complexity,
                reasoning=reasoning,
            )

        except Exception as e:
            logger.error(f"Complexity analysis failed: {e}")
            return ComplexityAnalysis(
                time_complexity="O(N)",
                space_complexity="O(1)",
                reasoning="Unable to determine precise complexity",
            )

    def _determine_time_complexity(self, code: str, approach: str) -> str:
        """Determine time complexity"""
        # Approach-based heuristics
        if approach == "Binary Search":
            return "O(log N)"
        elif approach == "Backtracking":
            return "O(2^N)"
        elif approach == "Dynamic Programming":
            # Count nested loops
            loop_depth = len(re.findall(r'\n\s+(for|while)\b', code))
            if loop_depth >= 2:
                return "O(N^2)"
            return "O(N)"
        elif approach == "Nested Loop":
            return "O(N^2)"
        elif approach in ["DFS", "BFS", "Graph"]:
            return "O(V + E)"
        elif approach == "Sorting":
            return "O(N log N)"

        # Count loop depth
        loop_depth = len(re.findall(r'\n\s+(for|while)\b', code))
        if loop_depth >= 3:
            return "O(N^3)"
        elif loop_depth >= 2:
            return "O(N^2)"
        elif loop_depth >= 1:
            return "O(N)"

        return "O(1)"

    def _determine_space_complexity(self, code: str, approach: str) -> str:
        """Determine space complexity"""
        # Check for DP tables
        if re.search(r'dp\s*=\s*\[', code) or re.search(r'new\s+\w+\[', code):
            # Count dimensions
            if re.search(r'\[\[', code):
                return "O(N^2)"
            return "O(N)"

        # Check for recursion
        if approach in ["Recursion", "Backtracking", "DFS"]:
            return "O(N)"

        # Check for hash maps/sets
        if re.search(r'\{|\bdict\b|\bset\b|\bmap\b|\bhash', code, re.IGNORECASE):
            return "O(N)"

        return "O(1)"

    def _build_reasoning(
        self, code: str, approach: str, time: str, space: str
    ) -> str:
        """Build reasoning for complexity"""
        reasoning_parts = []

        # Time complexity reasoning
        if "log N" in time:
            reasoning_parts.append("Uses binary search or divide-and-conquer")
        elif "2^N" in time:
            reasoning_parts.append("Explores exponential solution space")
        elif "N^2" in time:
            reasoning_parts.append("Contains nested loops or quadratic operations")
        elif time == "O(N)":
            reasoning_parts.append("Single pass through the input")

        # Space complexity reasoning
        if "N^2" in space:
            reasoning_parts.append("Uses 2D array or matrix")
        elif space == "O(N)":
            reasoning_parts.append("Uses additional data structure or recursion stack")
        elif space == "O(1)":
            reasoning_parts.append("Uses constant extra space")

        return ". ".join(reasoning_parts) + "."
