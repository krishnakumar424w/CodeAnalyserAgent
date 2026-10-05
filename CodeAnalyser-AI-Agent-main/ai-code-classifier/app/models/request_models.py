"""
Request models for API endpoints
"""

from pydantic import BaseModel, Field, field_validator


class CodeAnalysisRequest(BaseModel):
    """Request model for code analysis endpoint"""

    language: str = Field(
        ...,
        description="Programming language (c++, java, python)",
        min_length=1,
        max_length=20,
    )
    problem: str = Field(
        ...,
        description="Competitive programming problem statement",
        min_length=10,
        max_length=10000,
    )
    code: str = Field(
        ..., description="User-submitted source code", min_length=1, max_length=50000
    )

    @field_validator("language")
    @classmethod
    def normalize_language(cls, v: str) -> str:
        """Normalize language to lowercase"""
        return v.lower().strip()

    @field_validator("problem", "code")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Strip leading/trailing whitespace"""
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "language": "python",
                "problem": "Given an array of integers, find the maximum subarray sum using Kadane's algorithm.",
                "code": "def maxSubArray(nums):\n    max_sum = float('-inf')\n    current_sum = 0\n    for num in nums:\n        current_sum = max(num, current_sum + num)\n        max_sum = max(max_sum, current_sum)\n    return max_sum",
            }
        }
