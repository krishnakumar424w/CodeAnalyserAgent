"""
Language detection and analysis
"""

import re
from typing import Optional


class LanguageAnalyzer:
    """Analyzer for detecting programming language"""

    @staticmethod
    def detect(code: str) -> Optional[str]:
        """
        Detect programming language from code

        Args:
            code: Source code

        Returns:
            Detected language or None
        """
        # C++ indicators
        if re.search(r'#include\s*<|std::|cout\s*<<|vector\s*<', code):
            return "C++"

        # Java indicators
        if re.search(
            r'public\s+class|System\.out\.print|int\[\]|String\[\]', code
        ):
            return "Java"

        # Python indicators
        if re.search(r'def\s+\w+\s*\(|import\s+\w+|print\(', code):
            return "Python"

        return None
