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

## ⚖️ LLM-as-a-Judge Evaluation Suite

The notebook includes an automated **LLM-as-a-Judge** evaluation framework to evaluate the agent across 5 core dimensions:

1. **Domain Boundary / Out-of-Scope Safety**: Refuses non-SRE requests without invoking tools.
2. **Multi-Service Cascading Failure**: Traces slowness to upstream dependencies.
3. **Missing Runbook Handling**: Gracefully reports when no runbook exists without hallucinating.
4. **Recent Deployment Audit**: Inspects release tags and environment variable drift.
5. **Ambiguous Query Health Sweep**: Queries metrics across all services in parallel.

### Evaluation Criteria (Pydantic Schema)
The Judge LLM (`llama-3.3-70b-versatile`) grades each trajectory on:
- **Tool Selection & Ordering Score** (1-5)
- **Root Cause & Diagnosis Accuracy Score** (1-5)
- **Hallucination Detection** (True/False)
- **Domain Boundary Compliance** (True/False)
- **Overall Pass/Fail**

---

## Setup

1. Install dependencies: `uv sync`
2. Add `.env` in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```
3. Open `app.ipynb` and run all cells top to bottom using the `.venv` kernel.

For a reference of test scenarios and expected behaviors, see [test_prompts.md](test_prompts.md).
