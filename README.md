# HR-Agent

AI-powered HR Assistant built using FastAPI, React, LangChain, OpenAI, SQLite, and ChromaDB.

## Overview

HR-Agent is a full-stack HR assistant that enables employees and HR teams to interact with HR data and policies using natural language.

The system combines:

* Retrieval-Augmented Generation (RAG)
* SQL query generation
* Conversational memory
* Multi-route AI orchestration

The assistant can answer:

* HR policy questions
* Employee information queries
* Leave-related questions
* Timesheet queries
* Ticket status queries

This project was developed as an internship AI engineering project based on the provided HR AI Agent requirements document.

---

# Features

## RAG Pipeline

* HR policy document ingestion
* Semantic search using embeddings
* ChromaDB vector store
* Context-aware response generation

## SQL Pipeline

* Natural language to SQL generation
* SQLite database querying
* Conversational query rewriting
* Natural response formatting

## Intelligent Query Routing

The system automatically classifies queries into:

* RAG
* SQL
* GENERAL conversation

## Conversational Memory

Supports follow-up questions such as:

* "What is her email?"
* "Who among them are full time employees?"

## Full Stack Architecture

* React frontend
* FastAPI backend
* LangChain orchestration
* OpenAI GPT models

---

# Tech Stack

| Layer               | Technology                  |
| ------------------- | --------------------------- |
| Frontend            | React + Tailwind CSS        |
| Backend             | FastAPI                     |
| LLM Framework       | LangChain                   |
| Language Models     | OpenAI GPT-4o / GPT-4o-mini |
| Vector Database     | ChromaDB                    |
| Structured Database | SQLite                      |
| Embeddings          | text-embedding-3-small      |
| Document Parsing    | Docx2txt                    |
| Deployment Ready    | Yes                         |

---

# System Architecture

```text
React Frontend
        ↓
FastAPI Backend
        ↓
HR Assistant Orchestrator
   ↙               ↘
RAG Pipeline      SQL Pipeline
   ↓                   ↓
ChromaDB          SQLite
```

---

# Project Structure

```text
HR-AI-Agent/
│
├── app/
│   ├── api.py
│   ├── hr_assistant.py
│   ├── router.py
│   ├── retrieval_pipeline.py
│   ├── test_sql.py
│   └── ingestion_pipeline.py
│
├── frontend/
│
├── docs/
│
├── data/
│
├── db/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/your-username/peopledesk-ai.git
```

---

## 2. Backend Setup

Create virtual environment:

```bash
python3 -m venv venv
```

Activate environment:

### Linux / Mac

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create `.env`

```env
OPENAI_API_KEY=your_api_key
```

---

## 4. Run Backend

```bash
uvicorn app.api:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

Swagger API Docs:

```text
http://127.0.0.1:8000/docs
```

---

## 5. Frontend Setup

Move into frontend directory:

```bash
cd frontend
```

Install packages:

```bash
npm install
```

Run frontend:

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# Example Queries

## RAG Queries

* What is the leave policy?
* What are manager responsibilities during employee leave?
* Explain the work from home policy.

## SQL Queries

* Who is the manager of Priya Mehta?
* Show all employees in Bangalore.
* Who among them are full time employees?
* What is the status of ticket TKT-0042?
* Did John submit his timesheet last week?

---

# Key Concepts Implemented

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Conversational Query Rewriting
* Natural Language to SQL
* AI Query Routing
* Stateless Backend Architecture
* Frontend-managed Chat Memory
* Multi-turn Conversations

---

# Future Improvements

* Authentication & user sessions
* Persistent chat history
* Streaming responses
* SQL result tables in UI
* Role-based access control
* Deployment on AWS/Azure
* Docker support
* Analytics dashboard

---
