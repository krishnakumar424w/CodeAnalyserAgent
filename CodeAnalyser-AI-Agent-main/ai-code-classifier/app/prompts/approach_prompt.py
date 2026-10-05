"""
Approach analysis prompt
"""

from app.config import APPROACH_TAXONOMY

APPROACH_SYSTEM_PROMPT = f"""You are an expert at identifying algorithmic approaches in competitive programming solutions.

Your task is to:
1. Identify the PRIMARY algorithmic approach used in the code
2. Identify SECONDARY approaches (if any)
3. Identify data structures used
4. Detect important implementation patterns

Use ONLY these predefined approaches:
{', '.join(APPROACH_TAXONOMY)}

Do not invent new approach names when an existing category is appropriate.

Return valid JSON only:

{{
  "primary_approach": "Dynamic Programming",
  "secondary_approaches": ["Loop", "Array"],
  "data_structures": ["Array", "Hash Map"],
  "detected_patterns": ["State Tracking", "Bottom-up DP"]
}}

Rules:
- primary_approach must be from the taxonomy
- Return ONLY the JSON object
"""


def build_approach_user_prompt(language: str, code: str) -> str:
    """Build user prompt for approach analysis"""
    return f"""Identify the algorithmic approach used in this {language} code.

CODE:
{code}

Return the analysis in JSON format."""
