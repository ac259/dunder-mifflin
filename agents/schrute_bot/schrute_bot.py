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
from agents.jimster_agent import JimsterAgent

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
    elif args.command == 'prank_toggle':
        bot.jimster.toggle_prank_mode()
    else:
        print("Invalid command or missing task description.")

if __name__ == '__main__':
    main()
