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
