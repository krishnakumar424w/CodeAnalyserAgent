"""
LLM service abstraction
"""

import logging
from typing import Optional
import requests
from app.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Abstraction layer for LLM API calls"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key or settings.llm_api_key
        self.model = model or settings.llm_model
        self.base_url = base_url or settings.llm_base_url

    async def generate(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.1
    ) -> str:
        """
        Generate completion from LLM

        Args:
            system_prompt: System prompt
            user_prompt: User prompt
            temperature: Sampling temperature

        Returns:
            Generated text

        Raises:
            Exception: If LLM call fails
        """
        try:
            # Groq API uses OpenAI-compatible endpoint
            if "groq.com" in self.base_url and "/openai/v1" not in self.base_url:
                url = f"{self.base_url}/openai/v1/chat/completions"
            else:
                url = f"{self.base_url}/chat/completions"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": temperature,
                "response_format": {"type": "json_object"},
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            data = response.json()
            content = data["choices"][0]["message"]["content"]

            logger.info(f"LLM generation successful, length: {len(content)}")
            return content

        except requests.exceptions.Timeout:
            logger.error("LLM request timeout")
            raise Exception("LLM request timeout")
        except requests.exceptions.RequestException as e:
            logger.error(f"LLM request failed: {e}")
            raise Exception(f"LLM request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            logger.error(f"Invalid LLM response format: {e}")
            raise Exception("Invalid LLM response format")


# Global LLM service instance
llm_service = LLMService()
