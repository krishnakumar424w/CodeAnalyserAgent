"""
Tests for difficulty classification
"""

import pytest
from app.agents.difficulty_agent import DifficultyAgent


@pytest.mark.asyncio
async def test_difficulty_agent_easy(mock_llm_service):
    """Test difficulty agent with easy problem"""
    agent = DifficultyAgent()

    problem = "Given two numbers, return their sum."
    result = await agent.analyze(problem, "Loop", "O(1)")

    assert result.difficulty in ["Easy", "Medium", "Hard"]
    assert 0.0 <= result.confidence <= 1.0
    assert isinstance(result.reasoning, str)
    assert len(result.reasoning) > 0


@pytest.mark.asyncio
async def test_difficulty_agent_hard(mock_llm_service):
    """Test difficulty agent with hard problem"""
    agent = DifficultyAgent()

    problem = """
    Given a string s and a dictionary of strings wordDict, add spaces in s to construct
    a sentence where each word is a valid dictionary word. Return all such possible sentences.
    Constraints: 1 <= s.length <= 20, 1 <= wordDict.length <= 1000
    """
    result = await agent.analyze(problem, "Backtracking", "O(2^N)")

    assert result.difficulty in ["Easy", "Medium", "Hard"]
    assert isinstance(result.confidence, float)
    assert result.reasoning != ""


@pytest.mark.asyncio
async def test_difficulty_agent_invalid_difficulty(mock_llm_service, monkeypatch):
    """Test difficulty agent with invalid difficulty response"""

    async def mock_invalid_generate(*args, **kwargs):
        return '{"difficulty": "VeryHard", "confidence": 0.9, "reasoning": "test"}'

    monkeypatch.setattr(mock_llm_service, "generate", mock_invalid_generate)

    agent = DifficultyAgent()
    result = await agent.analyze("Test problem", "Loop", "O(N)")

    # Should fallback to Medium
    assert result.difficulty == "Medium"
    assert 0.0 <= result.confidence <= 1.0
