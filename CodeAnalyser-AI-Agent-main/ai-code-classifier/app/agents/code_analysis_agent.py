"""
Code pattern analysis agent
"""

import logging
import re
from typing import List
from app.models import ApproachAnalysis

logger = logging.getLogger(__name__)


class CodeAnalysisAgent:
    """Agent for analyzing code implementation patterns"""

    async def analyze(self, code: str, approach: ApproachAnalysis) -> List[str]:
        """
        Analyze code for implementation patterns

        Args:
            code: Source code
            approach: Detected approach

        Returns:
            List of detected patterns
        """
        patterns = []

        try:
            # Detect loops
            if re.search(r'\b(for|while)\b', code):
                patterns.append("Iteration")

            # Detect recursion
            func_names = re.findall(r'def\s+(\w+)|(\w+)\s*\([^)]*\)\s*\{', code)
            for name_tuple in func_names:
                func_name = name_tuple[0] or name_tuple[1]
                if func_name and re.search(rf'\b{func_name}\s*\(', code):
                    # Check if function calls itself
                    func_pattern = rf'(def\s+{func_name}|{func_name}\s*\([^)]*\)\s*\{{)(.*?)(?=\ndef\s+|\Z)'
                    func_match = re.search(func_pattern, code, re.DOTALL)
                    if func_match and func_name in func_match.group(2):
                        patterns.append("Recursion")
                        break

            # Detect DP patterns
            if 'dp' in code.lower() or 'memo' in code.lower():
                patterns.append("Memoization")
            if re.search(r'\[.*\]\s*=.*\[.*\]', code):
                patterns.append("State Tracking")

            # Detect graph patterns
            if re.search(r'\b(visited|visit|seen)\b', code, re.IGNORECASE):
                patterns.append("Graph Traversal")

            # Detect two pointers
            if re.search(r'\b(left|right|start|end)\b.*\b(left|right|start|end)\b', code):
                patterns.append("Two Pointers")

            # Detect sliding window
            if re.search(r'\b(window|slide)\b', code, re.IGNORECASE):
                patterns.append("Sliding Window")

            # Detect backtracking
            if 'backtrack' in code.lower() or (
                'Recursion' in patterns and re.search(r'\breturn\b', code)
            ):
                patterns.append("Backtracking")

            # Detect greedy patterns
            if approach.primary_approach == "Greedy" or re.search(
                r'\b(max|min|optimal|best)\b', code
            ):
                patterns.append("Greedy Choice")

            # Detect sorting
            if re.search(r'\bsort\b', code, re.IGNORECASE):
                patterns.append("Sorting")

            # Detect binary search
            if re.search(r'\b(mid|middle)\b.*\b(left|right)\b', code):
                patterns.append("Binary Search")

            # Remove duplicates
            patterns = list(dict.fromkeys(patterns))

            # Combine with detected patterns from approach
            all_patterns = patterns + approach.detected_patterns
            all_patterns = list(dict.fromkeys(all_patterns))

            logger.info(f"Detected {len(all_patterns)} code patterns")
            return all_patterns[:10]  # Limit to 10 patterns

        except Exception as e:
            logger.error(f"Code pattern analysis failed: {e}")
            return []
