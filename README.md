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
2. Decision criteria are automatically classified as:
   - already fulfilled
   - still missing
3. Only missing information is requested in the reply.
4. Product documentation is used as **high-level contextual grounding (RAG)**.
5. A draft response email is generated using a **local LLM**.

The assistant **does not** generate prices or final offers.
Its role is to **support the salesperson**, not replace them.

---

## Architecture (High Level)

- **Signal extraction**  
  LLM-based parsing of customer emails into structured facts

- **Decision criteria classification**  
  AI-assisted evaluation of which qualification inputs are missing

- **RAG (Retrieval-Augmented Generation)**  
  Synthetic product documentation indexed locally and used as contextual background

- **LLM generation**  
  Local inference using Ollama (no cloud dependency)

---

## Repository Structure
data/ – synthetic product documentation (BESS variants)
queries/ – example customer emails
prompts/ – prompt templates (signal extraction, classification, qualification)
scripts/ – core MVP logic and RAG pipeline
config/ – decision criteria definitions (YAML)
docs/ – conceptual documentation


---

## RAG in This MVP

A local RAG pipeline (Chroma + embeddings) is implemented and demonstrated.

In this MVP:
- RAG provides **high-level product context** only
- It does **not** influence the questions asked to the customer
- It can be used to demonstrate how different emails map to different solution variants

This separation is intentional and reflects real sales workflows.

---

## What This MVP Is Not

- Not a pricing engine
- Not an automated offer generator
- Not a replacement for sales engineers
- Not a production-ready system

---

## ▶Running the Demo (Local)

Requirements:
- Python 3.11+
- Poetry
- Ollama (local LLM runtime)

Typical demo flow:
1. Index synthetic product documentation
2. Analyse a customer email
3. Generate a qualification draft response

All processing is done **locally**.

---

## 👤 Author

Joanna Widzińska  
Personal portfolio project  
Focus: AI-assisted sales workflows in energy storage
