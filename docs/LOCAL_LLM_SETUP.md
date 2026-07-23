# Local LLM Setup Guide

You can run the entire **Brain** component fully offline using a local LLM.
The recommended path is **Ollama**. Any OpenAI-compatible server (LM Studio, vLLM, llama.cpp, etc.) also works.

---

## Option 1 – Ollama (Recommended)

### 1. Install Ollama

```bash
# Linux / macOS
curl -fsSL https://ollama.com/install.sh | sh

# Or download from https://ollama.com
```

### 2. Pull a model

Pick a fast model for real-time conversation (lower latency is better):

```bash
# Good balance of quality + speed
ollama pull llama3.1

# Or smaller / faster options
ollama pull llama3.2
ollama pull qwen2.5:7b
ollama pull phi3
ollama pull gemma2:9b
```

### 3. Verify it is running

```bash
ollama list
curl http://localhost:11434/api/tags
```

Ollama exposes an **OpenAI-compatible** endpoint at:

```
http://localhost:11434/v1
```

### 4. Configure the project

In your `.env`:

```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.1
LLM_BASE_URL=http://localhost:11434/v1
# No API key needed for Ollama
```

That’s it. The `LLMPersona` class will automatically use the local endpoint.

---

## Option 2 – LM Studio

1. Download [LM Studio](https://lmstudio.ai)
2. Load any GGUF model
3. Start the local server (usually port 1234)
4. Set in `.env`:

```env
LLM_PROVIDER=openai_compatible
LLM_MODEL=your-model-name-in-lm-studio
LLM_BASE_URL=http://localhost:1234/v1
```

---

## Option 3 – llama.cpp / vLLM / other OpenAI-compatible

Point `LLM_BASE_URL` at whatever OpenAI-compatible `/v1` endpoint your server exposes and set `LLM_PROVIDER=openai_compatible`.

---

## Option 4 – Cloud (still supported)

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
OPENAI_API_KEY=sk-...

# or
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Latency Tips for Real-Time Conversation

- Prefer 7B–8B or smaller quantized models for lower latency.
- Keep `LLM_MAX_TOKENS` low (128–256) – the persona should give short, punchy replies.
- Use streaming later (not yet implemented in the scaffold) for even better feel.
- GPU acceleration (CUDA / Metal / ROCm) makes a big difference.

---

## Full Local Stack (future)

Right now only the **Brain** is local-ready. For a completely offline system you would also replace:

| Component | Cloud | Local alternative |
|-----------|-------|-------------------|
| STT (Ears) | Deepgram | Whisper (faster-whisper / whisper.cpp) |
| TTS (Voice) | ElevenLabs | Piper, Coqui TTS, Bark, or XTTS |

These can be added later. The architecture already isolates each component so swapping is straightforward.
