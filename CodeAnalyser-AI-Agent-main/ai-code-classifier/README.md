# AI Code Classifier

A production-ready multi-agent system for analyzing competitive programming solutions using AI.

## 🎯 Overview

AI Code Classifier analyzes competitive programming code to determine:

- **Programming Language**: C++, Java, Python
- **Algorithmic Approach**: 26 predefined categories
- **Data Structures**: Arrays, Hash Maps, Trees, etc.
- **Complexity**: Time and Space complexity
- **Difficulty**: Easy, Medium, Hard (based on problem requirements)
- **Confidence Score**: 0.0 - 1.0
- **Implementation Patterns**: Detected coding patterns

## 🏗️ Architecture

### Multi-Agent System

```
┌─────────────────────────────────────────┐
│      Supervisor Agent (Coordinator)      │
└────────────┬────────────────────────────┘
             │
   ┌─────────┼──────────┬─────────────┐
   │         │          │             │
   ▼         ▼          ▼             ▼
┌────────┐ ┌───────┐ ┌──────────┐ ┌──────────┐
│Approach│ │Code   │ │Complexity│ │Difficulty│
│Agent   │ │Agent  │ │Analyzer  │ │Agent     │
└────────┘ └───────┘ └──────────┘ └──────────┘
```

### Components

```
app/
├── main.py                  # FastAPI application
├── config.py                # Configuration settings
├── models/                  # Pydantic models
│   ├── request_models.py    # Request validation
│   └── response_models.py   # Response validation
├── agents/                  # Multi-agent system
│   ├── supervisor_agent.py  # Coordinator
│   ├── approach_agent.py    # Approach identification
│   ├── difficulty_agent.py  # Difficulty classification
│   └── code_analysis_agent.py # Pattern detection
├── analyzers/               # Static analyzers
│   ├── complexity_analyzer.py # Complexity analysis
│   └── language_analyzer.py   # Language detection
├── prompts/                 # LLM prompts
│   ├── master_prompt.py
│   ├── approach_prompt.py
│   └── difficulty_prompt.py
├── services/                # Service layer
│   ├── llm_service.py       # LLM abstraction
│   └── analysis_service.py  # Analysis coordination
└── utils/                   # Utilities
    ├── json_parser.py       # Safe JSON parsing
    └── validators.py        # Validation helpers
```

## 🚀 Installation

### Prerequisites

- Python 3.10+
- Groq API key (free tier available)

### Steps

1. **Clone/Navigate to project**:
```bash
cd ai-code-classifier
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
# LLM Configuration
LLM_API_KEY=gsk_your_groq_api_key_here
LLM_MODEL=llama-3.3-70b-versatile
LLM_BASE_URL=https://api.groq.com/openai/v1

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Security Limits
MAX_CODE_LENGTH=50000
MAX_PROBLEM_LENGTH=10000
```

Get your free Groq API key: https://console.groq.com/keys

## 🏃 Running the Server

### Method 1: Using run.py
```bash
python run.py
```

### Method 2: Using uvicorn
```bash
uvicorn app.main:app --reload
```

### Method 3: Production mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Server will start at: **http://localhost:8000**

## 📡 API Documentation

### Endpoints

#### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

#### POST /api/analyze

Analyze competitive programming code.

**Request:**
```json
{
  "language": "python",
  "problem": "Given an array of integers, find the maximum subarray sum.",
  "code": "def maxSubArray(nums):\n    max_sum = float('-inf')\n    current_sum = 0\n    for num in nums:\n        current_sum = max(num, current_sum + num)\n        max_sum = max(max_sum, current_sum)\n    return max_sum"
}
```

**Response:**
```json
{
  "language": "Python",
  "primary_approach": "Dynamic Programming",
  "secondary_approaches": ["Loop"],
  "data_structures": ["Array"],
  "difficulty": "Medium",
  "confidence": 0.85,
  "time_complexity": "O(N)",
  "space_complexity": "O(1)",
  "reasoning": "The solution uses Kadane's algorithm, which is a dynamic programming approach that tracks the maximum subarray ending at each position. The problem requires understanding of optimal substructure and efficient state tracking.",
  "detected_patterns": ["State Tracking", "Greedy Choice", "Iteration"]
}
```

