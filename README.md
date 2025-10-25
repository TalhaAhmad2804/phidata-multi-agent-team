#  Phidata Multi-Agent Team

A **multi-agent system** built with **Phidata** that demonstrates how intelligent agents can collaborate to perform different types of tasks — combining real-time tool access, contextual reasoning, and conversational memory.

## 🚀 Overview

This project implements two independent agents using **Phidata**:

1. **Stock & Time Agent** — Provides real-time stock price information and retrieves current date/time using tool integrations.  
2. **General Query Agent** — Handles general knowledge or conversational queries and maintains context across interactions.

Both agents are then combined into a **multi-agent team**, enabling them to work together seamlessly — sharing context and coordinating responses based on the type of query.


## ⚙️ Features

- 🧩 **Multi-Agent Collaboration** — Two agents communicate and delegate tasks intelligently.  
- 🕒 **Real-Time Tool Access** — Stock and time retrieval tools integrated via API calls.  
- 💬 **Context Memory** — Maintains previous conversation state for continuity.  
- 📚 **Knowledge Base Integration** — Agents can reference external knowledge for informed responses.  
- 🗂️ **Modular Design** — Easily extendable to add new tools or agents.  
- ⚡ **FastAPI Compatible** — Can be integrated into REST APIs for production deployment.


## 🏗️ Tech Stack

- **Phidata** — For agent and workflow creation  
- **Python** — Core programming language  
- **FastAPI** — For API endpoint creation (optional)  
- **Streamlit** — For building interactive UI (optional demo)  
- **SQLite / PostgreSQL** — For storing embeddings and logs  
- **Neo4j** — For experimenting with graph-based knowledge structures
