"""
API endpoint tests
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "AI Code Classifier"
    assert "endpoints" in data


@pytest.mark.asyncio
async def test_analyze_missing_fields():
    """Test analysis with missing required fields"""
    response = client.post("/api/analyze", json={})
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_analyze_unsupported_language():
    """Test analysis with unsupported language"""
    response = client.post(
        "/api/analyze",
        json={
            "language": "javascript",
            "problem": "Test problem",
            "code": "console.log('test')",
        },
    )
    assert response.status_code == 400
    assert "Unsupported language" in response.json()["detail"]


@pytest.mark.asyncio
async def test_analyze_empty_code():
    """Test analysis with empty code"""
    response = client.post(
        "/api/analyze",
        json={"language": "python", "problem": "Test problem", "code": ""},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_analyze_code_too_long():
    """Test analysis with code exceeding maximum length"""
    long_code = "x = 1\n" * 60000  # Exceeds 50000 chars
    response = client.post(
        "/api/analyze",
        json={"language": "python", "problem": "Test problem", "code": long_code},
    )
    assert response.status_code == 400
    assert "exceeds maximum length" in response.json()["detail"]


@pytest.mark.asyncio
async def test_analyze_python_dp(mock_llm_service):
    """Test analysis of Python Dynamic Programming solution"""
    code = """
def maxSubArray(nums):
    max_sum = float('-inf')
    current_sum = 0
    for num in nums:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum
"""
    response = client.post(
        "/api/analyze",
        json={
            "language": "python",
            "problem": "Find maximum subarray sum (Kadane's algorithm)",
            "code": code,
        },
    )

    assert response.status_code == 200
    data = response.json()

    # Validate response structure
    assert "language" in data
    assert "primary_approach" in data
    assert "difficulty" in data
    assert "confidence" in data
    assert "time_complexity" in data
    assert "space_complexity" in data
    assert "reasoning" in data

    # Validate types
    assert isinstance(data["secondary_approaches"], list)
    assert isinstance(data["data_structures"], list)
    assert isinstance(data["detected_patterns"], list)

    # Validate values
    assert data["difficulty"] in ["Easy", "Medium", "Hard"]
    assert 0.0 <= data["confidence"] <= 1.0
