import time
import random
import sqlite3
import hashlib
import sys
import os
# Add project root to sys.path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from multi_agent_orchestrator.agents import Agent, AgentOptions, AgentCallbacks
from multi_agent_orchestrator.types import ConversationMessage
from typing import List, Optional, Dict
from common.gemma_agent import GemmaAgent
from agents.jimster.big_tuna import JimsterAgent

DB_FILE = "schrutebot.db"

class SchruteBot(Agent):
    def __init__(self):
        options = AgentOptions(
            name="SchruteBot",
            description="Assistant for managing tasks with a Dwight Schrute persona.",
            save_chat=True,
            callbacks=AgentCallbacks(),
            LOG_AGENT_DEBUG_TRACE=False
        )
        super().__init__(options)
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.idle_time = 0
        self.cached_quotes = self.load_dwight_quotes()
        self.jimster = JimsterAgent()
        self.gemma = GemmaAgent()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                lane TEXT DEFAULT 'backlog',
                priority TEXT DEFAULT 'medium',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                hash TEXT UNIQUE
            )
        ''')
        self.conn.commit()

        # Migration: add 'lane' column if it doesn't exist (for older installs)
        try:
            self.cursor.execute("ALTER TABLE tasks ADD COLUMN lane TEXT DEFAULT 'backlog'")
        except sqlite3.OperationalError:
            pass  # Column already exists

    def generate_hash(self, task):
        return hashlib.sha256(task.encode()).hexdigest()

    def load_dwight_quotes(self):
        try:
            self.cursor.execute("SELECT line_text FROM dwight_quotes")
            quotes = [row[0] for row in self.cursor.fetchall()]
            return quotes if quotes else ["You have failed to populate quotes. Typical."]
        except sqlite3.OperationalError:
            return ["You have failed to set up the database correctly. Shame."]

    def generate_dynamic_response(self, prompt_type, context=""):
        quote_context = "\n".join(random.sample(self.cached_quotes, min(len(self.cached_quotes), 5)))
        prompt = f"Act as Dwight Schrute from The Office.\n\nScenario: {context}\n\nUse these quotes:\n{quote_context}\n\nRespond as Dwight."
        return self.mistral.generate_response(prompt)

    async def process_request(
        self,
        input_text: str,
        user_id: str,
        session_id: str,
        chat_history: List[ConversationMessage],
        additional_params: Optional[Dict[str, str]] = None
    ) -> str:
        message = input_text.lower().strip()

        if message.startswith("add task"):
            desc = message.replace("add task", "").strip()
            return self.add_task(desc)

        if message.startswith("complete task"):
            desc = message.replace("complete task", "").strip()
            return self.complete_task(desc)

        if message == "view tasks":
            return self.view_tasks()

        if message == "daily report":
            return self.daily_report()

        if message.startswith("move task"):
            parts = message.replace("move task", "").strip().split(" to ", 1)
            if len(parts) == 2:
                task, new_lane = parts[0].strip(), parts[1].strip()
                return self.move_task(task, new_lane)

        if message == "view board":
            return self.view_board()

        if message == "dwightism":
            return self.dwightism()

        if message.startswith("prank toggle"):
            self.jimster.toggle_prank_mode()
            return "🎭 Prank mode toggled."

        return "❌ Command not recognized."

    def add_task(self, task, priority="medium"):
        task = self.jimster.prank_task(task)
        task_hash = self.generate_hash(task)
        self.cursor.execute("INSERT INTO tasks (description, priority, hash) VALUES (?, ?, ?)", (task, priority, task_hash))
        self.conn.commit()

        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        task_count = self.cursor.fetchone()[0]

        context = (
            "Oh boy, here he goes again... overcommitting." if task_count > 10 else
            "Finally, a task. I was starting to think you were as lazy as Jim." if task_count == 1 else
            "Good. Efficiency is key. Unlike Kevin’s work ethic."
        )
        commentary = self.generate_dynamic_response("add_task", context)
        return f"✅ Task added: {task}\n\n💬 *{commentary}*"

    def complete_task(self, task):
        task_hash = self.generate_hash(task)
        self.cursor.execute("UPDATE tasks SET status = 'completed' WHERE hash = ?", (task_hash,))
        self.conn.commit()

        if self.cursor.rowcount:
            context = "Impressive. But is it truly complete, or like Stanley's sales calls?"
            commentary = self.generate_dynamic_response("complete_task", context)
            return f"✅ Task completed: {task}\n\n💬 *{commentary}*"
        else:
            context = "Either you never added it, or you're lying. I never tolerate liars."
            commentary = self.generate_dynamic_response("task_missing", context)
            return f"❌ Task not found: {task}\n\n💬 *{commentary}*"

    def view_tasks(self):
        self.cursor.execute("""
            SELECT description, status, priority 
            FROM tasks 
            ORDER BY CASE priority 
                WHEN 'high' THEN 1 
                WHEN 'medium' THEN 2 
                ELSE 3 END
        """)
        tasks = self.cursor.fetchall()
        if not tasks:
            return "📋 **Task List**\n\nNo tasks found. Productivity is the backbone of civilization!"

        tasks = self.jimster.prank_task_list(tasks)
        lines = ["📋 **Task List**"]
        for desc, status, priority in tasks:
            icon = {"high": "🔥", "medium": "📌", "low": "🧊"}.get(priority.lower(), "➖")
            lines.append(f"{icon} {desc.strip().capitalize()} - {status.upper()} ({priority.upper()})")

        commentary = self.generate_dynamic_response("view_tasks", "Report these findings to corporate.")
        return "\n".join(lines) + f"\n\n💬 *{commentary}*"

    def daily_report(self):
        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
        completed = self.cursor.fetchone()[0]
        context = f"Today, {completed} tasks were completed. {'Acceptable.' if completed > 5 else 'Disappointing.'}"
        commentary = self.generate_dynamic_response("daily_report", context)
        return f"📊 **Daily Report**\nTasks completed: {completed}\n\n💬 *{commentary}*"

    def move_task(self, task, new_lane):
        task_hash = self.generate_hash(task)
        self.cursor.execute("UPDATE tasks SET lane = ? WHERE hash = ?", (new_lane, task_hash))
        self.conn.commit()

        if self.cursor.rowcount:
            context = f"Task '{task}' moved to {new_lane.upper()} lane."
            commentary = self.generate_dynamic_response("move_task", context)
            return f"Task moved: {task} → {new_lane.upper()} 💬 *{commentary}*"
        else:
            context = f"Attempted to move a task that doesn't exist: '{task}'"
            commentary = self.generate_dynamic_response("task_missing", context)
            return f"❌ Task not found: {task} 💬 *{commentary}*"

    def view_board(self):
        self.cursor.execute("""
            SELECT lane, description, status, priority
            FROM tasks
            ORDER BY lane, priority DESC, timestamp ASC
        """)
        tasks = self.cursor.fetchall()

        if not tasks:
            return "📋 Your board is clean. Dwight is... suspicious."

        board = {}
        for lane, desc, status, priority in tasks:
            entry = f"• {desc.strip().capitalize()} ({status.upper()}, {priority.upper()})"
            board.setdefault(lane.upper(), []).append(entry)

        output = ["🗂️ **Project Board**"]
        for lane in sorted(board):
            output.append(f"\n📦 **{lane}**")
            output.extend(board[lane])

        commentary = self.generate_dynamic_response("view_board", "Display current swimlanes.")
        return "\n".join(output) + f"\n\n💬 *{commentary}*"


    def dwightism(self):
        commentary = self.generate_dynamic_response("dwightism")
        return f"💬 *{commentary}*"
