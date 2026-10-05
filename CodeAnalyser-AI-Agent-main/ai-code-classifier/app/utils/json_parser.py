"""
Safe JSON parsing utilities
"""

import json
import re
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def extract_json_from_text(text: str) -> Optional[str]:
    """
    Extract JSON from text that may contain markdown code blocks or extra text

    Args:
        text: Raw text that may contain JSON

    Returns:
        Extracted JSON string or None
    """
    # Remove markdown code blocks
    text = text.strip()

    # Try to find JSON between ```json and ``` or ``` and ```
    json_pattern = r"```(?:json)?\s*(\{.*?\})\s*```"
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        return match.group(1)

    # Try to find a JSON object directly
    json_pattern = r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}"
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        return match.group(0)

    # If text looks like it starts with {, try using it directly
    if text.startswith("{"):
        return text

    return None


def safe_json_parse(text: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Safely parse JSON with fallback extraction

    Args:
        text: JSON text to parse
        default: Default value if parsing fails

    Returns:
        Parsed JSON object or default
    """
    if default is None:
        default = {}

    try:
        # Try direct parsing
        return json.loads(text)
    except json.JSONDecodeError:
        logger.warning("Initial JSON parse failed, attempting extraction")

        # Try extracting JSON from text
        extracted = extract_json_from_text(text)
        if extracted:
            try:
                return json.loads(extracted)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse extracted JSON: {e}")

        # Final fallback
        logger.error("All JSON parsing attempts failed")
        return default
