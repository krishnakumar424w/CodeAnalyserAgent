import os
import sys
import re
import subprocess
import tempfile
import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(
    os.path.dirname(__file__),
    "CodeAnalyser-AI-Agent-main", "ai-code-classifier", ".env"
)
load_dotenv(ENV_PATH)

API_KEY = os.getenv("LLM_API_KEY", "")
MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.groq.com")

if "groq.com" in BASE_URL and "/openai/v1" not in BASE_URL:
    BASE_URL = BASE_URL.rstrip("/") + "/openai/v1"
CHAT_URL = BASE_URL.rstrip("/") + "/chat/completions"

LANG_PATTERNS = {
    "java": [r'\bclass\s+\w+', r'\bpublic\s+static\s+void\s+main', r'System\.out\.print'],
    "cpp": [r'#include\s*<', r'using\s+namespace\s+std', r'cout\s*<<', r'int\s+main\s*\('],
    "python": [r'^def\s+\w+', r'^import\s+\w+', r'^from\s+\w+', r'print\s*\(', r'^if\s+__name__'],
}


def detect_language(code):
    scores = {"java": 0, "cpp": 0, "python": 0}
    for lang, patterns in LANG_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, code, re.MULTILINE):
                scores[lang] += 1
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return None
    return best


def run_code(code, language):
    try:
        if language == "python":
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
                f.write(code)
                f.flush()
                path = f.name
            result = subprocess.run(
                ["python", path], capture_output=True, text=True, timeout=30
            )
            os.unlink(path)
            return result.stdout, result.stderr

        elif language == "java":
            match = re.search(r'class\s+(\w+)', code)
            if not match:
                return "", "Error: Could not find class name in Java code."
            class_name = match.group(1)
            tmpdir = tempfile.mkdtemp()
            src = os.path.join(tmpdir, f"{class_name}.java")
            with open(src, "w") as f:
                f.write(code)
            comp = subprocess.run(
                ["javac", src], capture_output=True, text=True, timeout=30
            )
            if comp.returncode != 0:
                return "", f"Compilation Error:\n{comp.stderr}"
            result = subprocess.run(
                ["java", "-cp", tmpdir, class_name],
                capture_output=True, text=True, timeout=30
            )
            for fname in os.listdir(tmpdir):
                os.unlink(os.path.join(tmpdir, fname))
            os.rmdir(tmpdir)
            return result.stdout, result.stderr

        elif language == "cpp":
            with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False, mode="w") as f:
                f.write(code)
                f.flush()
                src = f.name
            out_exe = src.replace(".cpp", ".exe")
            comp = subprocess.run(
                ["g++", src, "-o", out_exe], capture_output=True, text=True, timeout=30
            )
            if comp.returncode != 0:
                os.unlink(src)
                return "", f"Compilation Error:\n{comp.stderr}"
            result = subprocess.run(
                [out_exe], capture_output=True, text=True, timeout=30
            )
            os.unlink(src)
            if os.path.exists(out_exe):
                os.unlink(out_exe)
            return result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out (30s limit)."
    except Exception as e:
        return "", f"Error: {e}"


def analyze_with_groq(code, language):
    prompt = f"""Analyze the following {language.upper()} code. Return ONLY a JSON object with these fields:
- "approach": the primary algorithmic approach used (e.g., Recursion, Dynamic Programming, Greedy, etc.)
- "time_complexity": Big-O time complexity (e.g., "O(2^n)")
- "space_complexity": Big-O space complexity (e.g., "O(n)")
- "reasoning": a brief explanation of why these complexities apply

Code:
```{language}
{code}
```"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert algorithm analyst. Respond ONLY with valid JSON, no markdown fences."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }

    try:
        resp = requests.post(CHAT_URL, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        import json
        text = content.strip()
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        return json.loads(text)
    except requests.exceptions.HTTPError as e:
        return {"error": f"API Error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}


def print_separator(char="=", width=60):
    print(char * width)


def main():
    print_separator()
    print("  CODE ANALYSER - AI Agent")
    print("  Supports: Python | Java | C++")
    print_separator()
    print("\nPaste your code below, then press Enter on an empty line to finish:\n")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "" and lines and lines[-1].strip() == "":
            lines.pop()
            break
        lines.append(line)

    code = "\n".join(lines)
    if not code.strip():
        print("No code provided. Exiting.")
        return

    print_separator("-")
    print("[1/3] Detecting language...")
    language = detect_language(code)
    if not language:
        print("Could not detect language. Exiting.")
        return
    print(f"  Detected: {language.upper()}")

    print_separator("-")
    print("[2/3] Running code...")
    stdout, stderr = run_code(code, language)
    print("\n--- Execution Output ---")
    if stdout:
        print(stdout.rstrip())
    if stderr:
        print(f"[stderr] {stderr.rstrip()}")
    if not stdout and not stderr:
        print("(no output)")

    print_separator("-")
    print("[3/3] Analyzing approach & complexity (Groq API)...")
    analysis = analyze_with_groq(code, language)

    print_separator("=")
    print("  ANALYSIS RESULT")
    print_separator("=")

    if "error" in analysis:
        print(f"  Error: {analysis['error']}")
    else:
        print(f"  Language         : {language.upper()}")
        print(f"  Approach         : {analysis.get('approach', 'N/A')}")
        print(f"  Time Complexity  : {analysis.get('time_complexity', 'N/A')}")
        print(f"  Space Complexity : {analysis.get('space_complexity', 'N/A')}")
        print(f"  Reasoning        : {analysis.get('reasoning', 'N/A')}")

    print_separator("=")


if __name__ == "__main__":
    main()
