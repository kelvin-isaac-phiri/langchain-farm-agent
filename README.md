# LangChain Farm Agent (AgriGuide)

A simple starter project for learning **LangChain** and **agentic AI**.

You ask a farm question. The agent decides which **tools** to call (database, crop info, weather, or web search), then answers.

This is one of the easiest ways to start: few files, free Gemini key, and you can see every tool call in the terminal.

> Demo only — sample data, not real farm advice.

## What you will learn

- What an **agent** is (model + tools + loop)
- How tools work (`@tool`)
- How an agent reads from a **SQLite** database
- How an agent can **search the web**
- The difference between hardcoded data, DB tools, and live search

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Put your free Gemini key in `.env`:

```env
GOOGLE_API_KEY=your_api_key_here
```

Get a key: [Google AI Studio](https://aistudio.google.com/apikey)

Run:

```bash
python agent.py
```

## Try this

1. Farm ID: `F002`
2. Question:

```text
My tomato leaves are turning yellow. Check my farm, weather, and search the web. What should I check first?
```

You should see tools run, then an answer.

Other farm IDs: `F001` (maize), `F002` (tomato). Type `quit` to exit.

## Project files

```text
agent.py          # runs the agent
tools.py          # tools the agent can call
db.py             # SQLite connection (agent_db)
data.py           # seed / crop sample data
requirements.txt
.env.example
```

## Tools

| Tool | What it does |
|------|----------------|
| `get_farm_info` | Reads a farm from SQLite (`agent_db`) |
| `get_crop_information` | Local crop problem tips |
| `check_farm_weather` | Simple weather from farm location |
| `search_web` | Live web search (DuckDuckGo) |

## Stack

Python · LangChain · LangGraph · Google Gemini · SQLite · DuckDuckGo

## Built with Algin System

If you want a ready **RAG platform** (upload docs → ask questions over your data), try:

**https://rag.alignsystemsltd.com**

## License note

Educational prototype. Use it to learn and experiment.
