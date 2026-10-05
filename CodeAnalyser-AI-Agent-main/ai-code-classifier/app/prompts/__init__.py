"""
Prompt templates for LLM agents
"""

from .master_prompt import MASTER_SYSTEM_PROMPT
from .approach_prompt import APPROACH_SYSTEM_PROMPT, build_approach_user_prompt
from .difficulty_prompt import DIFFICULTY_SYSTEM_PROMPT, build_difficulty_user_prompt

__all__ = [
    "MASTER_SYSTEM_PROMPT",
    "APPROACH_SYSTEM_PROMPT",
    "build_approach_user_prompt",
    "DIFFICULTY_SYSTEM_PROMPT",
    "build_difficulty_user_prompt",
]
