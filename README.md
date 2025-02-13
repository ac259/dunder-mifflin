# dunder-mifflin

Inspired by The Office, Dunder Mifflin AI is an agentic system designed to bring a mix of humor and efficiency to your everyday tasks. 
Whether it’s scheduling meetings (without double-booking like Michael Scott), managing emails (unlike Kevin’s famous chili disaster), or even delivering sarcastic but useful productivity insights à la Jim Halpert,
this AI assistant is here to help.

With a playful nod to Scranton’s most beloved paper company, this system doesn’t just get things done—it does them with the kind of quirky personality that makes work fun. 
Think of it as an AI Dwight Schrute: hyper-efficient, knowledgeable, and occasionally over-the-top, but ultimately making your life easier.

## Ideas
This concept has huge potential, especially if you lean into the humor and make it feel like an actual “Dunder Mifflin” AI assistant. You could add themed responses, custom voices, and even character-based modes (e.g., a "Stanley Mode" that only gives minimal effort, or a "Michael Mode" that offers bad but enthusiastic advice).

You could also integrate GPT-based conversational elements that mimic different Office characters reacting to your tasks, turning routine work into entertainment.

### Fun AI Agents You Could Build
Here are some hilarious and useful AI agents that fit the Office theme:

The "Michael Scott" Motivational AI 🏆

An AI that gives you wildly inappropriate yet strangely inspiring pep talks before meetings.
Example: "You miss 100% of the shots you don’t take – Wayne Gretzky – Michael Scott."
Dwight Schrute Productivity Enforcer 💼

Tracks your work habits and aggressively reminds you to stay productive.
Can respond to inactivity with lines like: "You are slacking. In the wild, you would be eliminated."
Pam's Passive-Aggressive Email Assistant 📧

Helps you draft perfectly passive-aggressive emails that maintain professionalism.
Example: "Per my last email, I’m just following up… again."
Kevin’s Budgeting Bot 💰

Helps manage finances but occasionally suggests terrible ideas, like investing in chili.
Stanley’s Work-Life Balance Monitor 😴

Detects overwork and shuts down your system at 5 PM sharp.
Jim’s Prank Bot 🎭

Subtly alters small details in your workflow for harmless pranks (e.g., randomly changing one file name per week).
Creed’s Mysterious Business Advisor 🕵️‍♂️

Generates vague, possibly illegal but intriguing business ideas.


## Folder Structure
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