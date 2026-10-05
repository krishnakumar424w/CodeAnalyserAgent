#!/usr/bin/env python3
"""
Demo: Test the complete AI Code Classifier with real Groq API
"""
import asyncio
import json
from app.services.analysis_service import analysis_service
from app.models import CodeAnalysisRequest

# Test cases
TEST_CASES = [
    {
        "name": "Kadane's Algorithm (Dynamic Programming)",
        "request": CodeAnalysisRequest(
            language="python",
            problem="Find the maximum subarray sum. Array length up to 100,000. Use optimal O(N) time and O(1) space solution.",
            code="""def maxSubArray(nums):
    max_sum = float('-inf')
    current_sum = 0
    for num in nums:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum"""
        )
    },
    {
        "name": "Binary Search",
        "request": CodeAnalysisRequest(
            language="java",
            problem="Search for a target value in a sorted array. Return the index if found, -1 otherwise. Array length up to 10^6.",
            code="""public int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}"""
        )
    },
]

async def run_demo():
    print("=" * 70)
    print("AI CODE CLASSIFIER - LIVE DEMO with Groq API")
    print("=" * 70)

    for i, test in enumerate(TEST_CASES, 1):
        print(f"\n[Test {i}] {test['name']}")
        print("-" * 70)

        try:
            result = await analysis_service.analyze_code(test['request'])

            print(f"Language:          {result.language}")
            print(f"Primary Approach:  {result.primary_approach}")
            print(f"Secondary:         {', '.join(result.secondary_approaches) if result.secondary_approaches else 'None'}")
            print(f"Data Structures:   {', '.join(result.data_structures) if result.data_structures else 'None'}")
            difficulty_label = {"a": "Easy", "b": "Medium", "c": "Hard"}.get(result.difficulty, result.difficulty)
            print(f"Difficulty:        {result.difficulty} ({difficulty_label})")
            print(f"Confidence:        {result.confidence:.2f}")
            print(f"Time Complexity:   {result.time_complexity}")
            print(f"Space Complexity:  {result.space_complexity}")
            print(f"Patterns:          {', '.join(result.detected_patterns[:3])}")
            print(f"Reasoning:         {result.reasoning[:150]}...")

            print("\n[SUCCESS] Analysis completed!")

        except Exception as e:
            print(f"\n[ERROR] {e}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_demo())
