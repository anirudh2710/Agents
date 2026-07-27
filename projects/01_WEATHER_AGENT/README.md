# 🌤️ Weather Agent (Model Context Protocol / MCP)

A conversational AI agent that fetches real-time weather data for any city using an **MCP (Model Context Protocol) Weather Server** connected to the [Open-Meteo API](https://open-meteo.com/).

Built with **LangChain**, **LangGraph**, **FastMCP**, **`langchain-mcp-adapters`**, and **Groq (Llama 3.3 70B)**.

---

## How It Works

```
                        stdio / JSON-RPC
┌──────────────────────────┐  Tool Discovery   ┌──────────────────────────┐
│     LangChain Agent      │ ◄───────────────► │    Weather MCP Server    │
│ (MCP Client via Adapters)│   & Execution     │ (weather_server.py)      │
└────────────┬─────────────┘                   └────────────┬─────────────┘
             │                                              │
             ▼                                              ▼
     User Question                                   Open-Meteo API
```

1. **`weather_server.py`**: A standalone MCP Server built with `FastMCP` exposing `get_weather(city)`.
2. **`app.ipynb`**: The LangChain agent connects asynchronously via `MultiServerMCPClient` over `stdio`, retrieves tool definitions, and executes queries asynchronously via `await agent.ainvoke(...)`.

---

## Stack

| Component | Library / API |
|-----------|---------------|
| LLM | `langchain-groq` · `llama-3.3-70b-versatile` |
| Agent Framework | `langchain` · `create_agent` |
| MCP Server | `mcp.server.fastmcp` · `FastMCP` |
| MCP Client | `langchain-mcp-adapters` · `MultiServerMCPClient` |
| Graph Runtime | `langgraph` · `MemorySaver` |
| Weather Data | [Open-Meteo Forecast API](https://open-meteo.com/) (free, no key) |

---

## Project Structure

```
01_WEATHER_AGENT/
├── weather_server.py   # Standalone MCP Weather Server (FastMCP)
├── app.ipynb           # Main notebook — MCP Client & Agent invocation
└── README.md           # Documentation
```

---

## 💻 Setup & Running

### 1. Install dependencies

```bash
uv sync          # or: pip install -r requirements.txt
```

### 2. Create a `.env` file in the project root

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the notebook

Open `projects/01_WEATHER_AGENT/app.ipynb` in Jupyter and run all cells top to bottom using the `.venv` kernel.

---

## 💡 Key Technical Details

- **Async Invocation (`agent.ainvoke`)**: Since MCP clients communicate asynchronously over `stdio`/JSON-RPC, calling `await agent.ainvoke(inputs, config=config)` is required so LangGraph executes `ToolNode._execute_tool_async()` instead of throwing `StructuredTool does not support sync invocation`.
- **Interpreter Path (`sys.executable`)**: The client passes `sys.executable` as the server command to ensure the child MCP process uses the active virtual environment.
