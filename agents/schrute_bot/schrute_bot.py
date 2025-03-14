import time
import random
import argparse
import sqlite3
import hashlib
import sys
import os
from datetime import datetime
from multi_agent_orchestrator.agents import Agent, AgentOptions, AgentCallbacks
from multi_agent_orchestrator.types import ConversationMessage
from typing import List, Optional, Dict

# Add project root to sys.path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from common.mistral_agent import MistralAgent
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
        self.nudges = self.load_dwight_quotes()
        self.keywords = ["task", "assign", "track", "complete", "project", "work"]
        self.mistral = MistralAgent()
        self.cached_quotes = self.load_dwight_quotes()
        self.jimster = JimsterAgent()
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                hash TEXT UNIQUE
            )
        ''')
        self.conn.commit()
    
    async def process_request(
        self,
        input_text: str,
        user_id: str,
        session_id: str,
        chat_history: List[ConversationMessage],
        additional_params: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Process task-related requests.

        Args:
            input_text (str): The user's input.
            user_id (str): Unique identifier for the user.
            session_id (str): Unique identifier for the session.
            chat_history (List[ConversationMessage]): The conversation history.
            additional_params (Optional[Dict[str, str]]): Additional request parameters.

        Returns:
            str: The response from SchruteBot.
        """
        message = input_text.lower().strip()
        print(f"📌 SchruteBot received: {message}")

        if message.startswith("add task"):
            task_description = message.replace("add task", "").strip()
            self.add_task(task_description)
            return f"✅ Task '{task_description}' added."

        elif message.startswith("complete task"):
            task_description = message.replace("complete task", "").strip()
            self.complete_task(task_description)
            return f"✅ Task '{task_description}' marked as complete."

        elif message == "view tasks":
            self.view_tasks()
            return "📋 Task list displayed."

        elif message == "daily report":
            self.daily_report()
            return "📊 Daily report generated."

        elif message == "dwightism":
            self.dwightism()
            return "💬 Dwight wisdom shared."

        elif message.startswith("prank toggle"):
            self.jimster.toggle_prank_mode()
            return "🎭 Prank mode toggled."

        else:
            return "❌ Command not recognized."


    def load_dwight_quotes(self):
        try:
            self.cursor.execute("SELECT line_text FROM dwight_quotes")
            quotes = [row[0] for row in self.cursor.fetchall()]
            if not quotes:
                raise sqlite3.OperationalError
            return quotes
        except sqlite3.OperationalError:
            return ["Error: You have failed to set up the database correctly. This is unacceptable."]
    
    def generate_hash(self, task):
        return hashlib.sha256(task.encode()).hexdigest()
    
    def add_task(self, task, priority="medium"):
        task = self.jimster.prank_task(task)  # Jimster may modify the task
        task_hash = self.generate_hash(task)
        self.cursor.execute("INSERT INTO tasks (description, priority, hash) VALUES (?, ?, ?)", (task, priority, task_hash))
        self.conn.commit()

        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        task_count = self.cursor.fetchone()[0]

        print(f"📌 **Task Added:** '{task}' (Priority: {priority.upper()})\n")
        
        if task_count > 10:
            context = f"Oh boy, here he goes again... overcommitting. Just like Michael at a sales call."
        elif task_count == 1:
            context = f"Finally, a task. I was starting to think you were as lazy as Jim."
        else:
            context = f"Good. Efficiency is key. Unlike Kevin’s work ethic."
        
        print("*Dwight's commentary is loading...*")
        time.sleep(1)
        print(self.generate_dynamic_response("add_task", context))
    
    def view_tasks(self):
        self.cursor.execute("SELECT description, status, priority FROM tasks ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END")
        tasks = self.cursor.fetchall()

        if not tasks:
            print("📋 **Task List Report - SchruteBot**\n\nNo tasks found. Productivity is the backbone of civilization!")
            return

        tasks = self.jimster.prank_task_list(tasks)  # Jimster may alter task descriptions
        task_list = "\n".join([f"🔹 **{desc}** *(Priority: {priority.upper()}, Status: {status})*" for desc, status, priority in tasks])
        print(f"📋 **Task List Report - SchruteBot**\n\nHere are your current assigned tasks:\n{task_list}\n")
        
        context = "Provide a sarcastic but insightful comment about the current workload."
        print("*Dwight's commentary is loading...*")
        time.sleep(1)
        print(f"\n*Dwight's commentary:* {self.generate_dynamic_response('view_tasks', context)}")
    
    def complete_task(self, task):
        task_hash = self.generate_hash(task)
        self.cursor.execute("UPDATE tasks SET status = 'completed' WHERE hash = ?", (task_hash,))
        self.conn.commit()

        if self.cursor.rowcount:
            print(f"✅ **Task Completed:** '{task}'\n")
            context = f"Impressive. But is it *truly* complete, or just half-heartedly done like Stanley's sales calls?"
        else:
            print(f"❌ **Task Not Found:** '{task}'\n")
            context = f"Either you never added it, or you are lying. And I *never* tolerate liars."
        
        print("*Dwight's commentary is loading...*")
        time.sleep(1)
        print(self.generate_dynamic_response("complete_task", context))
    
    def daily_report(self):
        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
        completed = self.cursor.fetchone()[0]
        print(f"📊 **Daily Report:** {completed} tasks completed.\n")
        context = f"Today, {completed} tasks were completed. That is {'acceptable' if completed > 5 else 'disappointing'}. Efficiency is key."
        print("*Dwight's commentary is loading...*")
        time.sleep(1)
        print(self.generate_dynamic_response("daily_report", context))
    
    def dwightism(self):
        print("*Dwight's wisdom is loading...*")
        time.sleep(1)
        print(self.generate_dynamic_response("dwightism"))
    
    def detect_idle(self, seconds):
        self.idle_time += seconds
        if self.idle_time > 10:
            print(self.generate_dynamic_response("idle"))
        else:
            print(self.generate_dynamic_response("working"))
    
    def generate_dynamic_response(self, prompt_type, context=""):
        quote_context = "\n".join(random.sample(self.cached_quotes, min(len(self.cached_quotes), 5)))
        prompt = f"Act as Dwight Schrute from The Office.\n\n**Scenario:** {context}\n\n**Use these Dwight quotes for inspiration:**\n{quote_context}\n\n**Now, respond as Dwight Schrute:**"
        return self.mistral.generate_response(prompt)
    

def main():
    bot = SchruteBot()
    parser = argparse.ArgumentParser(description='SchruteBot - The Productivity Enforcer')
    parser.add_argument('command', choices=['add', 'view', 'complete', 'report', 'dwightism', 'prank_toggle'], help='Command to execute')
    parser.add_argument('task', nargs='?', help='Task description (for add or complete)')
    parser.add_argument('--priority', choices=['high', 'medium', 'low'], default='medium', help='Priority level for the task')
    args = parser.parse_args()

    if args.command == 'add' and args.task:
        bot.add_task(args.task, args.priority)
    elif args.command == 'view':
        bot.view_tasks()
    elif args.command == 'complete' and args.task:
        bot.complete_task(args.task)
    elif args.command == 'report':
        bot.daily_report()
    elif args.command == 'dwightism':
        bot.dwightism()
    elif args.command == 'prank_toggle':
        bot.jimster.toggle_prank_mode()
    else:
        print("Invalid command or missing task description.")

if __name__ == '__main__':
    main()
