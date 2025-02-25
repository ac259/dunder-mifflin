# MODELS 

High Context -> Slow speed - tradeoff analysis

To determine the largest model you can run locally for PamBot on your Mac M1 with 16GB of RAM, prioritizing maximum context size over speed, I’ve analyzed the constraints of your hardware and the models available on Ollama’s library (https://ollama.com/library). Here’s a complete breakdown and recommendation tailored to your needs.

### Hardware Constraints
Your Mac M1 has 16GB of unified memory, shared between the CPU and GPU. This means the total memory available for the model, its context, and the PamBot application must fit within this limit, leaving some room for the operating system (typically 2-4GB). Since you don’t prioritize speed, we can push the memory usage close to the 16GB ceiling, accepting potential slowness or minor swapping.

### Model Considerations
Ollama supports various models, such as Llama 2, Mistral, Qwen, and others, optimized for local execution. The “largest” model here refers to the one offering the maximum context size (the number of tokens it can process at once), as that’s your priority, rather than parameter count alone. Larger context sizes enable PamBot to handle more extensive inputs, which is ideal for research tasks requiring comprehensive text processing.

Models come in different parameter sizes (e.g., 7B, 13B, 70B), and their memory usage depends on:
- **Weights**: Determined by parameter count and quantization level (e.g., 4-bit reduces memory needs).
- **Context**: Memory scales with context size, though optimizations like sliding window attention (used in Mistral) keep this linear rather than quadratic.

Since you’re currently using Mistral (likely Mistral 7B, with a context size of 8192 tokens), we’ll explore alternatives that offer larger context sizes while fitting within 16GB RAM.

### Memory Estimation
For a transformer model:
- **Weights**: A 4-bit quantized model uses approximately 0.5 bytes per parameter. For example:
  - 7B parameters ≈ 3.5GB
  - 13B parameters ≈ 6.5GB
  - 70B parameters ≈ 35GB (far exceeding 16GB, so ruled out)
- **Context**: Memory depends on the number of tokens (C), layers (L), and hidden size (H), but a rough estimate for 7B models is 1-2GB for 8192 tokens, scaling linearly with context size due to optimizations in modern models.

PamBot’s additional overhead is assumed to be minimal, so the model and context memory dominate.

### Model Options from Ollama
Let’s evaluate models available on Ollama, focusing on those with large context sizes that fit your hardware:

#### 1. Mistral 7B
- **Parameters**: 7B
- **Context Size**: 8192 tokens
- **Memory**: ~3.5GB (weights) + ~2GB (context) = ~5.5GB total
- **Fit**: Comfortably within 16GB, leaving ample room.
- **Notes**: Since you’re using Mistral, this is your baseline. It’s efficient due to sliding window attention but offers a moderate context size.

#### 2. Llama 2 7B
- **Parameters**: 7B
- **Context Size**: 4096 tokens
- **Memory**: ~3.5GB (weights) + ~1GB (context) = ~4.5GB total
- **Fit**: Easily fits, but the context is smaller than Mistral’s 8192, making it less ideal.

#### 3. Llama 2 13B
- **Parameters**: 13B
- **Context Size**: 4096 tokens
- **Memory**: ~6.5GB (weights) + ~1.5GB (context) = ~8GB total
- **Fit**: Fits with a larger context (e.g., 2048 tokens uses less), but 4096 is tight (~10-12GB total possible). Swapping may occur if other apps run.
- **Notes**: Larger parameter count than Mistral, but smaller context size limits its appeal.

#### 4. CodeLlama 7B
- **Parameters**: 7B
- **Context Size**: Up to 16,384 tokens (some variants support this)
- **Memory**: ~3.5GB (weights) + ~4GB (context at 16k) = ~7.5-8GB total
- **Fit**: Fits comfortably within 16GB.
- **Notes**: Designed for coding, but usable for general tasks. Offers a larger context than Mistral.

#### 5. Qwen 1.5 7B
- **Parameters**: 7B
- **Context Size**: 32,768 tokens
- **Memory**: ~3.5GB (weights) + ~8GB (context at 32k) = ~11.5-12GB total
- **Fit**: Fits within 16GB, leaving ~4GB for the system, though it’s snug. You may need to close other applications.
- **Notes**: Available on Ollama (e.g., `ollama run qwen:7b`). Its 32k context is significantly larger than Mistral’s 8192, ideal for extensive research inputs.

#### 6. Yarn-Mistral 7B
- **Parameters**: 7B
- **Context Size**: Up to 128,000 tokens
- **Memory**: ~3.5GB (weights) + ~32GB (context at 128k, scaled linearly) = ~35GB total
- **Fit**: Exceeds 16GB by a wide margin, even with optimizations.
- **Notes**: While theoretically a 7B model, the massive context size makes it impractical without drastic memory-saving techniques unavailable in standard Ollama setups.

#### 7. RWKV 7B
- **Parameters**: 7B
- **Context Size**: Effectively unlimited (e.g., 100k+ tokens)
- **Memory**: ~4GB (weights) + minimal context memory (<1GB even for large contexts)
- **Fit**: Easily fits (~5GB total).
- **Notes**: An RNN-based model, not a transformer, with constant memory usage for context. However, it may underperform transformers for research tasks requiring deep contextual understanding.

### Recommendation
Since you prioritize maximum context size over speed for PamBot’s research tasks, the **Qwen 1.5 7B** model stands out. Here’s why:
- **Context Size**: 32,768 tokens—four times larger than Mistral’s 8192—allowing PamBot to process much longer inputs without truncation.
- **Memory Fit**: Approximately 12GB total (3.5GB weights + 8GB context), fitting within your 16GB RAM, though you should minimize background applications to avoid swapping.
- **Availability**: Supported by Ollama, installable via `ollama run qwen:7b`.
- **Suitability**: As a transformer model, it aligns with PamBot’s likely need for strong contextual understanding, unlike RWKV.

While CodeLlama 7B (16k context) is a solid alternative, Qwen 1.5 7B doubles that context size, offering more flexibility for extensive research documents. Larger models like Llama 2 13B or 70B either fit poorly (13B with reduced context) or not at all (70B), and Yarn-Mistral’s 128k context exceeds your memory capacity.

### Final Answer
For your Mac M1 with 16GB RAM, the largest model you can run locally for PamBot, prioritizing maximum context size over speed, is **Qwen 1.5 7B**. It supports a context size of 32,768 tokens and should work better than Mistral for tasks requiring large context, such as research, assuming you can tolerate potential slowness due to high memory usage. To install it, run:

```bash
ollama run qwen:7b
```

This model balances your hardware constraints with your need for a substantial context window, enhancing PamBot’s capabilities for your task.