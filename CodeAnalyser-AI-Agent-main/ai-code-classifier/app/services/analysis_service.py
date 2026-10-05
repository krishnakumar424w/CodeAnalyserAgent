"""
Analysis service coordinating all agents
"""

import logging
from app.models import CodeAnalysisRequest, CodeAnalysisResponse
from app.agents.supervisor_agent import SupervisorAgent

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for coordinating code analysis"""

    def __init__(self):
        self.supervisor = SupervisorAgent()

    async def analyze_code(self, request: CodeAnalysisRequest) -> CodeAnalysisResponse:
        """
        Analyze code using multi-agent system

        Args:
            request: Code analysis request

        Returns:
            Complete analysis response

        Raises:
            Exception: If analysis fails
        """
        try:
            logger.info(
                f"Starting analysis for {request.language} code, "
                f"problem length: {len(request.problem)}, "
                f"code length: {len(request.code)}"
            )

            result = await self.supervisor.analyze(
                language=request.language,
                problem=request.problem,
                code=request.code,
            )

            logger.info(f"Analysis completed: {result.difficulty} difficulty")
            return result

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise


# Global analysis service instance
analysis_service = AnalysisService()
