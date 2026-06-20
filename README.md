# Agentic Telegram Bot

An autonomous AI agent that lives in Telegram. It understands your messages, searches the web in real-time, monitors your Google Classroom for new assignments, and drafts responses for you automatically.

---

## Features

- **LLM Brain** — Powered by Groq (LLaMA 3.1 8B) for natural language understanding and intent routing
- **Real-Time Web Search** — Searches the web and returns cited sources on demand
- **Google Classroom Watcher** — Monitors active courses every 60 seconds for new assignments
- **Assignment Notifications** — Sends instant Telegram alerts with course, title, type, description, and due date
- **AI Assignment Drafting** — Reply /yes to any notification and the agent drafts a complete response based on the assignment description
- **Persistent Memory** — Remembers seen assignments across restarts, no duplicate notifications

---

## Commands

| Command | Action |
|---------|--------|
| `/start` | Wake the agent |
| `/yes` | Draft a response for the latest assignment |
| `/skip` | Dismiss the latest assignment notification |

---

## Architecture
[Telegram User]

↕

[Telegram Bot API]

↕

[Orchestrator] — LLM decides which tool to use

↕

[Tool Layer]

├── Web Search (DuckDuckGo)

└── Google Classroom Watcher

---

## Tech Stack

- Python 3.x
- python-telegram-bot
- Groq API (LLaMA 3.1 8B Instant)
- Google Classroom API
- DuckDuckGo Search (ddgs)
- google-auth-oauthlib

---

## Setup

### 1. Clone the repo
```bash
git clone <your_repo_url>
cd Agentic_Telegram_Bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure credentials
Create a `config.py` file:
```python
TELEGRAM_TOKEN = "your_telegram_bot_token"
GROQ_API_KEY = "your_groq_api_key"
```

### 4. Google Classroom authentication
Place your `credentials.json` from Google Cloud Console in the project root, then run:
```bash
python authenticate.py
```
Log in with your Google account and accept permissions. This generates `token.pickle`.

### 5. Run the bot
```bash
python main.py
```

---

## Project Structure
Agentic_Telegram_Bot/

├── tools/

│   ├── search.py          — DuckDuckGo web search

│   └── classroom.py       — Google Classroom watcher

├── authenticate.py        — Google OAuth setup

├── bot.py                 — Telegram handlers

├── orchestrator.py        — LLM intent routing

├── main.py                — Entry point

├── config.py              — API keys (not committed)

├── credentials.json       — Google OAuth credentials (not committed)

├── requirements.txt       — Dependencies

└── README.md

---

## Notes

- Classroom is polled every 60 seconds
- The bot must be running to receive notifications
- Assignment drafts are AI-generated — always review before submitting
