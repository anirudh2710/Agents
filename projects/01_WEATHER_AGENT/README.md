# 🌤️ Weather Agent

A conversational AI agent that fetches real-time weather data for any city using the [Open-Meteo API](https://open-meteo.com/) — no API key required for weather data.

Built with **LangChain**, **LangGraph**, and **Groq (Llama 3.3 70B)**.

---

## How It Works

```
User: "What's the weather in Berlin?"
  └─► Agent calls get_weather tool
        └─► Geocoding API: "Berlin" → (52.52°N, 13.42°E)
        └─► Open-Meteo API: coordinates → temperature, wind, humidity
  └─► Agent summarises and responds in natural language
```

The agent runs as a **LangGraph tool-calling loop** — it calls tools until it has enough information to answer, then returns a final response.

---

## Stack

| Component | Library |
|-----------|---------|
| LLM | `langchain-groq` · `llama-3.3-70b-versatile` |
| Agent framework | `langchain` · `create_agent` |
| Graph runtime | `langgraph` |
| Weather data | [Open-Meteo Forecast API](https://open-meteo.com/) (free, no key) |
| Geocoding | [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/) (free, no key) |

---

## Project Structure

```
01_WEATHER_AGENT/
├── app.ipynb   # Main notebook — agent definition and invocation
└── README.md
```

---

## Setup

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/anirudh2710/Agents.git
cd Agents
uv sync          # or: pip install -r requirements.txt
```

### 2. Create a `.env` file in the project root

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the notebook

Open `projects/01_WEATHER_AGENT/app.ipynb` in Jupyter and run all cells top to bottom.

> **Kernel**: Make sure the notebook kernel is set to `.venv` (the project virtual environment).

---

You can ask about any city in the world:
- `"What's the weather in Tokyo?"`
- `"How hot is it in Dubai right now?"`
- `"Current weather in New York?"`

---

## Notes

- A **fresh `thread_id`** is generated per run via `uuid.uuid4()` to prevent `MemorySaver` from accumulating tool responses across runs (which would exceed the Groq free-tier token limit).
- The weather API call uses `forecast_days=1` to return only today's 24-hour forecast instead of the default 7-day dump, keeping the tool response small.
