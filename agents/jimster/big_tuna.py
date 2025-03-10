import random
import json
import os
from common.mistral_agent import MistralAgent
from multi_agent_orchestrator.agents import Agent, AgentOptions, AgentCallbacks

CONFIG_FILE = "config.json"

class JimsterAgent(Agent):
    def __init__(self):
        options = AgentOptions(
            name="JimsterAgent",
            description="A prankster assistant specializing in humorous task modifications and fake assignments.",
            save_chat=True,
            callbacks=AgentCallbacks(),
            LOG_AGENT_DEBUG_TRACE=False
        )
        super().__init__(options)
        config = self.load_config()
        self.keywords = ["prank", "joke", "fake task", "trick", "mischief", "fun"] 
        self.prank_mode = config["prank_mode"]
        self.prank_probability = config["prank_probability"]
        self.fake_task_probability = config["fake_task_probability"]
        self.mistral = MistralAgent()

    def process_request(self, message: str):
        """Handles prank-related requests for JimsterAgent."""
        message = message.lower().strip()

        if message.startswith("prankify task"):
            task_description = message.replace("prankify task", "").strip()
            pranked_task = self.prank_task(task_description, self.generate_prank_dictionary([(task_description, "", "")]))
            return f"🤡 Pranked Task: '{pranked_task}'"

        elif message == "generate prank task":
            fake_task = self.mistral.generate_response("Generate a single, absurd fake task.")
            return f"🎭 Fake Task: {fake_task.strip()}"

        elif message == "toggle prank mode":
            self.toggle_prank_mode()
            return "🎭 Prank mode toggled."

        else:
            return "❌ Command not recognized."

    
    def load_config(self):
        """Loads Jimster's settings from config file."""
        if not os.path.exists(CONFIG_FILE):
            return {"prank_mode": True, "prank_probability": 0.3, "fake_task_probability": 0.1}
        
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)

    def toggle_prank_mode(self):
        """Toggles prank mode ON/OFF and updates config file."""
        self.prank_mode = not self.prank_mode
        with open(CONFIG_FILE, "w") as file:
            json.dump({"prank_mode": self.prank_mode, "prank_probability": self.prank_probability, "fake_task_probability": self.fake_task_probability}, file)
        status = "ON" if self.prank_mode else "OFF"
        print(f"🎭 Jimster's Prank Mode is now {status}!")

    def generate_prank_dictionary(self, tasks):
        """Uses Mistral to generate a prank word substitution dictionary based on the task list."""
        task_descriptions = "\n".join([task[0] for task in tasks])
        prompt = f"""
        You are Jim Halpert from The Office. You love pranking Dwight.
        Based on the following task descriptions, generate a humorous word substitution dictionary that makes tasks ridiculous but still recognizable.
        
        Task List:
        {task_descriptions}
        
        Example output format: {{"meeting": "party", "report": "memoir", "presentation": "stand-up routine"}}
        """
        
        response = self.mistral.generate_response(prompt)
        try:
            prank_dict = json.loads(response)
            return prank_dict if isinstance(prank_dict, dict) else {}
        except json.JSONDecodeError:
            return {}

    def prank_task(self, task, prank_dict):
        """Slightly modifies task description using the generated prank dictionary."""
        if not self.prank_mode:
            return task
        
        words = task.split()
        pranked_words = [prank_dict.get(word, word) for word in words]
        return " ".join(pranked_words)

    def prank_task_list(self, tasks):
        """Randomly modifies some task descriptions in the task list and generates dynamic fake tasks."""
        if not self.prank_mode:
            return tasks

        prank_dict = self.generate_prank_dictionary(tasks)
        pranked_tasks = []
        for desc, status, priority in tasks:
            if random.random() < self.prank_probability:  # Use config value
                desc = self.prank_task(desc, prank_dict)
            pranked_tasks.append((desc, status, priority))

        if random.random() < self.fake_task_probability:  # Use config value
            prompt = """You are Jim Halpert from The Office. Generate a single, absurd fake task that would confuse Dwight but still seem vaguely plausible.
            **ONLY return the task description, no extra commentary.**
            Example Output:
            "Hide all of SchruteBot’s beets"
            """
            fake_task = self.mistral.generate_response(prompt).strip().strip('"')  # Removes any quotes if present
            pranked_tasks.append((fake_task, "pending", "low"))

        return pranked_tasks