### Example Requests

#### Python - Dynamic Programming
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "problem": "Find maximum subarray sum (Kadane algorithm)",
    "code": "def maxSubArray(nums):\n    max_sum = current_sum = nums[0]\n    for num in nums[1:]:\n        current_sum = max(num, current_sum + num)\n        max_sum = max(max_sum, current_sum)\n    return max_sum"
  }'
```

#### Java - Binary Search
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "language": "java",
    "problem": "Search for target in sorted array",
    "code": "public int binarySearch(int[] arr, int target) {\n    int left = 0, right = arr.length - 1;\n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        if (arr[mid] == target) return mid;\n        if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}"
  }'
```

#### C++ - Graph DFS
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "language": "c++",
    "problem": "Traverse graph using depth-first search",
    "code": "#include <vector>\nvoid dfs(vector<vector<int>>& graph, int node, vector<bool>& visited) {\n    visited[node] = true;\n    for (int neighbor : graph[node]) {\n        if (!visited[neighbor]) {\n            dfs(graph, neighbor, visited);\n        }\n    }\n}"
  }'
```

## 🎯 Supported Languages

- **C++** (cpp, c++)
- **Java** (java)
- **Python** (python, py)

## 📚 Approach Taxonomy

The system uses 26 predefined approaches:

| Approach | Description |
|----------|-------------|
| Loop | Simple iteration |
| Nested Loop | Multiple nested loops |
| Recursion | Recursive function calls |
| Backtracking | Exploration with backtracking |
| Dynamic Programming | DP with memoization/tabulation |
| Greedy | Greedy choice strategy |
| DFS | Depth-first search |
| BFS | Breadth-first search |
| Binary Search | Binary search algorithm |
| Two Pointers | Two pointer technique |
| Sliding Window | Sliding window technique |
| Prefix Sum | Prefix sum array |
| Sorting | Sorting-based approach |
| Hashing | Hash map/set usage |
| Stack | Stack data structure |
| Queue | Queue data structure |
| Heap | Heap/priority queue |
| Graph | Graph algorithms |
| Tree | Tree algorithms |
| Union Find | Disjoint set union |
| Divide and Conquer | Divide and conquer |
| Bit Manipulation | Bitwise operations |
| Math | Mathematical approach |
| String Algorithm | String-specific algorithms |
| Simulation | Direct simulation |
| Other | Other approaches |

## 🎓 Difficulty Classification

### Methodology

Difficulty is **NOT** determined solely from code length or complexity.

The system considers:

1. **Problem Statement**: What the problem asks for
2. **Input Constraints**: Size of N, M, etc.
3. **Expected Algorithm**: Required algorithmic approach
4. **Number of Concepts**: How many concepts must be combined
5. **Algorithmic Complexity**: Time/space requirements
6. **Implementation Complexity**: Difficulty to implement correctly
7. **Edge Cases**: Number and subtlety of edge cases
8. **Data Structures**: Required data structures
9. **Optimization**: Need for optimal solutions
10. **Time/Memory Constraints**: Strict limits

### Classification Levels

- **Easy**: Single concept, straightforward implementation, small constraints
- **Medium**: Multiple concepts, moderate optimization, larger constraints
- **Hard**: Advanced algorithms, complex optimization, very large constraints

### Examples

**Easy Problem (Long Code)**:
```
Problem: Print all elements in an array
Code: 500 lines with extensive error handling
Difficulty: Easy (simple concept despite code length)
```

**Hard Problem (Short Code)**:
```
Problem: Find median of two sorted arrays in O(log(m+n))
Code: 20 lines using binary search
Difficulty: Hard (requires advanced algorithm)
```

## 🔒 Security

### Implemented Safeguards

✅ **Input Validation**: All inputs validated with Pydantic  
✅ **Length Limits**: Maximum code length (50,000 chars)  
✅ **No Code Execution**: Code is NEVER executed  
✅ **No eval()/exec()**: No dynamic code execution  
✅ **Environment Variables**: Secrets in .env file  
✅ **Request Validation**: Strict type checking  
✅ **Error Handling**: Safe error responses  

### Important Notes

- The system **analyzes** code only
- User code is **never executed**
- No shell commands with user input
- No file system writes from user input

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
pytest tests/test_api.py
pytest tests/test_approach.py
pytest tests/test_difficulty.py
pytest tests/test_complexity.py
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Test Categories

1. **API Tests** (`test_api.py`):
   - Health check
   - Request validation
   - Error handling
   - Complete analysis workflow

2. **Approach Tests** (`test_approach.py`):
   - Approach identification
   - Invalid JSON handling
   - Multiple languages

3. **Difficulty Tests** (`test_difficulty.py`):
   - Easy, Medium, Hard classification
   - Confidence scoring
   - Invalid responses

4. **Complexity Tests** (`test_complexity.py`):
   - Time complexity detection
   - Space complexity detection
   - Various algorithm patterns

### Mocking

Tests use **mocked LLM service** to avoid real API calls.

The mock returns deterministic responses based on prompt content.

## 📊 Example Workflow

```python
# 1. User submits code via POST /api/analyze
{
  "language": "python",
  "problem": "Find max subarray sum",
  "code": "def maxSubArray(nums): ..."
}

