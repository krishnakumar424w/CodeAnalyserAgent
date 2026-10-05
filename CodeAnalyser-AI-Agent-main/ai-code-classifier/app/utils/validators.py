"""
Validation utilities
"""

from typing import Optional
from app.config import SUPPORTED_LANGUAGES, APPROACH_TAXONOMY, DIFFICULTY_LEVELS


def validate_language(language: str) -> Optional[str]:
    """
    Validate and normalize language

    Args:
        language: Language string to validate

    Returns:
        Normalized language name or None if invalid
    """
    lang_lower = language.lower().strip()

    # Direct match
    if lang_lower in SUPPORTED_LANGUAGES:
        # Normalize to standard names
        if lang_lower in ["c++", "cpp"]:
            return "C++"
        elif lang_lower == "java":
            return "Java"
        elif lang_lower in ["python", "py"]:
            return "Python"

    return None


def validate_approach(approach: str) -> bool:
    """
    Validate if approach is in the predefined taxonomy

    Args:
        approach: Approach string to validate

    Returns:
        True if valid, False otherwise
    """
    return approach in APPROACH_TAXONOMY


def validate_difficulty(difficulty: str) -> bool:
    """
    Validate if difficulty is one of the valid levels

    Args:
        difficulty: Difficulty string to validate

    Returns:
        True if valid, False otherwise
    """
    return difficulty in DIFFICULTY_LEVELS
