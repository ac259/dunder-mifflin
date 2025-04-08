# 🧠 SchruteBot 2.0: “Schruteboard” Planning Document

## 🧩 Overview

We’re evolving SchruteBot from a simple task assistant into a **strategic project planner** with a Kanban-like interaction model, in true Dwight fashion. The bot will continue speaking in-character, but provide real functionality — task creation, lane management, filtering, and movement across swimlanes.

---

## ✅ Core Features

| Feature               | Description |
|-----------------------|-------------|
| `add_task`            | Create a new task with optional `priority` and `lane` |
| `view_board`          | Display tasks organized by swimlanes |
| `move_task`           | Move a task between lanes |
| `complete_task`       | Mark a task complete (auto-move to `Done`) |
| `filter_tasks`        | Filter by lane, priority, or status |
| `daily_report`        | Show task stats + Dwight’s commentary |
| `dwightism`           | Show random Dwight wisdom |

---

## 🗃 Database Schema Additions

### Updated `tasks` table:

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    lane TEXT DEFAULT 'backlog',
    priority TEXT DEFAULT 'medium',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    hash TEXT UNIQUE
);
```

- **lane**: one of `backlog`, `in_progress`, `review`, `done`, `blocked`

---

## 🧠 Commands & Agent Inputs

```plaintext
| Prompt Format                             | Intent                  |
|-------------------------------------------|--------------------------|
| `add task Build frontend lane:in_progress`| Add task to a specific lane |
| `view board`                               | Show all tasks in swimlanes |
| `move task Build API to review`           | Move task between lanes |
| `filter by lane review`                   | List tasks only in `review` |
| `complete task Finalize report`           | Mark task done, update lane |
| `daily report`                             | Show productivity stats |
| `dwightism`                                | Give random quote |
```

---

## 🧱 Lane Definitions

```python
LANES = ["backlog", "in_progress", "review", "done", "blocked"]
```

---

## 🖼 Wireframe (Textual-style layout)

```plaintext
┌────────────────────────────── DunderBoard ─────────────────────────────┐
│ Dwight says: “You couldn’t handle my job.”                             │
│                                                                        │
│ BACKLOG           IN_PROGRESS         REVIEW           DONE            │
│ 🔹 Task A          🔸 Task B            🛠 Task C         ✅ Task D       │
│ 🔹 Task E          🔸 Task F            🛠 Task G         ✅ Task H       │
│                                                                        │
│ > add task Call Jan about finances lane:backlog priority:high         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📐 Architecture Plan

### 🧩 Modular Methods:

- `add_task(description, lane, priority)`
- `move_task(description, target_lane)`
- `view_board()`
- `filter_tasks(lane, priority, status)`
- `lane_summary(lane)` → Optional

### 👨‍💼 Agent Responsibilities

All interactions continue to go through `process_request()` like:

```python
if message.startswith("move task"):
    ...
elif message.startswith("view board"):
    ...
```

Dwight will still chime in after every action with custom feedback.

---

## 🚀 Stretch Goals

- [ ] Markdown output for checklists
- [ ] Subtasks or task IDs
- [ ] Due dates & reminders
- [ ] Assignments (maybe integrate with Jimster for chaos 🤡)

---