# 2. Supervisor Agent coordinates analysis:
#    a. Approach Agent identifies: "Dynamic Programming"
#    b. Complexity Analyzer determines: O(N) time, O(1) space
#    c. Code Agent detects: ["State Tracking", "Iteration"]
#    d. Difficulty Agent classifies: "Medium" (0.85 confidence)

# 3. System returns complete analysis:
{
  "language": "Python",
  "primary_approach": "Dynamic Programming",
  "difficulty": "Medium",
  "time_complexity": "O(N)",
  ...
}
```

## 🛠️ Development

### Code Quality

```bash
# Format code
black app/ tests/

# Lint code
ruff check app/ tests/

# Type checking (optional)
mypy app/
```

### Project Structure Best Practices

- **Separation of Concerns**: Each module has a single responsibility
- **Dependency Injection**: Services injected, not hardcoded
- **Error Handling**: Comprehensive exception handling
- **Logging**: Structured logging throughout
- **Testing**: Comprehensive test coverage
- **Documentation**: Docstrings and type hints

## 🐛 Troubleshooting

### Issue: LLM API Key Not Found

**Solution**: Ensure `.env` file exists and contains `LLM_API_KEY=your_key_here`

### Issue: Port Already in Use

**Solution**: Change port in `.env` or kill existing process:
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -ti:8000 | xargs kill
```

### Issue: Import Errors

**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Tests Failing

**Solution**: Tests use mocked LLM service and don't require real API keys.
```bash
pytest -v  # Verbose output
pytest --tb=short  # Shorter traceback
```

## 📝 API Design Principles

1. **Clear Separation**: Business logic separate from API routes
2. **Validation**: Pydantic models for request/response validation
3. **Error Handling**: Appropriate HTTP status codes
4. **Logging**: Structured logging for debugging
5. **Security**: No code execution, input validation
6. **Testability**: Mocked dependencies for unit tests

## 🚀 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY run.py .

EXPOSE 8000
CMD ["python", "run.py"]
```

### Environment Variables

Set in production environment:
- `LLM_API_KEY`: Your Groq API key
- `DEBUG=false`: Disable debug mode
- `HOST=0.0.0.0`: Allow external connections
- `PORT=8000`: Server port

## 📄 License

MIT License

## 🙏 Acknowledgments

- FastAPI framework
- Groq LLM API
- Pydantic validation

---

**Built with ❤️ for competitive programmers**
