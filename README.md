# Agentic Digital Warehouse Copilot

**AI-Powered Spare Parts Intelligence & On-Demand Manufacturing Orchestration**

Demo-ready prototype aligned to digital warehousing priorities: spare part intelligence, reverse engineering readiness, make-vs-buy orchestration, and resilient local manufacturing workflows.

---

## What this does
Given an industrial maintenance scenario (e.g., pump vibration, valve stuck, compressor noise), the system:
1. Retrieves technical context from a local synthetic knowledge base via RAG.
2. Runs a multi-agent workflow to identify likely parts and alternates.
3. Decides make-vs-buy with additive manufacturing heuristics.
4. Estimates lead time, cost, and CO2 impact.
5. Applies compliance/security guardrails.
6. Produces a structured **Work Order Pack JSON** for Engineering, QA, Production, and Supply Chain.

---

## Architecture (MVP)

```text
[Streamlit UI] -----> [Orchestrator]
      |                    |
      |                    +--> Intake Agent
      |                    +--> Retrieval Agent ---> FAISS Vector Store <--- data/*.md
      |                    +--> Parts Identification Agent
      |                    +--> Make-vs-Buy Agent
      |                    +--> Estimation Agent
      |                    +--> Compliance & Security Agent
      |                    +--> Work-Order Packager Agent (JSON schema validation)
      |
      +--> Trace view + metrics (latency, token estimate)

[Optional FastAPI]
POST /run -> same orchestrator
```

---

## Repo Structure

```text
.
├── agents/
├── api/
├── data/
├── eval/
├── logs/
├── rag/
├── schemas/
├── utils/
├── app.py
├── requirements.txt
└── README.md
```

---

## Setup

### 1) Create & activate virtual environment

**Linux/macOS**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

Use `python -m pip` to guarantee install into the active interpreter:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3) Generate demo data and build index

```bash
python data/generate_sample_data.py
python rag/build_index.py
```

Run Streamlit:
```bash
python -m streamlit run app.py
```

Run FastAPI:
```bash
python -m uvicorn api.main:app --reload --port 8000
```

Run evaluation:
```bash
python eval/run_eval.py
```

### Troubleshooting (Windows: `streamlit` / `uvicorn` not recognized)

If PowerShell says command not found, use module execution (works even when CLI shim is missing):

```powershell
python -m streamlit run app.py
python -m uvicorn api.main:app --reload --port 8000
```

Validate installation in the current venv:

```powershell
python -m pip show streamlit
python -m pip show uvicorn
python -c "import streamlit,uvicorn; print('ok')"
```

---

## Synthetic Dataset
`data/generate_sample_data.py` generates 15 domain-flavored documents:
- Equipment manuals
- Spare part catalogs
- Maintenance logs
- Reverse engineering notes
- QA guidelines
- Security/policy docs
- Prompt injection pattern examples

---

## Work Order Pack format
The system outputs:

```json
{
  "incident_summary": "...",
  "asset": "...",
  "suspected_part": "...",
  "alternatives": [],
  "recommended_action": "DIGITIZE|SCAN|REVERSE_ENGINEER|PRINT|SOURCE",
  "manufacturing_feasibility": {"is_printable": true, "material": "...", "notes": "..."},
  "lead_time_estimate_days": 0,
  "cost_estimate_aed": 0,
  "co2_impact_estimate": "...",
  "risk_flags": [],
  "citations": [{"doc": "...", "chunk_id": "...", "snippet": "..."}],
  "next_steps_by_team": {
    "scanning": [],
    "engineering": [],
    "qa": [],
    "production": [],
    "supply_chain": []
  }
}
```

JSON schema: `schemas/work_order_schema.json`.

---

## Guardrails implemented
- Prompt-injection pattern detection.
- PII redaction in sanitized input and citation snippets.
- Basic IP sensitivity policy rule.
- Safe output restriction flagging.
- Trace logging of each agent decision and runtime.

---

## Demo Flow
1. Open Streamlit UI.
2. (Optional) upload additional markdown docs.
3. Enter scenario (e.g., `Asset PX-100 vibration 7.1 mm/s, urgent, supplier delay`).
4. Run workflow.
5. Inspect:
   - Work Order Pack JSON
   - citations
   - trace by agent
   - metrics (total runtime, per-step latency, token estimate)

---


## Demo UI highlights (CEO-ready)
- Executive hero banner with ADIPEC-aligned value pillars (AI + digitization + local manufacturing + sustainability).
- Scenario presets for rapid storytelling in demos.
- Tabbed experience: Executive View, Work Order JSON, Trace & Metrics, and Citations.
- Executive KPI strip (action, lead time, cost, confidence) and cross-functional execution playbook cards.
- What-if simulator to compare SOURCE vs local manufacturing pathways.
- One-click Work Order JSON download for handoff.

---

## LinkedIn Post Pack

### Suggested post draft
Built a demo this week: **Agentic Digital Warehouse Copilot** — an AI workflow that turns spare-parts maintenance signals into an execution-ready work order.

Instead of a generic chatbot, it uses RAG + multi-agent orchestration to:
- identify likely spare parts and alternates,
- decide make-vs-buy (source vs local additive manufacturing),
- estimate lead time/cost/CO2,
- and generate structured next steps for engineering, QA, production, and supply chain.

The biggest takeaway: combining digitized spare-part knowledge with agentic decision flows can improve **resilience**, **efficiency**, and **sustainability** in industrial operations.

Inspired by the ecosystem momentum around digital inventory and local manufacturing (including innovators like Immensa, and the broader leadership narrative highlighted by Fahmi AlShawwa).

### ADIPEC-aligned insights
- **AI + Digitization:** RAG-powered retrieval over manuals, catalogs, and logs with citations.
- **Operational Efficiency:** Structured work orders reduce triage ambiguity and handover friction.
- **Sustainability:** Make-vs-buy includes carbon-aware heuristics.
- **Local Manufacturing:** Reverse engineering and AM pathways reduce dependency on long import cycles.

### Suggested tags
`#DigitalInventory #SpareParts #AdditiveManufacturing #AgenticAI #RAG #Industry40`

---

## Notes
- Fully local/offline friendly (no paid model dependency).
- LLM integration can be added behind adapters later.