from transformers import AutoModelForCausalLM, AutoTokenizer
import os

model_name = "Qwen/Qwen2.5-32B-Instruct"
save_directory = os.path.join(os.path.dirname(__file__), "qwen2_5_32b_instruct")

# Create directory if it doesn't exist
os.makedirs(save_directory, exist_ok=True)

# Load and save tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_directory)

# Load model (with automatic dtype and device mapping)
model = AutoModelForCausalLM.from_pretrained(
    model_name, torch_dtype="auto", device_map="auto"
)
model.save_pretrained(save_directory)

print(f"Model and tokenizer saved in '{save_directory}'")
