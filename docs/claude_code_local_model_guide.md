# Using Claude Code with a Local Model (Docker + Ollama + Llama)

Claude Code can be pointed at any API endpoint that implements the Anthropic Messages API format. This guide runs Claude Code in a Docker container and connects it to a local model served by Ollama.

## What Goes Where

You will install two things on your machine: **Docker** and **Ollama**. Claude Code itself is never installed on your machine — it runs entirely inside a Docker container.

| Component | Where it runs |
|-----------|---------------|
| Docker | Your machine |
| Ollama (model server) | Your machine |
| Claude Code | Inside a Docker container |

**Hardware for local models:** 16GB+ RAM minimum, GPU with 16-24GB VRAM recommended (or Apple Silicon with 32GB+ unified memory). CPU-only works but will be slow.

## Step 1: Install Docker and Ollama

Install Docker from [docs.docker.com/get-docker](https://docs.docker.com/get-docker/). Install Ollama from [ollama.com](https://ollama.com). Then pull a model:

```bash
# Llama 3.1 8B — good starting point, runs on modest hardware
ollama pull llama3.1:8b

# Llama 3.1 70B — much more capable, needs ~40GB VRAM
ollama pull llama3.1:70b

# Alternatives strong at coding:
ollama pull qwen2.5-coder:32b
ollama pull deepseek-coder-v2:16b
```

Verify Ollama is running:

```bash
ollama list
```

Ollama serves on `http://localhost:11434` by default.

## Step 2: Create the Claude Code Docker Image

Create a file called `Dockerfile`:

```dockerfile
FROM node:20

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /workspace && chmod 777 /workspace
WORKDIR /workspace

RUN npm install -g @anthropic-ai/claude-code@latest

ENTRYPOINT ["claude"]
```

Build the image:

```bash
docker build -t claude-code .
```

## Step 3: Run Claude Code in Docker

The key flags:
- `-it` gives Claude Code an interactive terminal (required)
- `-v` mounts your project directory into the container
- `-e` passes environment variables to point at Ollama
- `--network host` lets the container reach Ollama on localhost

```bash
docker run -it \
  --network host \
  -e ANTHROPIC_BASE_URL=http://localhost:11434 \
  -e ANTHROPIC_AUTH_TOKEN=ollama \
  -v $(pwd):/workspace \
  claude-code --model llama3.1:8b
```

To use Claude with the Anthropic API instead of a local model, pass your API key:

```bash
docker run -it \
  -e ANTHROPIC_API_KEY=your-key-here \
  -v $(pwd):/workspace \
  claude-code
```

## Step 4: Make It Convenient

Create a shell alias so you don't have to type the full command every time. Add this to your `~/.bashrc` or `~/.zshrc`:

```bash
alias claude='docker run -it --network host \
  -e ANTHROPIC_BASE_URL=http://localhost:11434 \
  -e ANTHROPIC_AUTH_TOKEN=ollama \
  -v $(pwd):/workspace \
  claude-code --model llama3.1:8b'
```

Then just run:

```bash
cd /path/to/your/project
claude
```

### Docker Compose Alternative

Create a `docker-compose.yml`:

```yaml
services:
  claude-code:
    build: .
    network_mode: host
    environment:
      ANTHROPIC_BASE_URL: http://localhost:11434
      ANTHROPIC_AUTH_TOKEN: ollama
    volumes:
      - .:/workspace
    stdin_open: true
    tty: true
```

Run with:

```bash
docker compose run --rm claude-code --model llama3.1:8b
```

## Important Limitations

**Context window:** Claude Code is designed for large context windows (64K+ tokens). Most local models have smaller context windows, which means Claude Code may struggle with large codebases or multi-file operations.

**Tool use:** Claude Code relies heavily on tool use (function calling). Not all local models support tool use well. Models fine-tuned for tool use (like Llama 3.1, Qwen 2.5 Coder) work best.

**Performance:** Even on a good GPU, local models are significantly slower than the Anthropic API. Expect longer waits, especially for planning and multi-step tasks.

**Capability:** Smaller local models will make more mistakes, produce lower-quality code, and struggle with complex reasoning compared to Claude. This is a tradeoff for privacy and cost.

## Switching Models

You can switch models by changing the `--model` flag:

```bash
docker run -it --network host \
  -e ANTHROPIC_BASE_URL=http://localhost:11434 \
  -e ANTHROPIC_AUTH_TOKEN=ollama \
  -v $(pwd):/workspace \
  claude-code --model qwen2.5-coder:32b
```

Or switch during a session with `/model llama3.1:8b`.

## Alternative: Cloud Providers

If you want Claude models through your own cloud infrastructure (not local open-source models), Claude Code has first-class support for:

```bash
# Amazon Bedrock
docker run -it -e CLAUDE_CODE_USE_BEDROCK=1 ...

# Google Vertex AI
docker run -it -e CLAUDE_CODE_USE_VERTEX=1 ...
```

These give you Claude models through your own cloud account, with data staying in your infrastructure.
