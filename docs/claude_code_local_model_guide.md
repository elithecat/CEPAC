# Using Claude Code with a Local Model (Ollama + Llama)

Claude Code can be pointed at any API endpoint that implements the Anthropic Messages API format. The easiest way to run a local model is through **Ollama**, which supports Anthropic API compatibility.

## Prerequisites

- Claude Code CLI installed
- Ollama v0.14.0+ installed ([ollama.com](https://ollama.com))
- Sufficient hardware: 16GB+ RAM minimum, GPU with 16-24GB VRAM recommended (or Apple Silicon with 32GB+ unified memory)

## Step 1: Pull a Model

```bash
# Llama 3.1 8B — good starting point, runs on modest hardware
ollama pull llama3.1:8b

# Llama 3.1 70B — much more capable, needs ~40GB VRAM
ollama pull llama3.1:70b

# Alternatives strong at coding:
ollama pull qwen2.5-coder:32b
ollama pull deepseek-coder-v2:16b
```

## Step 2: Start Ollama

```bash
# Ollama usually runs as a background service after install.
# Verify it's running:
ollama list

# Or start it manually:
ollama serve
```

By default, Ollama serves on `http://localhost:11434`.

## Step 3: Configure Claude Code

Set the environment variables to point Claude Code at your local Ollama instance:

```bash
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
```

You can make this persistent by adding to your shell profile, or by using Claude Code's settings:

```bash
claude config set -g env.ANTHROPIC_BASE_URL "http://localhost:11434"
claude config set -g env.ANTHROPIC_AUTH_TOKEN "ollama"
```

Or edit `~/.claude/settings.json` directly:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama"
  }
}
```

## Step 4: Launch Claude Code with Your Model

```bash
# Specify the model on launch
claude --model llama3.1:8b

# Or switch models during a session
/model llama3.1:8b
```

## Important Limitations

**Context window:** Claude Code is designed for large context windows (64K+ tokens). Most local models have smaller context windows, which means Claude Code may struggle with large codebases or multi-file operations.

**Tool use:** Claude Code relies heavily on tool use (function calling). Not all local models support tool use well. Models fine-tuned for tool use (like Llama 3.1, Qwen 2.5 Coder) work best.

**Performance:** Even on a good GPU, local models are significantly slower than the Anthropic API. Expect longer waits, especially for planning and multi-step tasks.

**Capability:** Smaller local models will make more mistakes, produce lower-quality code, and struggle with complex reasoning compared to Claude. This is a tradeoff for privacy and cost.

## Switching Back to Anthropic

To return to using the Anthropic API:

```bash
unset ANTHROPIC_BASE_URL
unset ANTHROPIC_AUTH_TOKEN

# Or remove from settings:
claude config set -g env.ANTHROPIC_BASE_URL ""
```

## Alternative: Cloud Providers

If you want Claude models through your own cloud infrastructure (not local open-source models), Claude Code has first-class support for:

```bash
# Amazon Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Google Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
```

These give you Claude models through your own cloud account, with data staying in your infrastructure.
