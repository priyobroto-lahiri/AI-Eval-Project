# Project Gemini Instructions: AI Eval Engineer Portfolio

## Workspace Context
This project is a 5-month transition from Quality Engineering to AI Evaluation Engineering. The goal is to build a professional portfolio of LLM benchmarks and EvalOps tools.

## Core Workflows
### 1. Socratic Scaffolding 2.0 (Mandatory)
... (steps 1-7)

### 2. Git-First Incremental Workflow
Before writing implementation logic, ensure the following version control steps are met:
1. **Scaffold Push:** Commit and push the project structure and documentation (README/GEMINI.md) before logic.
2. **Incremental Commits:** Commit after every successful Socratic step (e.g., after Structure, after Builder).
3. **Atomic Changes:** One feature/fix per commit with a clear "Why" in the message.

## Documentation Standards
- **PARTNERSHIP_LOG.md:** Tracks collaboration philosophy and high-level milestones.
- **PROGRESS_REPORT.md:** Tracks roadmap phases and project completion status.
- **AGENT_LOG.md:** Records technical execution and shell commands.
- **LEARNING_BLUEPRINT.md:** A durable guide for recreating this learning environment in future projects.

## Environment Notes
- **Restriction:** System Application Control policies block DLLs in local Conda environments.
- **Fix:** Use the **base Anaconda Python** environment and install libraries with `pip install --user`.
- **Command:** `python src/batch_runner.py` (or other scripts).
