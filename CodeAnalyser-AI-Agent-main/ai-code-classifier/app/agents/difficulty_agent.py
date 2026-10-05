"""
Difficulty classification agent
"""

import logging
from app.models import DifficultyAnalysis
from app.services.llm_service import llm_service
from app.prompts import DIFFICULTY_SYSTEM_PROMPT, build_difficulty_user_prompt
from app.utils import safe_json_parse

logger = logging.getLogger(__name__)


class DifficultyAgent:
    """Agent for classifying problem difficulty"""

    def __init__(self):
        self.llm = llm_service

    async def analyze(
        self, problem: str, approach: str, complexity: str
    ) -> DifficultyAnalysis:
        """
        Analyze problem difficulty

        Args:
            problem: Problem statement
            approach: Detected approach
            complexity: Time complexity

        Returns:
            Difficulty analysis result
        """
        try:
            user_prompt = build_difficulty_user_prompt(problem, approach, complexity)

            # Call LLM
            response = await self.llm.generate(DIFFICULTY_SYSTEM_PROMPT, user_prompt)

            # Parse JSON
            data = safe_json_parse(
                response,
                default={
                    "difficulty": "Medium",
                    "confidence": 0.5,
                    "reasoning": "Unable to determine difficulty precisely",
                },
            )

            # Validate difficulty
            difficulty = data.get("difficulty", "Medium")
            if difficulty not in ["Easy", "Medium", "Hard"]:
                logger.warning(f"Invalid difficulty: {difficulty}, using 'Medium'")
                difficulty = "Medium"

            # Validate confidence
            confidence = float(data.get("confidence", 0.5))
            confidence = max(0.0, min(1.0, confidence))

            result = DifficultyAnalysis(
                difficulty=difficulty,
                confidence=confidence,
                reasoning=data.get(
                    "reasoning", "Difficulty determined based on problem requirements"
                ),
            )

            logger.info(
                f"Difficulty analysis: {result.difficulty} (confidence: {result.confidence:.2f})"
            )
            return result

        except Exception as e:
            logger.error(f"Difficulty analysis failed: {e}")
            # Return safe default
            return DifficultyAnalysis(
                difficulty="Medium",
                confidence=0.5,
                reasoning="Unable to determine difficulty precisely due to analysis error",
            )
