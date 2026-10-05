"""
Configuration management for AI Code Classifier
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # LLM Configuration
    llm_api_key: str
    llm_model: str = "llama-3.3-70b-versatile"
    llm_base_url: str = "https://api.groq.com/openai/v1"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Security Limits
    max_code_length: int = 50000
    max_problem_length: int = 10000

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


# Supported languages
SUPPORTED_LANGUAGES = ["c++", "cpp", "java", "python", "py"]

# Approach taxonomy
APPROACH_TAXONOMY = [
    "Loop",
    "Nested Loop",
    "Recursion",
    "Backtracking",
    "Dynamic Programming",
    "Greedy",
    "DFS",
    "BFS",
    "Binary Search",
    "Two Pointers",
    "Sliding Window",
    "Prefix Sum",
    "Sorting",
    "Hashing",
    "Stack",
    "Queue",
    "Heap",
    "Graph",
    "Tree",
    "Union Find",
    "Divide and Conquer",
    "Bit Manipulation",
    "Math",
    "String Algorithm",
    "Simulation",
    "Other",
]

# Difficulty levels
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
