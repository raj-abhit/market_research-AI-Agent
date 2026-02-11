# InsightPilot AI Agent Crew

A multi-agent CrewAI system that evaluates an AI product idea end-to-end and generates an investor-style business memo.

This project coordinates specialist agents for:
- Market sizing and trend analysis
- Competitive intelligence
- Customer insight synthesis
- Product strategy
- Final business recommendation

The default run produces a final report at `reports/report.md`.

## Architecture

The crew runs sequentially through five agents:
1. `Market Research Specialist`
2. `Competitive Intelligence Analyst`
3. `Customer Insights Researcher`
4. `Product Strategy Advisor`
5. `Business Analyst and Report Synthesizer`

Configuration files:
- Agents: `src/market_research_crew/config/agents.yaml`
- Tasks: `src/market_research_crew/config/tasks.yaml`
- Crew assembly and runtime controls: `src/market_research_crew/crew.py`
- Entry point: `src/market_research_crew/main.py`

## Tech Stack

- Python 3.10-3.13
- CrewAI
- crewAI tools (`SerperDevTool`, `ScrapeWebsiteTool`, `SeleniumScrapingTool`)
- LLM provider: Groq (current default), with model selection via `.env`
- Dependency/runtime manager: `uv`

## Prerequisites

- Python installed
- `uv` installed
- API keys for selected providers/tools

Install `uv` if needed:

```bash
pip install uv
```

## Setup

1. Install dependencies:

```bash
crewai install
```

2. Create and populate `.env`:

```env
MODEL=groq/llama-3.1-8b-instant
GROQ_API_KEY=your_groq_key
SERPER_API_KEY=your_serper_key

MAX_TOKENS=500
MAX_ITER=2
MAX_RPM=1
```

Notes:
- `.env` is git-ignored.
- If keys were ever committed/shared, rotate them immediately.

## Run

```bash
crewai run
```

Output:
- Final report: `reports/report.md`

## Runtime Controls

These variables help balance quality, speed, and rate limits:

- `MODEL`: provider/model identifier used by CrewAI
- `MAX_TOKENS`: max tokens per model response
- `MAX_ITER`: max reasoning/tool loop iterations per agent task
- `MAX_RPM`: max requests per minute at crew level

Current tuning is optimized to reduce Groq 429 failures while preserving report quality.

## Common Issues

### 1. `404 model not found`
Use a currently supported model in `.env`.

### 2. `429 rate_limit_exceeded`
Reduce prompt pressure by lowering `MAX_TOKENS` and/or `MAX_ITER`, keep `MAX_RPM` low, and rerun after cooldown.

### 3. Missing LiteLLM proxy dependencies
Install:

```bash
uv pip install --python .\\.venv\\Scripts\\python.exe "litellm[proxy]"
```

## Project Structure

```text
market_research_crew/
|-- src/market_research_crew/
|   |-- config/
|   |   |-- agents.yaml
|   |   `-- tasks.yaml
|   |-- crew.py
|   `-- main.py
|-- reports/
|   `-- report.md
|-- .env
|-- .gitignore
`-- pyproject.toml
```

## License

Add your preferred license before publishing (MIT recommended for open source).
