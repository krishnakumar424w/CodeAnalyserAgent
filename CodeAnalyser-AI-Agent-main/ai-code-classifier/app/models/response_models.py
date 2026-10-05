"""
Response models for API endpoints
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class HealthResponse(BaseModel):
    """Health check response"""

    status: str = "ok"


class ApproachAnalysis(BaseModel):
    """Approach analysis result"""

    primary_approach: str
    secondary_approaches: List[str] = []
    data_structures: List[str] = []
    detected_patterns: List[str] = []


class ComplexityAnalysis(BaseModel):
    """Complexity analysis result"""

    time_complexity: str
    space_complexity: str
    reasoning: str


class DifficultyAnalysis(BaseModel):
    """Difficulty analysis result"""

    difficulty: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        """Ensure difficulty is one of the valid levels"""
        valid = ["Easy", "Medium", "Hard"]
        if v not in valid:
            return "Medium"  # Default fallback
        return v


class CodeAnalysisResponse(BaseModel):
    """Complete code analysis response"""

    language: str
    primary_approach: str
    secondary_approaches: List[str] = []
    data_structures: List[str] = []
    difficulty: str
    confidence: float = Field(ge=0.0, le=1.0)
    time_complexity: str
    space_complexity: str
    reasoning: str
    detected_patterns: List[str] = []

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        """Ensure difficulty is one of the valid levels"""
        valid = ["Easy", "Medium", "Hard"]
        if v not in valid:
            return "Medium"
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "language": "Python",
                "primary_approach": "Dynamic Programming",
                "secondary_approaches": ["Loop"],
                "data_structures": ["Array"],
                "difficulty": "Medium",
                "confidence": 0.85,
                "time_complexity": "O(N)",
                "space_complexity": "O(1)",
                "reasoning": "The solution uses Kadane's algorithm, which is a dynamic programming approach that tracks the maximum subarray ending at each position.",
                "detected_patterns": ["State Tracking", "Greedy Choice"],
            }
        }
