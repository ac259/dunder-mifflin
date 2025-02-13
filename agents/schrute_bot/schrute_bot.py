import time
import random
import argparse
import sqlite3
import hashlib
import sys
import os
from datetime import datetime

# Add project root to sys.path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from common.mistral_agent import MistralAgent


DB_FILE = "schrutebot.db"

class SchruteBot:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.idle_time = 0
        self.nudges = self.load_dwight_quotes()
        self.mistral = MistralAgent()
        self.cached_quotes = self.load_dwight_quotes()
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                hash TEXT UNIQUE
            )
        ''')
        self.conn.commit()
    
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
    
    def add_task(self, task):
        task_hash = self.generate_hash(task)
        self.cursor.execute("INSERT INTO tasks (description, hash) VALUES (?, ?)", (task, task_hash))
        self.conn.commit()

        # Check task count for dynamic responses
        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        task_count = self.cursor.fetchone()[0]

        if task_count > 10:
            context = f"A new task was added: '{task}'. Oh boy, here he goes again... overcommitting. Just like Michael at a sales call."
        elif task_count == 1:
            context = f"A new task was added: '{task}'. Finally, a task. I was starting to think you were as lazy as Jim."
        else:
            context = f"A new task was added: '{task}'. Good. Efficiency is key. Unlike Kevin’s work ethic."

        return self.generate_dynamic_response("add_task", context)

    
    def view_tasks(self):
        self.cursor.execute("SELECT description, status FROM tasks")
        tasks = self.cursor.fetchall()

        if not tasks:
            return self.generate_dynamic_response("view_tasks", "No tasks found. Someone is slacking.")

        task_list = "\n".join([f"- {desc} ({status})" for desc, status in tasks])
        context = f"Here are the current assigned tasks:\n{task_list}"

        return self.generate_dynamic_response("view_tasks", context)


    
    def complete_task(self, task):
        task_hash = self.generate_hash(task)
        self.cursor.execute("UPDATE tasks SET status = 'completed' WHERE hash = ?", (task_hash,))
        self.conn.commit()

        if self.cursor.rowcount:
            context = f"The task '{task}' was marked as completed. Impressive. But is it *truly* complete, or just half-heartedly done like Stanley's sales calls?"
        else:
            context = f"Task '{task}' was *not* found. Either you never added it, or you are lying. And I *never* tolerate liars."

        return self.generate_dynamic_response("complete_task", context)

    
    def detect_idle(self, seconds):
        self.idle_time += seconds
        if self.idle_time > 10:
            return self.generate_dynamic_response("idle")
        return self.generate_dynamic_response("working")
    
    def daily_report(self):
        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
        completed = self.cursor.fetchone()[0]
        context = f"Today, {completed} tasks were completed. That is {'acceptable' if completed > 5 else 'disappointing'}. Efficiency is key."
        return self.generate_dynamic_response("daily_report", context)

    
    def dwightism(self):
        return self.generate_dynamic_response("dwightism")
    
    def generate_dynamic_response(self, prompt_type, context=""):
        """Generates a function-specific, context-aware Dwight Schrute response."""
        quote_context = "\n".join(random.sample(self.cached_quotes, min(len(self.cached_quotes), 5)))

        # Define specific prompts for each function
        prompts = {
            "view_tasks": f"""
            Act as Dwight Schrute from The Office.
            Your coworker has requested to see the list of current tasks.
            You must list out the tasks **clearly** but also provide your classic Dwight commentary.
            
            **Scenario:** {context}

            **Use these Dwight quotes for inspiration:**
            {quote_context}

            **Now, respond as Dwight Schrute and include the list of tasks:**
            """,

            "add_task": f"""
            Act as Dwight Schrute from The Office.
            A new task has been added. You must acknowledge it, but also critique whether it is an efficient use of time.
            
            **Scenario:** {context}

            **Use these Dwight quotes for inspiration:**
            {quote_context}

            **Now, respond as Dwight Schrute and confirm the task addition:**
            """,

            "complete_task": f"""
            Act as Dwight Schrute from The Office.
            A coworker claims they have completed a task. You must verify this and provide commentary on the importance of efficiency and discipline.
            
            **Scenario:** {context}

            **Use these Dwight quotes for inspiration:**
            {quote_context}

            **Now, respond as Dwight Schrute and confirm task completion:**
            """,

            "daily_report": f"""
            Act as Dwight Schrute from The Office.
            You are generating a daily report on completed tasks. Give the user a motivational speech about efficiency and discipline.
            
            **Scenario:** {context}

            **Use these Dwight quotes for inspiration:**
            {quote_context}

            **Now, respond as Dwight Schrute and summarize the daily report:**
            """,

            "dwightism": f"""
            Act as Dwight Schrute from The Office.
            Provide a wise, fact-driven, and slightly aggressive statement that only Dwight Schrute would say.
            
            **Scenario:** {context}

            **Use these Dwight quotes for inspiration:**
            {quote_context}

            **Now, respond as Dwight Schrute:**
            """
        }

        # Use the correct prompt based on the function
        prompt = prompts.get(prompt_type, "Error: Invalid prompt type provided.")

        return self.mistral.generate_response(prompt)

    

def main():
    bot = SchruteBot()
    parser = argparse.ArgumentParser(description='SchruteBot - The Productivity Enforcer')
    parser.add_argument('command', choices=['add', 'view', 'complete', 'report', 'dwightism'], help='Command to execute')
    parser.add_argument('task', nargs='?', help='Task description (for add or complete)')
    args = parser.parse_args()

    if args.command == 'add' and args.task:
        print(bot.add_task(args.task))
    elif args.command == 'view':
        print(bot.view_tasks())
    elif args.command == 'complete' and args.task:
        print(bot.complete_task(args.task))
    elif args.command == 'report':
        print(bot.daily_report())
    elif args.command == 'dwightism':
        print(bot.dwightism())
    else:
        print("Invalid command or missing task description.")

if __name__ == '__main__':
    main()
