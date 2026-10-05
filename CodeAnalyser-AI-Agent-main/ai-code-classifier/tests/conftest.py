"""
Pytest configuration and fixtures
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.llm_service import LLMService


@pytest.fixture
def mock_llm_service(monkeypatch):
    """Mock LLM service to avoid real API calls"""

    async def mock_generate(system_prompt: str, user_prompt: str, temperature: float = 0.1):
        """Mock LLM generation based on prompt content"""
        # Determine response type from prompt
        if "algorithmic approach" in system_prompt.lower() or "approach" in user_prompt.lower():
            return """{
                "primary_approach": "Dynamic Programming",
                "secondary_approaches": ["Loop"],
                "data_structures": ["Array"],
                "detected_patterns": ["State Tracking"]
            }"""
        elif "difficulty" in system_prompt.lower():
            return """{
                "difficulty": "Medium",
                "confidence": 0.85,
                "reasoning": "Problem requires understanding of dynamic programming concepts and optimal substructure"
            }"""
        else:
            # Master prompt
            return """{
                "language": "Python",
                "primary_approach": "Dynamic Programming",
                "secondary_approaches": ["Loop"],
                "data_structures": ["Array"],
                "difficulty": "Medium",
                "confidence": 0.85,
                "time_complexity": "O(N)",
                "space_complexity": "O(1)",
                "reasoning": "Uses dynamic programming with constant space optimization",
                "detected_patterns": ["State Tracking"]
            }"""

    # Patch the LLM service
    mock_service = MagicMock(spec=LLMService)
    mock_service.generate = AsyncMock(side_effect=mock_generate)

    monkeypatch.setattr("app.services.llm_service.llm_service", mock_service)
    monkeypatch.setattr("app.agents.approach_agent.llm_service", mock_service)
    monkeypatch.setattr("app.agents.difficulty_agent.llm_service", mock_service)

    return mock_service
