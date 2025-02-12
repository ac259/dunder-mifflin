import time
import random
import argparse
import sys

class SchruteBot:
    def __init__(self):
        self.tasks = []
        self.idle_time = 0
        self.nudges = [
            "Inactivity detected. If you were in the wild, you would be dead.",
            "Are you working or watching beets grow? Stay focused!",
            "Distractions are for the weak. Finish your task now!"
        ]

    def add_task(self, task):
        self.tasks.append(task)
        return f"Task added: {task}. Don't disappoint me."
    
    def view_tasks(self):
        if not self.tasks:
            return "No tasks? Unacceptable. You must always have something to do."
        return "Your tasks: " + ", ".join(self.tasks)
    
    def complete_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            return f"Task '{task}' completed. Adequate."
        else:
            return f"Task '{task}' not found. This inefficiency disgusts me."
    
    def detect_idle(self, seconds):
        self.idle_time += seconds
        if self.idle_time > 10:
            return random.choice(self.nudges)
        return "Good. Keep working."
    
    def daily_report(self):
        completed = 5 - len(self.tasks)
        return f"You completed {completed}/5 tasks. This is acceptable. Barely."

def main():
    bot = SchruteBot()
    parser = argparse.ArgumentParser(description='SchruteBot - The Productivity Enforcer')
    parser.add_argument('command', choices=['add', 'view', 'complete', 'report'], help='Command to execute')
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
    else:
        print("Invalid command or missing task description.")

if __name__ == '__main__':
    main()