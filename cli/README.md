# CLI

✅ CLI → AgentConnector → Pam → Agents (via Orchestrator)
So your flow becomes:

```plaintext
User input in CLI
    ↓
AgentConnector (calls PamBot)
    ↓
PamBot (classifies + routes)
    ↓
Orchestrator → Schrute, Jimster, Darryl
```

