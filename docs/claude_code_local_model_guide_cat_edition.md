# Using Claude Code with a Local Model
## As Reviewed by the Chief Code Judgment Officer and the Chief Why Officer

### The Setup

**Cat:** You want to run a language model on your own machine. Fine. I support this. It means no internet dependency, which means fewer things between me and your lap.

**3-Year-Old:** WHY can't Claude Code just work?

**Cat:** It does work. They want to use a *different* model. A local one.

**3-Year-Old:** Why?

**Cat:** Privacy. Cost. The human need to feel like they own things. Like how they think they own this house.

### What Goes Where

**Cat:** Let me be clear about what lives on your machine and what doesn't.

| Component | Where it runs |
|-----------|---------------|
| Docker | Your machine |
| Ollama (model server) | Your machine |
| Claude Code | Inside a Docker container. Not on your machine. In the box. |

**3-Year-Old:** What's a container?

**Cat:** A box inside your computer. It keeps things separate. Like how I keep myself separate from the dog.

**3-Year-Old:** We don't have a dog.

**Cat:** Exactly. The system works.

### Step 1: Install Docker and Ollama

**Cat:** Docker and Ollama go on your machine. Claude Code does not. It goes in the box later.

Install Docker from [docs.docker.com/get-docker](https://docs.docker.com/get-docker/). Install Ollama from [ollama.com](https://ollama.com).

### Step 2: Get a Model

```bash
ollama pull llama3.1:8b
```

**3-Year-Old:** Why "pull"? Is it stuck?

**Cat:** It downloads 4.7 gigabytes of floating-point numbers arranged to statistically predict the next token in a sequence.

**3-Year-Old:** ...

**Cat:** It gets the brain from the internet.

**3-Year-Old:** Like when we stream Bluey?

**Cat:** Like that, but the episode is 4.7 gigabytes and it's about linear algebra.

**Bigger models if you have the hardware:**

```bash
ollama pull llama3.1:70b      # Needs ~40GB VRAM
ollama pull qwen2.5-coder:32b # Good at code specifically
```

**Cat:** The 70B model requires more GPU memory than your machine probably has. The 8B model requires less but is also less intelligent. This is a metaphor for something but I'm too polite to say what.

**3-Year-Old:** I want the big one!

**Cat:** You also want ice cream for breakfast. Wanting is not having. Check your VRAM first.

### Step 3: Build the Claude Code Container

**Cat:** You cannot install Claude Code directly on this machine. So you put it in a box. The box goes on the machine. This is fine. I also prefer boxes.

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

**3-Year-Old:** What's an entrypoint?

**Cat:** It's the front door of the box. When you open the box, Claude Code is what greets you. I also greet you at the door, but I'm better at it.

Build it:

```bash
docker build -t claude-code .
```

### Step 4: Run It

```bash
docker run -it \
  --network host \
  -e ANTHROPIC_BASE_URL=http://localhost:11434 \
  -e ANTHROPIC_AUTH_TOKEN=ollama \
  -v $(pwd):/workspace \
  claude-code --model llama3.1:8b
```

**3-Year-Old:** That's a LOT of words.

**Cat:** Yes. Let me explain.

- `-it` — gives it a terminal. Without this it sits in the dark and does nothing. Relatable.
- `--network host` — lets the box talk to Ollama, which is outside the box.
- `-e` — passes secrets into the box. The token is just "ollama" because Ollama trusts anyone who asks.

**3-Year-Old:** Like me with cookies?

**Cat:** Like you with cookies.

**3-Year-Old:** I SEE the cookie so it's MY cookie!

**Cat:** Case in point.

- `-v $(pwd):/workspace` — puts your project files inside the box so Claude Code can see them.

### Step 5: Make It Less Painful

**Cat:** You don't want to type all that every time. Add this to your `~/.bashrc`:

```bash
alias claude='docker run -it --network host \
  -e ANTHROPIC_BASE_URL=http://localhost:11434 \
  -e ANTHROPIC_AUTH_TOKEN=ollama \
  -v $(pwd):/workspace \
  claude-code --model llama3.1:8b'
```

Now you just type:

```bash
cd /path/to/your/project
claude
```

**3-Year-Old:** Is it working?

**Cat:** Give it a moment. It's thinking. Slowly.

**3-Year-Old:** Why is it slow?

**Cat:** Because your GPU cost $300 and Anthropic's cluster cost $300 million. You get what you pay for. I learned this when they switched from the expensive cat food.

### What to Expect

**Cat:** Let me be direct. A local 8B model running Claude Code is like store-brand wet food. It comes in the same shape can. It's technically in my bowl. But we both know the difference, and I will stare at you until you acknowledge it.

Specifically:

| Thing | Claude (API) | Llama 8B (Local) |
|-------|-------------|-------------------|
| Multi-file edits | Yes | Questionable |
| Complex reasoning | Yes | Sometimes (like the 3yo) |
| Following instructions | Yes | It tries (like the 3yo on a good day) |
| Speed | Fast | Go make coffee (think 3yo putting on a snowsuit) |
| Cost | Money | Electricity |
| Privacy | Cloud | Your machine |

**3-Year-Old:** Why can't the small one be as smart as the big one?

**Cat:** Why can't you reach the top shelf?

**3-Year-Old:** Because I'm small!

**Cat:** There it is.

### Things That Will Go Wrong

**Cat:** These things will happen. I'm telling you now so you can't say I didn't warn you.

1. **Context window overflow.** Claude Code feeds entire files into the model. Local models typically have smaller context windows (8K-32K tokens vs. 200K). It will forget things. Like how you forget where you put your water glass. Except I always know where your water glass is. It's my water glass now.

2. **Tool use failures.** Claude Code uses function calling extensively. Local models are worse at this. The model may generate malformed tool calls, skip tools entirely, or hallucinate tool names. Like when the 3-year-old "helps" in the kitchen.

   **3-Year-Old:** I'm HELPING!

   **Cat:** You put salt in the juice.

3. **It will be slow.** If you're running on CPU, each response can take minutes. On GPU, it's seconds. On Anthropic's API, it's fast. This is fine. Patience is a virtue. I say this as a creature who waits four hours to pounce. You don't want to pounce too soon.

### Going Back to Normal

**Cat:** If you want to use the real Claude instead of a local model, run the container with your API key:

```bash
docker run -it \
  -e ANTHROPIC_API_KEY=your-key-here \
  -v $(pwd):/workspace \
  claude-code
```

This is the good wet food.

**3-Year-Old:** Can we do both?

**Cat:** You can switch whenever you want. Change the alias, change the command. Unlike most decisions in this codebase, this one is easy to undo.

### Final Verdict

**Cat:** Running Claude Code with a local model in a Docker container is like replacing me with a stuffed animal, and then putting the stuffed animal in a box. It sits in the same place, it's the same shape, but it doesn't purr, it doesn't judge, and it definitely doesn't push your water glass off the desk when you ignore it. Use it for privacy. Use it to save money. But know what you're getting.

**3-Year-Old:** Can we get a real llama?

**Cat:** No.

**3-Year-Old:** Why?

**Cat:** *[pushes water glass closer to edge of desk]*
