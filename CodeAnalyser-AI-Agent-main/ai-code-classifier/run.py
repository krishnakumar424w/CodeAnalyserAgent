#!/usr/bin/env python3
"""
Run script for AI Code Classifier
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"Starting AI Code Classifier on {settings.host}:{settings.port}")
    print(f"Debug mode: {settings.debug}")
    print(f"LLM Model: {settings.llm_model}")

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug",
    )
