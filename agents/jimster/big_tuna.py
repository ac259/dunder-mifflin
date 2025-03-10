import random
import json
import os
from common.mistral_agent import MistralAgent
from multi_agent_orchestrator.agents import Agent, AgentOptions, AgentCallbacks
from multi_agent_orchestrator.types import ConversationMessage
from typing import List, Optional, Dict

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

        self.mistral = MistralAgent()
        self.keywords = ["prank", "joke", "fake task", "trick", "mischief", "fun"] 

        # Load prank settings
        config = self.load_config()
        self.prank_mode = config["prank_mode"]
        self.prank_probability = config["prank_probability"]
        self.fake_task_probability = config["fake_task_probability"]

    async def process_request(
        self,
        input_text: str,
        user_id: str,
        session_id: str,
        chat_history: List[ConversationMessage],
        additional_params: Optional[Dict[str, str]] = None
    ) -> str:
        """Processes prank-related requests."""
        message = input_text.lower().strip()
        print(f"🤡 JimsterAgent received: {message}")

        if message.startswith("prankify task"):
            task_description = message.replace("prankify task", "").strip()
            prank_dict = self.generate_prank_dictionary([(task_description, "", "")])
            pranked_task = self.prank_task(task_description, prank_dict)
            return f"🤡 Pranked Task: '{pranked_task}'"

        elif message == "generate prank task":
            fake_task = self.generate_fake_task()
            return f"🎭 Fake Task: {fake_task}"

        elif message == "toggle prank mode":
            return self.toggle_prank_mode()

        return "❌ Command not recognized."
    
    def load_config(self) -> Dict[str, any]:
        """Loads Jimster's prank settings from config file."""
        if not os.path.exists(CONFIG_FILE):
            return {"prank_mode": True, "prank_probability": 0.3, "fake_task_probability": 0.1}
        
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)

    def toggle_prank_mode(self) -> str:
        """Toggles prank mode ON/OFF and updates config file."""
        self.prank_mode = not self.prank_mode
        with open(CONFIG_FILE, "w") as file:
            json.dump({
                "prank_mode": self.prank_mode,
                "prank_probability": self.prank_probability,
                "fake_task_probability": self.fake_task_probability
            }, file)
        
        status = "ON" if self.prank_mode else "OFF"
        return f"🎭 Jimster's Prank Mode is now {status}!"

    def generate_prank_dictionary(self, tasks: List[tuple]) -> Dict[str, str]:
        """Generates a prank word substitution dictionary using Mistral."""
        if not tasks:
            return {}

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

    def prank_task(self, task: str, prank_dict: Optional[Dict[str, str]] = None) -> str:
        """Modifies task description using the prank dictionary."""
        if not self.prank_mode:
            return task

        if prank_dict is None:
            prank_dict = self.generate_prank_dictionary([(task, "", "")])

        words = task.split()
        pranked_words = [prank_dict.get(word, word) for word in words]
        return " ".join(pranked_words)

    def generate_fake_task(self) -> str:
        """Generates a single absurd fake task using Mistral."""
        prompt = """You are Jim Halpert from The Office. Generate a single, absurd fake task that would confuse Dwight but still seem vaguely plausible.
        **ONLY return the task description, no extra commentary.**
        Example Output:
        "Hide all of SchruteBot’s beets"
        """
        return self.mistral.generate_response(prompt).strip().strip('"')

    def prank_task_list(self, tasks: List[tuple]) -> List[tuple]:
        """Modifies some task descriptions in the task list and generates dynamic fake tasks."""
        if not self.prank_mode:
            return tasks

        prank_dict = self.generate_prank_dictionary(tasks)
        pranked_tasks = []

        for desc, status, priority in tasks:
            if random.random() < self.prank_probability:  # Use config value
                desc = self.prank_task(desc, prank_dict)
            pranked_tasks.append((desc, status, priority))

        if random.random() < self.fake_task_probability:  # Use config value
            fake_task = self.generate_fake_task()
            pranked_tasks.append((fake_task, "pending", "low"))

        return pranked_tasks
