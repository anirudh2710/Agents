# 🛒 Conversational RAG Support Agent (Hybrid Search & Memory)

An enterprise-grade Customer Support & Returns Agent that parses unstructured company documentation using **Hybrid Search** (BM25 + ChromaDB + Reciprocal Rank Fusion), enforces strict inline source citations, and maintains stateful conversational memory across multiple turns.

Built with **LangChain**, **LangGraph**, **ChromaDB**, **rank_bm25**, and **Groq (Llama 3.3 70B)**.

---

## 🏗️ Architecture

```
 ┌──────────────────────────────────────────────────────────┐
 │                       USER QUERY                         │
 │     ("Can I return my open-box headphones after 20 days?") │
 └────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
 ┌──────────────────────────────────────────────────────────┐
 │                 HYBRID RETRIEVAL LAYER                   │
 │   - BM25 Sparse Search (Catches "headphones", "20")      │
 │   - ChromaDB Dense Vector Search (Catches semantic intent)│
 │   - Reciprocal Rank Fusion (RRF) Re-ranker               │
 └────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
 ┌──────────────────────────────────────────────────────────┐
 │                   AGENT STATE & MEMORY                   │
 │   - Formatted Context + System Citation Instructions     │
 │   - Thread Memory Checkpointer (MemorySaver / thread_id) │
 └────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
 ┌──────────────────────────────────────────────────────────┐
 │                    GROUNDED RESPONSE                     │
 │   ("Yes, open-box electronics have a 30-day window...    │
 │    [Source: return_policy.md]")                          │
 └──────────────────────────────────────────────────────────┘
```

---

## 📁 Enterprise Knowledge Base Data Layer (`/data`)

- `return_policy.md`: Return windows (30 days electronics, 60 days clothing), open-box conditions, 15% restocking fees.
- `shipping_and_support.md`: Flat domestic/international shipping rates, order cancellation rules (1-hour window), lost package claims.
- `warranty_rules.md`: 1-Year Limited Manufacturer Warranty terms, exclusions, and RMA replacement procedures.

---

## ⚡ Key Features

1. **Hybrid Retrieval (BM25 + Vector Search)**: Combines keyword precision for exact numbers/SKUs (`"30-day"`, `"20"`) with dense semantic vector search (`ChromaDB`).
2. **Reciprocal Rank Fusion (RRF)**: Re-ranks candidates using the formula $RRF = \sum \frac{1}{k + r_i}$ with $k=60$.
3. **Strict Citation Enforcement**: Grounded responses require explicit inline citations `[Source: return_policy.md]`.
4. **Stateful Conversational Memory**: Thread state (`MemorySaver`) maintains context across follow-up queries without re-specifying entity details.
5. **Guardrails & Refusal**: Politely declines out-of-bounds queries or questions lacking policy context.

---

## 💻 Setup & Running

1. Install dependencies: `uv sync`
2. Add `.env` in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```
3. Open `app.ipynb` in `projects/03_RAG_HYBRID_SEARCH/` and run all cells top-to-bottom using the `.venv` kernel.

---