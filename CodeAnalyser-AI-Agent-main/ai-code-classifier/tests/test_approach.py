"""
Tests for approach analysis
"""

import pytest
from app.agents.approach_agent import ApproachAgent


@pytest.mark.asyncio
async def test_approach_agent_python(mock_llm_service):
    """Test approach agent with Python code"""
    agent = ApproachAgent()

    code = """
def dfs(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
"""

    result = await agent.analyze("Python", code)

    assert result.primary_approach in [
        "DFS",
        "Dynamic Programming",
        "Recursion",
        "Other",
    ]
    assert isinstance(result.secondary_approaches, list)
    assert isinstance(result.data_structures, list)
    assert isinstance(result.detected_patterns, list)


@pytest.mark.asyncio
async def test_approach_agent_java(mock_llm_service):
    """Test approach agent with Java code"""
    agent = ApproachAgent()

    code = """
public int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
"""

    result = await agent.analyze("Java", code)

    assert result.primary_approach in ["Binary Search", "Dynamic Programming", "Other"]
    assert isinstance(result.secondary_approaches, list)


@pytest.mark.asyncio
async def test_approach_agent_invalid_json(mock_llm_service, monkeypatch):
    """Test approach agent with invalid JSON response"""

    async def mock_invalid_generate(*args, **kwargs):
        return "This is not JSON at all"

    monkeypatch.setattr(mock_llm_service, "generate", mock_invalid_generate)

    agent = ApproachAgent()
    result = await agent.analyze("Python", "def test(): pass")

    # Should return default values
    assert result.primary_approach == "Other"
    assert result.secondary_approaches == []
