from transformers import pipeline, AutoTokenizer

model_name = "google/gemma-3-1b-pt"
tokenizer = AutoTokenizer.from_pretrained(model_name)
pipe = pipeline("text-generation", model=model_name, tokenizer=tokenizer, device="mps", torch_dtype="auto")

output = pipe("Eiffel tower is located in", max_new_tokens=50)
print(output)