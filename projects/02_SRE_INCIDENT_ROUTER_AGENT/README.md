# 🚨 SRE Incident Responder Agent

An autonomous SRE agent that triages infrastructure outages, isolates root causes from logs/metrics, and provides resolution runbooks.

Built with **LangChain**, **LangGraph**, and **Groq (Llama 3.3 70B)**.

---

## Data Layer

Includes a mock data layer simulating production telemetry (Datadog metrics), application log streams (Splunk/Elastic), deployment registries (Kubernetes configs), and internal runbook knowledge bases (Confluence).

---

## Tools Included

- `get_system_metrics`: Fetches latency, 5xx error rates, and operational status.
- `fetch_application_logs`: Queries application stdout/stderr streams to extract stack traces.
- `get_deployment_details`: Inspects active deployment configs and environment variables.
- `query_internal_runbooks`: Searches internal runbook database for matching exception resolution steps.

---

## Setup

1. Install dependencies: `uv sync`
2. Add `.env` in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```
3. Open `app.ipynb` and run all cells top to bottom using the `.venv` kernel.

---

