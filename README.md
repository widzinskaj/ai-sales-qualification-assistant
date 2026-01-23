# AI Sales Qualification Assistant for Energy Storage

This repository contains a **portfolio-grade MVP** of an AI-powered assistant
designed to support the **first response and qualification stage** of the sales process
for **energy storage systems (BESS)**.

The project focuses on automating the preparation of a **first reply to a customer inquiry**:
understanding the message, identifying what information is already known,
and generating a clear, professional response asking only for missing details.

> Disclaimer
> This is a **personal portfolio project**.
> It uses **only synthetic or public data** and does **not** contain any confidential,
> proprietary, or internal information from any company.

---

## Problem

Sales engineers and technical sales teams often receive customer inquiries
that are **incomplete, non-technical, or ambiguous**.

Typical challenges:
- Customers describe needs in natural language, not technical parameters
- Important details (capacity, power, constraints) are missing
- First responses take time and are repetitive
- Sales teams risk asking redundant or irrelevant questions

---

## Solution (MVP Scope)

This MVP demonstrates a realistic **AI-assisted sales qualification workflow**:

1. A customer email is analysed to extract structured signals (facts).
2. Decision criteria are evaluated to determine which inputs are
   already known and which are still missing.
3. Only missing information is requested in the reply.
4. Product documentation is used as **high-level contextual grounding (RAG)**.
5. A draft response email is generated using a **local LLM**.

The assistant **does not** generate prices or final offers.
Its role is to **support the salesperson**, not replace them.

---

## Features & Capabilities

**Signal Extraction**
- LLM-based parsing of customer emails into structured JSON facts
- Extracts explicitly stated information such as capacity references, power hints, location constraints, and stated use cases
- Configurable extraction prompts

**RAG Pipeline**
- ChromaDB vector database for product documentation
- Sentence-transformers embeddings (all-MiniLM-L6-v2)
- Human-readable context generation from ranked documents
- Synthetic BESS product variants and accessories database

**Qualification Logic**
- YAML-based decision criteria configuration
- Multi-stage prompt construction with known facts and RAG context
- LLM-assisted identification of missing qualification inputs

**Local LLM Inference**
- Ollama runtime integration (no cloud dependency)
- Configurable model selection (default: qwen2.5:1.5b)
- Subprocess-based stable execution on Windows

**Demo & Testing**
- 3 example customer emails with varying complexity
- Sample outputs demonstrating end-to-end workflow
- Configurable via environment variables

---

## Architecture (High Level)

- **Signal extraction**
  LLM-based parsing of customer emails into structured facts

- **Decision criteria evaluation**
  AI-assisted evaluation of which qualification inputs are missing

- **RAG (Retrieval-Augmented Generation)**
  Synthetic product documentation indexed locally and used as contextual background

- **LLM generation**
  Local inference using Ollama (no cloud dependency)

---

## Technology Stack

**Core Dependencies**
- Python 3.11+
- Poetry (dependency management)
- Ollama (local LLM runtime)

**Key Libraries**
- `chromadb` – vector database for RAG
- `sentence-transformers` – embedding generation
- `PyYAML` – decision criteria configuration

---

## Repository Structure

```
data/                           – synthetic product documentation (BESS variants)
├── bess_small_modular/         – modular BESS system specs
└── accessories/                – wireless communication and monitoring accessories

queries/                        – example customer emails
├── client_email_01.txt         – basic capacity inquiry
├── client_email_02.txt         – multi-site deployment request
└── client_email_03.txt         – accessory/add-on request

prompts/                        – prompt templates
├── extract_signals_prompt.md   – signal extraction instructions
└── qualification_prompt.md     – main qualification prompt template

scripts/                        – core MVP logic and RAG pipeline
├── run_qualification.py        – main end-to-end qualification workflow
├── extract_signals.py          – LLM-based signal extraction
├── rag_index.py                – index product documentation into ChromaDB
├── rag_search.py               – retrieve relevant context from RAG
└── rag_query.py                – interactive RAG query tool

config/                         – decision criteria definitions (YAML)
└── decision_criteria_bess.yaml – qualification requirements for BESS sales

demo_output/                    – example generated outputs
└── mail01_*.md                 – sample qualification responses

docs/                           – conceptual documentation
tests/                          – test suite (pytest)
chroma_db/                      – local vector database (gitignored)
```

---

## RAG in This MVP

A local RAG pipeline (Chroma + embeddings) is implemented and demonstrated.

In this MVP:
- RAG provides **high-level product context** only
- It does **not** influence the questions asked to the customer
- It can be used to demonstrate how different emails map to different solution variants

This separation is intentional and reflects real sales workflows.

This design choice intentionally separates qualification logic from product selection,
reflecting how real sales engineers operate in early-stage conversations.

---

## What This MVP Is Not

- Not a pricing engine
- Not an automated offer generator
- Not a replacement for sales engineers
- Not a production-ready system

---

## ▶ Running the Demo (Local)

### Prerequisites
- Python 3.11+
- Poetry
- Ollama (local LLM runtime)

### Setup
```bash
git clone https://github.com/yourusername/ai-offer-assistant.git
cd ai-offer-assistant
poetry install
```

Pull a local model:
```bash
ollama pull qwen2.5:3b
```

### Demo Workflow

Index product documentation (RAG):
```bash
python scripts/rag_index.py
```

Run end-to-end qualification:
```bash
python scripts/run_qualification.py
```

Try different inputs:
```bash
export QUAL_EMAIL_FILE=client_email_02.txt
export OLLAMA_MODEL=qwen2.5:3b
python scripts/run_qualification.py
```

---

## Example Output

The outputs are intended as decision support for a human salesperson,
not as fully automated customer communication.

Sample outputs are available in [`demo_output/`](demo_output/):
- Signal extraction results (structured JSON)
- RAG context retrieval (ranked documents)
- Final qualification email drafts

These demonstrate the system's ability to:
- Parse ambiguous customer requests
- Identify missing technical parameters
- Generate professional, context-aware responses

---

## 👤 Author

Joanna Widzińska
Personal portfolio project
Focus: AI-assisted sales workflows in energy storage
