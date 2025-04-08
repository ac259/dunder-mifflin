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


## 🧱 Wireframe Layout Plan

We’ll build a **multi-pane app** in Textual, where you can:

- Navigate agents
- Interact with each agent’s task UI
- Send messages or commands
- View logs and responses

---

### 🔳 **Primary Layout Wireframe**

```
╔════════════════════════════════════════════════════════════════════════╗
║ 🧠  DUNDER TERMINAL HQ — Powered by PamBot                             ║
╠════════════════════╦═══════════════════════════════════════════════════╣
║ 👥 AGENTS           ║ 📋 TASKS / RESPONSES                               ║
║────────────────────║──────────────────────────────────────────────────║
║ 🔹 SchruteBot       ║ 🔹 Defeat the printer (MEDIUM)                    ║
║ 🔹 JimsterAgent     ║ 🔹 Hide SchruteBot’s beets (LOW)                 ║
║ 🔹 PamBot (Router)  ║ 🔹 Fix Pam's email (HIGH)                         ║
║                    ║                                                  ║
║ [SPACE] Select     ║ *Dwight’s quote loads...*                         ║
╠════════════════════╩═══════════════════════════════════════════════════╣
║ 💬 Command: /add "disable CreedBot" priority=high                      ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

### 🎮 Planned Interaction Flow

```plaintext
| Action | Input | Result |
|--------|-------|--------|
| Add Task | `/add "task desc" priority=high` | Goes to SchruteBot |
| Toggle Prank Mode | `/toggle_pranks` | JimsterAgent toggles mode |
| View Agents | Arrow keys or click | Updates main panel |
| Freeform Prompt | `/ask [agent] What's our mission?` | Routed via PamBot |
| Dynamic Feedback | All agents respond in real-time | Updates console |
```

---

### 📁 File Structure Proposal (Textual Version)

```bash
cli/
├── textual_ui.py     # 🚀 Entry point for Textual app
├── widgets/
│   ├── agent_list.py # Left pane: Selectable agent list
│   ├── task_panel.py # Main panel: task lists or messages
│   └── command_box.py# Input at bottom for commands
├── app.py            # Sets up layout, events, agent hooks
```

---

### 🧩 Components Breakdown

```plaintext
| Widget | Description |
|--------|-------------|
| `AgentList` | List of all registered agents (toggle/select) |
| `TaskPanel` | Displays agent-specific content (tasks, messages, responses) |
| `CommandBox` | Input box for user commands — routed via `PamBot` |
| `AppLayout` | Orchestrates it all and handles routing events to agents |
```

---