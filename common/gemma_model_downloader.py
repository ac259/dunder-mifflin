from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
import os
import torch

model_name = "google/gemma-3-1b-pt"
save_directory = os.path.join(os.path.dirname(__file__), "gemma-3-1b-pt")

# Create directory if it doesn't exist
os.makedirs(save_directory, exist_ok=True)

# Load and save tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_directory)

# Load model with explicit dtype and device mapping
model = AutoModelForCausalLM.from_pretrained(
    model_name, torch_dtype=torch.float16, device_map="auto"
)
model.save_pretrained(save_directory)

print(f"Model and tokenizer saved in '{save_directory}'")
