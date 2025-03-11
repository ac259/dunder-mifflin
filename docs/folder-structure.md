## Folder Structure
This is a potential structure.

```
dunder-mifflin/
│── agents/                   # Individual AI agents (each mapped to an Office character)
│   │── schrute_bot/          # Dwight Schrute's Productivity Enforcer
│   │   │── __init__.py
│   │   │── schrute_bot.py    # Core logic for task tracking & nudging
│   │   │── prompts.py        # Dwight-like messages & responses
│   │   │── tests/            # Unit tests for SchruteBot
│   │── michael_bot/          # Michael Scott (Supervisor AI)
│   │── kevin_bot/            # Kevin’s Budgeting AI
│   │── pam_bot/              # Pam’s Email Assistant
│
│── core/                     # Central system logic
│   │── __init__.py
|   |__ mistral_agent.py      # Mistral LLM handling (shared across agents)
│   │── manager.py            # Multi-agent manager (Michael delegates tasks)
│   │── utils.py              # Shared utility functions
│
│── database/                    # Database & migrations
│   │── schema.sql                # SQL schema for setup
│   │── migrations/               # Future database upgrades
│   │── schrutebot.db             # SQLite database file
|
│── integrations/             # APIs & external service integrations
│   │── google_calendar.py    # Google Calendar API integration
│   │── notion_api.py         # Notion API integration
│   │── website_blocker.py    # Productivity enforcement via blocking distractions
│
│── configs/                  # Config & environment variables
│   │── settings.py           # Main config file
│   │── .env                  # API keys & secrets (not committed)
│
│── tests/                    # General test cases
│
│── docs/                     # Documentation
│   │── README.md             # Project overview
│   │── AGENTS.md             # Details on each agent’s role & logic
│
│── main.py                   # Entry point to run the AI system
│── requirements.txt          # Python dependencies
│── .gitignore                # Ignoring unnecessary files (logs, env files, etc.)
│── LICENSE                   # Open-source license (if applicable)
```
