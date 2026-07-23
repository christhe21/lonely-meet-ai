# Lonely Meet AI

Real-time **voice-to-voice AI agent** for Google Meet.

A headless bot joins your meeting, stays silent while others are present, and activates **only when you are alone**. It listens to your speech (lecture / pitch practice), runs it through a configurable LLM persona, and speaks back into the call via TTS audio injection.

> Example persona: Gordon Ramsay grilling you about your presentation.

## Status

**Scaffolding / Spec complete.** Implementation not started.

See **[SPEC.md](./SPEC.md)** for the full architecture, components, sequences, risks, and planned structure.

## Quick Links

| Document | Description |
|----------|-------------|
| [SPEC.md](./SPEC.md) | Full project specification |
| [docs/personas/](./docs/personas/) | Example system prompts |
| [docs/diagrams/](./docs/diagrams/) | Architecture & sequence diagrams (to be added) |
| [.env.example](./.env.example) | Required environment variables |

## High-Level Architecture

1. **Joiner** – Playwright (or managed service) joins the Meet as a headless participant  
2. **Lonely Trigger** – DOM participant-count detector  
3. **Ears** – Streaming STT (Deepgram) or caption scrape  
4. **Brain** – LLM + persona system prompt  
5. **Voice** – TTS + virtual microphone injection  
6. **Orchestrator** – State machine coordinating everything

## Planned Stack

- Playwright
- Deepgram (STT)
- OpenAI / Claude / Gemini (LLM)
- ElevenLabs (TTS)
- Virtual audio cable / Web Audio injection

## Getting Started (once implemented)

```bash
cp .env.example .env
# fill keys
pip install -r requirements.txt
playwright install
python -m src.main --meet-url "https://meet.google.com/..." --persona gordon-ramsay
```

## License

MIT (planned)
