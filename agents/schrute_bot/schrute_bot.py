import time
import random
import argparse
import sqlite3
import hashlib
from datetime import datetime

DB_FILE = "schrutebot.db"

class SchruteBot:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.idle_time = 0
        self.nudges = self.load_dwight_quotes()
    
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
        return f"Task added: {task}. Don't disappoint me."
    
    def view_tasks(self):
        self.cursor.execute("SELECT description, status FROM tasks")
        tasks = self.cursor.fetchall()
        if not tasks:
            return "No tasks? Unacceptable. You must always have something to do."
        return "Your tasks: " + ", ".join([f"{t[0]} ({t[1]})" for t in tasks])
    
    def complete_task(self, task):
        task_hash = self.generate_hash(task)
        self.cursor.execute("UPDATE tasks SET status = 'completed' WHERE hash = ?", (task_hash,))
        self.conn.commit()
        if self.cursor.rowcount:
            return f"Task '{task}' completed. Adequate."
        else:
            return f"Task '{task}' not found. This inefficiency disgusts me."
    
    def detect_idle(self, seconds):
        self.idle_time += seconds
        if self.idle_time > 10:
            return random.choice(self.nudges)
        return "Good. Keep working."
    
    def daily_report(self):
        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
        completed = self.cursor.fetchone()[0]
        return f"You completed {completed} tasks today. This is acceptable. Barely."
    
    def dwightism(self):
        return random.choice(self.nudges)

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
