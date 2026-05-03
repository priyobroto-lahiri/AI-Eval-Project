# AI Evaluation Engineer Portfolio

This repository tracks my 5-month transition from Quality Engineering to AI Evaluation Engineering. It contains a collection of LLM benchmarks, EvalOps scripts, and statistical evaluation tools.

## 🚀 Current Project: Project 0.2 - LLM Batch Runner
A robust Python-based pipeline for running batch prompts through LLM APIs (starting with Gemini 1.5 Flash) with:
- **Resilient API Calls:** Nested error handling for network and safety blocks.
- **Telemetry:** Automated tracking of latency and token usage.
- **Evaluation Ready:** Outputs formatted for statistical metrics analysis.

## 📁 Repository Structure
- `src/`: Core implementation logic and scripts.
- `data/`: Sample prompts and data ingestion files (Ignored by Git, except template).
- `results/`: Output logs and evaluation results (Ignored by Git).

## 🛠 Tech Stack
- **Language:** Python 3.x
- **Libraries:** Pandas, google-genai, python-dotenv, httpx
- **Model:** Gemini 1.5 Flash (via Google Generative AI SDK)
