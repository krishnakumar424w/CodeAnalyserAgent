#!/usr/bin/env python3
import asyncio
from app.config import settings
from app.services.llm_service import LLMService

async def main():
    print(f"Model: {settings.llm_model}")
    print(f"Base URL: {settings.llm_base_url}")
    print(f"API Key: {settings.llm_api_key[:20]}...")

    service = LLMService()

    try:
        print("\nCalling Groq API...")
        result = await service.generate(
            "You are a code analysis expert. Return only valid JSON.",
            'Identify the approach in this code. Return: {"primary_approach": "Dynamic Programming"}',
            0.1
        )
        print("\n✓ SUCCESS!")
        print("Response:", result[:200])
        return True

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    print(f"\nTest: {'PASSED' if success else 'FAILED'}")
