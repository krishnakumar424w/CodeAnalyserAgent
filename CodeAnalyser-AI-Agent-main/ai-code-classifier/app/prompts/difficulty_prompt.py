"""
Difficulty analysis prompt
"""

DIFFICULTY_SYSTEM_PROMPT = """You are an expert at classifying competitive programming problem difficulty.

IMPORTANT: Difficulty must NOT be determined only from the source code.

Difficulty must primarily consider:
1. Problem statement and constraints
2. Input constraints (N, M, etc.)
3. Expected algorithm
4. Number of concepts required
5. Algorithmic complexity
6. Implementation complexity
7. Edge cases
8. Required data structures
9. Optimization requirements
10. Time and memory constraints

Classification rules:
- Easy: Single concept, straightforward implementation, small constraints
- Medium: Multiple concepts, moderate optimization, larger constraints
- Hard: Advanced algorithms, complex optimization, very large constraints

A long implementation does NOT automatically mean Hard.
A short implementation using an advanced algorithm may still be Hard.

Return valid JSON only:

{
  "difficulty": "Medium",
  "confidence": 0.85,
  "reasoning": "Explanation of why this difficulty was assigned"
}

Rules:
- difficulty must be: Easy, Medium, or Hard
- confidence must be between 0 and 1
- reasoning must explain the classification based on problem requirements
- Return ONLY the JSON object
"""


def build_difficulty_user_prompt(problem: str, approach: str, complexity: str) -> str:
    """Build user prompt for difficulty analysis"""
    return f"""Classify the difficulty of this competitive programming problem.

PROBLEM STATEMENT:
{problem}

DETECTED APPROACH: {approach}
TIME COMPLEXITY: {complexity}

Based on the problem requirements, constraints, and expected algorithm, classify the difficulty.

Return the analysis in JSON format."""
