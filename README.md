# robots,logs,bugs,fix
This repo is about analyzing robot job logs, finding the root cause, fixing issues, and preventing future failures.
<img width="1536" height="1024" alt="architecture" src="https://github.com/user-attachments/assets/253bd916-95b9-453b-bb98-92cd65c4c95e" />
# Robots Logs Bug Fix

AI-powered analyzer for UiPath robot job logs that identifies root causes, recommends fixes, and provides prevention strategies for recurring failures.

## Overview

UiPath automation environments can generate a large number of job logs when robots execute business processes. Finding the root cause of a failure manually can be time-consuming, especially when similar errors have already occurred in the past.

This project uses **RAG (Retrieval-Augmented Generation)**, **vector search**, and an **LLM** to analyze UiPath errors using both:

- Historical robot errors
- UiPath technical knowledge
- Semantic similarity search
- LLM-based reasoning

The goal is to move from:

```text
Robot Failure
     ↓
Manual Log Investigation
     ↓
Search Documentation
     ↓
Find Similar Historical Errors
     ↓
Determine Root Cause
     ↓
Find Solution
How RAG Works in This Project

The system does not send the error directly to the LLM.

Instead, it first retrieves relevant information.

1. Historical Error Retrieval

The new error is converted into an embedding vector.

The vector is compared against historical UiPath errors stored in Qdrant.

New Error
    ↓
Embedding
    ↓
Qdrant Semantic Search
    ↓
Similar Historical Errors

The current implementation retrieves the top 5 results and applies a similarity threshold.

Top-K: 5
Similarity Threshold: 0.20
Distance: Cosine
2. Knowledge Retrieval

The same error is also used to search the UiPath knowledge base.

The knowledge base contains Markdown documents such as:

data/knowledge/
├── debugging.md
├── error-handling-guide.md
└── reframework-guide.md

The documents are split into sections and chunks before being embedded and stored in Qdrant.

3. Context Construction

The ContextBuilder combines:

New Error
+
Similar Historical Errors
+
Relevant UiPath Knowledge

into a structured context for the LLM.

4. LLM Analysis

The context is sent to the LLM through OpenRouter.

The LLM returns structured information:

Root Cause
Explanation
Recommended Solution
Prevention
Confidence

The response is validated using Pydantic.

Technical Highlights
Embeddings

The project uses:

Sentence Transformers
all-MiniLM-L6-v2

Technical characteristics:

384-dimensional embeddings
Semantic representation of error messages
Used for both historical errors and knowledge chunks
Suitable for semantic similarity retrieval
Vector Database

The project uses Qdrant as the vector database.

A single Qdrant client manages two collections:

Qdrant
│
├── uipath_errors
│
└── uipath_knowledge
uipath_errors

Stores historical UiPath errors together with their metadata.

Example metadata:

log_id
timestamp
job_key
process_name
workflow
robot
environment
status
error_code
error_category
severity
error_message
retry_count
queue_item
uipath_knowledge

Stores UiPath technical knowledge chunks.

Each chunk contains:

source
heading
content
embedding
LLM Output

The LLM response is represented by the following Pydantic model:

class ErrorAnalysis(BaseModel):
    root_cause: str
    explanation: str
    recommended_solution: str
    prevention: str
    confidence: float

The confidence value is constrained between:

0.0 and 1.0

This provides a predictable structure for downstream applications.

Project Structure
JobsErrorLogsAnalyzer/
│
├── data/
│   ├── uipath_error_logs.xlsx
│   ├── qdrant/
│   └── knowledge/
│       ├── debugging.md
│       ├── error-handling-guide.md
│       └── reframework-guide.md
│
├── src/
│   └── uipath_agent/
│       │
│       ├── main.py
│       ├── config.py
│       ├── log_reader.py
│       ├── retriever.py
│       ├── context_builder.py
│       ├── analyzer.py
│       ├── knowledge_loader.py
│       ├── knowledge_ingestor.py
│       ├── knowledge_retriever.py
│       ├── ingestion_qdrant.py
│       │
│       ├── models/
│       │   ├── error.py
│       │   └── analysis.py
│       │
│       ├── embeddings/
│       │   └── embedder.py
│       │
│       └── vectorstore/
│           ├── qdrant_store.py
│           └── knowledge_store.py
│
├── tests/
│   ├── __init__.py
│   └── test_log_reader.py
│
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
Technology Stack
Technology	Purpose
Python	Application development
Pydantic	Data validation and structured models
Pandas	Excel/log data processing
OpenPyXL	Excel file handling
Sentence Transformers	Text embeddings
all-MiniLM-L6-v2	Embedding model
Qdrant	Vector database
OpenRouter	LLM API access
GPT-5.6 Luna	Error analysis
Pytest	Testing
Ruff	Code quality and linting
python-dotenv	Environment configuration
Configuration

Create a .env file in the project root:

OPENROUTER_API_KEY=YOUR_API_KEY
LOG_FILE_PATH=data/uipath_error_logs.xlsx
KNOWLEDGE_DIR=data/knowledge

API keys should never be committed to Git.

The .env file is excluded through .gitignore.

Installation

Clone the repository:

git clone https://github.com/rza4ev/robots-logs-bugs-fix.git

Move into the project directory:

cd robots-logs-bugs-fix

Create a virtual environment:

python -m venv .venv

Install the project dependencies:

pip install -e .

For development dependencies:

pip install -e ".[dev]"
Running the Analyzer

Run the application with:

python -m uipath_agent.main

If the virtual environment cannot be activated because of Windows execution-policy restrictions, use the virtual environment interpreter directly:

.\.venv\Scripts\python.exe -m uipath_agent.main
Example

Example input:

The Confirm button cannot be found on the screen.

The system performs:

1. Create error representation
        ↓
2. Generate embedding
        ↓
3. Search historical errors
        ↓
4. Search UiPath knowledge
        ↓
5. Build LLM context
        ↓
6. Send context to LLM
        ↓
7. Validate structured response

Example output:

========== LLM ANALYSIS ==========

Root Cause:
The target UI element could not be located during execution.

Explanation:
The historical errors indicate that similar failures
were caused by UI elements becoming unavailable or
selectors no longer matching the application state.

Recommended Solution:
Verify the selector and application state before interacting
with the Confirm button. Consider adding appropriate waits
and validating element availability.

Prevention:
Use stable selectors, appropriate synchronization,
and explicit element existence checks.

Confidence:
0.89

===================================

The exact output depends on the retrieved historical errors, knowledge chunks, and LLM response.

Design Principles

The project follows several principles:

Separation of concerns

Each component has a specific responsibility:

Log Reader
    ↓
Data Model
    ↓
Embedding
    ↓
Vector Store
    ↓
Retriever
    ↓
Context Builder
    ↓
LLM Analyzer
Structured data

Pydantic models are used to validate:

UiPath errors
LLM analysis results
Semantic retrieval

The system uses vector similarity instead of relying only on exact keyword matching.

Knowledge grounding

The LLM receives relevant historical errors and UiPath documentation as context.

Single Qdrant client

The application uses one shared Qdrant client for the two collections:

uipath_errors
uipath_knowledge

This avoids multiple local Qdrant storage instances accessing the same storage directory.

Current Status

The current version provides a Python CLI-based proof of concept with:

Historical UiPath error ingestion
Semantic error retrieval
UiPath knowledge ingestion
Semantic knowledge retrieval
RAG context construction
LLM-based error analysis
Structured Pydantic output
Local Qdrant vector storage
