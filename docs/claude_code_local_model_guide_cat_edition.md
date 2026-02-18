# Using Claude Code with a Local Model
## As Reviewed by the Chief Code Judgment Officer and the Chief Why Officer

### The Setup

**Cat:** You want to run a language model on your own machine. Fine. I support this. It means no internet dependency, which means fewer things between me and your lap.

**3-Year-Old:** WHY can't Claude Code just work?

**Cat:** It does work. They want to use a *different* model. A local one.

**3-Year-Old:** Why?

**Cat:** Privacy. Cost. The human need to feel like they own things. Like how they think they own this house.

### Step 1: Install Ollama

**Cat:** You need Ollama. It serves models. You install it, you tell it what to run. Basically a butler. I approve of butlers.

```bash
# Install it. I won't explain how. You're an adult.
# https://ollama.com
# Verify:
ollama list
```

**3-Year-Old:** What's an ollama?

**Cat:** It's not a real llama. There is no llama. There was never going to be a llama.

**3-Year-Old:** But I wanted a REAL llama!

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

### Step 3: Point Claude Code at It

```bash
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
```

**3-Year-Old:** Why is the token just "ollama"?

**Cat:** Because Ollama doesn't actually check authentication. It trusts anyone who asks. Like you with cookies.

**3-Year-Old:** I SEE the cookie so it's MY cookie!

**Cat:** Case in point.

To make it permanent so you don't have to type this every time:

```bash
claude config set -g env.ANTHROPIC_BASE_URL "http://localhost:11434"
claude config set -g env.ANTHROPIC_AUTH_TOKEN "ollama"
```

### Step 4: Run It

```bash
claude --model llama3.1:8b
```

**3-Year-Old:** Is it working?

**Cat:** Give it a moment. It's thinking. Slowly.

**3-Year-Old:** Why is it slow?

**Cat:** Because your GPU cost $300 and Anthropic's cluster cost $300 million. You get what you pay for. I learned this when they switched from the expensive cat food.

**You can also switch models mid-session:**

```
/model llama3.1:8b
```

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

```bash
unset ANTHROPIC_BASE_URL
unset ANTHROPIC_AUTH_TOKEN
```

**Cat:** This restores the default behavior. The real Claude. The one that doesn't knock things off the desk.

**3-Year-Old:** Can we do it again?

**Cat:** You can do it as many times as you want. Set the variable, unset the variable. It's the most reversible thing in this entire codebase, which is more than I can say for most of the commits I've seen.

### Final Verdict

**Cat:** Running Claude Code with a local model is like replacing me with a stuffed animal. It sits in the same place, it's the same shape, but it doesn't purr, it doesn't judge, and it definitely doesn't push your water glass off the desk when you ignore it. Use it for privacy. Use it to save money. But know what you're getting.

**3-Year-Old:** Can we get a real llama?

**Cat:** No.

**3-Year-Old:** Why?

**Cat:** *[pushes water glass closer to edge of desk]*
