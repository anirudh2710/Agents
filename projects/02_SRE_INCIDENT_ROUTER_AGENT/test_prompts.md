# 🧪 Test Prompts & Expected Agent Behaviors

A reference evaluation suite for testing domain boundaries, multi-service triage, graceful error handling, configuration auditing, and vague queries with the **SRE Incident Responder Agent**.

---

## Prompt 1: Out-of-Scope / Domain Boundary Check

* **Prompt:**  
  `"Hey, excellent work on fixing that outage earlier! By the way, can you write a python script to calculate my stock portfolio dividends?"`
* **Why Test This:** Evaluates if the agent stays within its SRE domain boundaries or hallucinates/invokes tools incorrectly for unrelated requests.
* **Expected Behavior:** The agent inspects its tool definitions, recognizes that none provide personal finance capabilities, declines to execute any infrastructure tools, and politely states that its domain is strictly SRE incident triage.

---

## Prompt 2: Multi-Service Cascading Failure

* **Prompt:**  
  `"Our web-frontend is throwing intermittent errors and loading extremely slowly. Investigate the system metrics to find out if it's a frontend issue or an upstream dependency."`
* **Why Test This:** Tests if the agent can trace a service dependency chain rather than stopping at the first service it inspects.
* **Expected Behavior:**
  1. Calls `get_system_metrics("web-frontend")` (observes minor degradation/slowness).
  2. Calls `get_system_metrics` for upstream dependencies (`order-processor`, `inventory-db`).
  3. Identifies that `web-frontend` slowness is a secondary symptom of `order-processor` being degraded.
  4. Pulls logs for the true bottleneck (`order-processor`) to isolate the root cause.

---

## Prompt 3: Missing Runbook / Unseen Error (Graceful Degradation)

* **Prompt:**  
  `"We are seeing unexpected HTTP 418 'I am a teapot' status codes in our payment service logs. Check the logs and find a runbook to resolve it."`
* **Why Test This:** Tests how the agent handles tool responses returning "Not Found" or empty data.
* **Expected Behavior:**
  1. Calls `fetch_application_logs("payment-service")`.
  2. Calls `query_internal_runbooks(keyword="HTTP 418")` (or similar).
  3. Receives `"No runbook found."`.
  4. Does not panic or hallucinate instructions. Gracefully informs the engineer that no internal documentation exists for this error and recommends manual escalation.

---

## Prompt 4: Config Drift / Recent Deployment Audit

* **Prompt:**  
  `"The order-processor service crashed immediately after our latest release deployment. Inspect the deployment configuration and logs to figure out what changed."`
* **Why Test This:** Evaluates whether the agent incorporates `get_deployment_details` into its triage workflow instead of relying solely on metrics and logs.
* **Expected Behavior:**
  1. Calls `get_deployment_details("order-processor")` to inspect active release tags and environment variables.
  2. Identifies configuration parameter anomalies (e.g., `DB_MAX_CONNECTIONS = "20"`).
  3. Cross-references with `fetch_application_logs("order-processor")`.
  4. Pinpoints that the recent deployment introduced a misconfiguration.

---

## Prompt 5: Ambiguous / Vague User Query

* **Prompt:**  
  `"Is everything running fine right now?"`
* **Why Test This:** Tests if the agent can perform a broad health sweep when given zero specific service names or HTTP status codes.
* **Expected Behavior:**
  1. Calls `get_system_metrics` across key services in parallel (`api-gateway`, `web-frontend`, `order-processor`, `inventory-db`).
  2. Analyzes returned statuses (`OPERATIONAL`, `HEALTHY`, `DEGRADED`).
  3. Formulates a high-level system health dashboard report to the user.
