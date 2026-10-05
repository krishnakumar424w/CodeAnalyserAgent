"""
Approach analysis agent
"""

import logging
from app.models import ApproachAnalysis
from app.services.llm_service import llm_service
from app.prompts import APPROACH_SYSTEM_PROMPT, build_approach_user_prompt
from app.utils import safe_json_parse, validate_approach

logger = logging.getLogger(__name__)


class ApproachAgent:
    """Agent for identifying algorithmic approaches"""

    def __init__(self):
        self.llm = llm_service

    async def analyze(self, language: str, code: str) -> ApproachAnalysis:
        """
        Analyze algorithmic approach

        Args:
            language: Programming language
            code: Source code

        Returns:
            Approach analysis result
        """
        try:
            user_prompt = build_approach_user_prompt(language, code)

            # Call LLM
            response = await self.llm.generate(APPROACH_SYSTEM_PROMPT, user_prompt)

            # Parse JSON
            data = safe_json_parse(
                response,
                default={
                    "primary_approach": "Other",
                    "secondary_approaches": [],
                    "data_structures": [],
                    "detected_patterns": [],
                },
            )

            # Validate primary approach
            primary = data.get("primary_approach", "Other")
            if not validate_approach(primary):
                logger.warning(f"Invalid primary approach: {primary}, using 'Other'")
                primary = "Other"

            # Validate secondary approaches
            secondary = data.get("secondary_approaches", [])
            secondary = [s for s in secondary if validate_approach(s)]

            result = ApproachAnalysis(
                primary_approach=primary,
                secondary_approaches=secondary,
                data_structures=data.get("data_structures", []),
                detected_patterns=data.get("detected_patterns", []),
            )

            logger.info(f"Approach analysis: {result.primary_approach}")
            return result

        except Exception as e:
            logger.error(f"Approach analysis failed: {e}")
            # Return safe default
            return ApproachAnalysis(
                primary_approach="Other",
                secondary_approaches=[],
                data_structures=[],
                detected_patterns=[],
            )
