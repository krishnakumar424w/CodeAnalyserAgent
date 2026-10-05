"""
FastAPI main application
"""

import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.models import CodeAnalysisRequest, CodeAnalysisResponse, HealthResponse
from app.services import analysis_service
from app.config import settings, SUPPORTED_LANGUAGES

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Code Classifier",
    description="Multi-agent code analysis system for competitive programming",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "message": "An unexpected error occurred"},
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AI Code Classifier",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "health": "/api/health",
            "analyze": "/api/analyze",
        },
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint

    Returns:
        Health status
    """
    return HealthResponse(status="ok")


@app.post("/api/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """
    Analyze competitive programming code

    Args:
        request: Code analysis request

    Returns:
        Complete analysis including approach, complexity, and difficulty

    Raises:
        HTTPException: If validation or analysis fails
    """
    try:
        # Validate language
        if request.language not in SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: {request.language}. Must be one of: {', '.join(SUPPORTED_LANGUAGES)}",
            )

        # Validate lengths
        if len(request.code) > settings.max_code_length:
            raise HTTPException(
                status_code=400, detail=f"Code exceeds maximum length of {settings.max_code_length} characters"
            )

        if len(request.problem) > settings.max_problem_length:
            raise HTTPException(
                status_code=400,
                detail=f"Problem statement exceeds maximum length of {settings.max_problem_length} characters",
            )

        # Perform analysis
        logger.info(f"Received analysis request for {request.language}")
        result = await analysis_service.analyze_code(request)

        return result

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
