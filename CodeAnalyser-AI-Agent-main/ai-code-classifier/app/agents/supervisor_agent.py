"""
Supervisor agent coordinating all analysis agents
"""

import logging
from app.models import CodeAnalysisResponse
from app.utils import validate_language
from app.agents.approach_agent import ApproachAgent
from app.agents.difficulty_agent import DifficultyAgent
from app.agents.code_analysis_agent import CodeAnalysisAgent
from app.analyzers.complexity_analyzer import ComplexityAnalyzer

logger = logging.getLogger(__name__)


class SupervisorAgent:
    """
    Supervisor agent that coordinates all specialized agents
    """

    def __init__(self):
        self.approach_agent = ApproachAgent()
        self.difficulty_agent = DifficultyAgent()
        self.code_agent = CodeAnalysisAgent()
        self.complexity_analyzer = ComplexityAnalyzer()

    async def analyze(
        self, language: str, problem: str, code: str
    ) -> CodeAnalysisResponse:
        """
        Coordinate complete code analysis

        Args:
            language: Programming language
            problem: Problem statement
            code: Source code

        Returns:
            Complete analysis response

        Raises:
            ValueError: If language is not supported
            Exception: If analysis fails
        """
        # Validate language
        normalized_lang = validate_language(language)
        if not normalized_lang:
            raise ValueError(
                f"Unsupported language: {language}. Must be one of: C++, Java, Python"
            )

        logger.info(f"Supervisor starting analysis for {normalized_lang}")

        try:
            # Step 1: Analyze approach and patterns
            logger.info("Step 1: Analyzing algorithmic approach")
            approach_result = await self.approach_agent.analyze(normalized_lang, code)

            # Step 2: Analyze complexity
            logger.info("Step 2: Analyzing complexity")
            complexity_result = self.complexity_analyzer.analyze(
                code, approach_result.primary_approach
            )

            # Step 3: Verify code implementation
            logger.info("Step 3: Verifying code patterns")
            code_patterns = await self.code_agent.analyze(code, approach_result)

            # Step 4: Determine difficulty
            logger.info("Step 4: Determining difficulty")
            difficulty_result = await self.difficulty_agent.analyze(
                problem, approach_result.primary_approach, complexity_result.time_complexity
            )

            # Combine results
            logger.info("Combining analysis results")
            response = CodeAnalysisResponse(
                language=normalized_lang,
                primary_approach=approach_result.primary_approach,
                secondary_approaches=approach_result.secondary_approaches,
                data_structures=approach_result.data_structures,
                difficulty=difficulty_result.difficulty,
                confidence=difficulty_result.confidence,
                time_complexity=complexity_result.time_complexity,
                space_complexity=complexity_result.space_complexity,
                reasoning=difficulty_result.reasoning,
                detected_patterns=code_patterns,
            )

            logger.info(f"Analysis complete: {response.difficulty} difficulty")
            return response

        except Exception as e:
            logger.error(f"Supervisor analysis failed: {e}")
            raise Exception(f"Analysis failed: {str(e)}")
