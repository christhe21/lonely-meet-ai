# Lonely Meet AI – Project Specification

**Version:** 0.1.1  
**Status:** Planning / Scaffolding  
**Last Updated:** 2026-07-24

## 1. Project Overview & Context

### Goal
Build a real-time, voice-to-voice AI agent that joins a Google Meet call as a headless participant. The agent activates **only when the user is alone** in the meeting, listens to the user’s speech (e.g., practicing a lecture or pitch), processes it through a configurable LLM persona, and responds by speaking back into the call via audio injection.

### Core Use Case
User joins a Google Meet, starts the bot, and practices a presentation alone. When alone for a threshold duration, the bot activates and role-plays a critical audience member (e.g., Gordon Ramsay, investor, professor) that asks probing questions or gives feedback in real time.

### Key Constraints
- No official Google Meet bot API → must use browser automation (Playwright/Puppeteer) or managed services (Recall.ai, Meeting Baas).
- Must detect “lonely” state via DOM scraping of participant count.
- Low-latency audio pipeline required for natural conversation feel.
- Audio must be injected as if coming from the bot’s microphone.
- **Must support both cloud and fully local LLMs** (Ollama, LM Studio, etc.).

### High-Level Value
- Practice presentations with realistic, persona-driven feedback.
- Extensible to other meeting platforms later.
- Educational / productivity tool for solo rehearsal.
- Privacy-friendly: can run the Brain entirely offline.

---

## 2. Architecture Components

| Component | Responsibility | Primary Tech | Notes |
|-----------|----------------|--------------|-------|
| **Joiner** | Launch headless browser, navigate to Meet link, click Join, stay in call | Playwright (Python or Node) | Managed alternative: Recall.ai / Meeting Baas |
| **Lonely Trigger / Participant Detector** | Continuously poll DOM for participant count; activate listening only when count == 1 for N seconds | Playwright page.evaluate / MutationObserver | Selector example: `.uGOf1d` (fragile – needs monitoring) |
| **Ears (Speech-to-Text)** | Capture audio stream or scrape live captions → real-time transcript | Deepgram / Gladia / Google Live Caption scrape | Prefer streaming STT for lower latency. Future: local Whisper |
| **Brain (LLM + Persona)** | Receive final transcript segments, generate persona-aligned response | **Local first**: Ollama / any OpenAI-compatible. Also OpenAI, Anthropic | See `docs/LOCAL_LLM_SETUP.md` |
| **Voice (TTS + Injection)** | Convert LLM text → audio, route audio into the browser’s virtual microphone | ElevenLabs / OpenAI TTS + VB-Cable / Web Audio API / virtual sink | Critical path for “speaking”. Future: local Piper/Coqui |
| **Orchestrator** | State machine coordinating the above; handles silence detection, turn-taking, activation/deactivation | Custom Python service | Central control loop |
| **Config & Persona Store** | Meeting link, persona prompts, thresholds, API keys, LLM provider | `.env` + YAML personas | Hot-reloadable personas |
| **Logging & Observability** | Transcript history, latency metrics, error tracking | Structured logs + optional dashboard | |

### Optional / Future Components
- Multi-persona switching mid-call
- Visual avatar / camera injection (beyond scope of v1)
- Recording of sessions for review
- Web dashboard for controlling the bot
- Fully offline stack (local Whisper STT + local TTS)

---

## 3. Overall Data / Control Flow

```
[User] ──joins──> Google Meet <──joins── [Headless Browser / Bot]
                         │
                         ▼
              [Participant Detector]
                         │
              (count == 1 for threshold?)
                         │ yes
                         ▼
              [Ears] ← audio / captions
                         │
                         ▼
              [STT] → live transcript segments
                         │
              (end of utterance / silence)
                         │
                         ▼
              [Brain] ← transcript + persona system prompt
                    │
                    ├── Local: Ollama / LM Studio / openai-compatible
                    └── Cloud: OpenAI / Anthropic
                         │
                         ▼
              [LLM] → response text
                         │
                         ▼
              [TTS] → audio buffer
                         │
                         ▼
              [Audio Injection] → virtual mic → Google Meet
                         │
                         ▼
              User hears the persona speaking
```

---

## 4. Key Sequences

### 4.1 Startup Sequence
1. User provides Meet link + persona config.
2. Orchestrator launches Playwright browser (or calls managed API).
3. Browser navigates to link, dismisses pre-join screens, joins with mic/camera off or virtual.
4. Detector starts polling participant count.
5. Bot remains silent until lonely condition met.

### 4.2 Activation Sequence (Lonely Mode)
1. Detector observes participant count == 1 for `LONELY_THRESHOLD_SECONDS`.
2. Orchestrator flips state to `LISTENING`.
3. Ears begin streaming / caption capture.
4. Visual indicator (optional) or log entry “Activated – waiting for speech”.

### 4.3 Conversation Turn Sequence
1. User speaks → Ears capture audio.
2. STT produces incremental transcripts.
3. Silence detection (VAD or timeout) finalizes utterance.
4. Final transcript sent to Brain with persona system prompt + recent history.
5. LLM returns response (streaming preferred).
6. TTS synthesizes audio (streaming or full).
7. Audio is pushed into virtual microphone device attached to the Playwright browser context.
8. Google Meet shows bot’s mic active and plays audio to user.
9. After TTS finishes, return to listening (or brief cooldown).

### 4.4 Deactivation Sequence
1. Participant count > 1 detected.
2. Orchestrator immediately stops listening / TTS, mutes virtual mic.
3. State → `IDLE` / `STANDING_BY`.

### 4.5 Shutdown
1. User signals stop or closes browser context.
2. Clean teardown of audio devices, browser, connections.

---

## 5. Required Diagrams (to be created)

Place diagrams in `/docs/diagrams/`:

- [ ] **Architecture Overview** (component boxes + data arrows) – Mermaid or draw.io
- [ ] **Sequence Diagram: Full Conversation Turn**
- [ ] **State Machine** of the Orchestrator (IDLE → LISTENING → THINKING → SPEAKING → …)
- [ ] **Audio Pipeline Detail** (browser → virtual cable → TTS service → injection)
- [ ] **Deployment / Runtime Topology** (local vs cloud bot host)

---

## 6. Technology Stack Recommendations

**Core Runtime**
- Language: Python 3.11+
- Browser automation: Playwright
- Async: asyncio / Playwright async API

**AI Services – LLM (Brain)**  
**First-class local support:**
- Ollama (recommended) → `http://localhost:11434/v1`
- LM Studio, vLLM, llama.cpp server, any OpenAI-compatible endpoint

Cloud still fully supported:
- OpenAI (GPT-4o, etc.)
- Anthropic (Claude 3.5 / 4)

See **`docs/LOCAL_LLM_SETUP.md`** for exact setup steps.

**STT (Ears)**
- Primary: Deepgram Nova-2 (or Gladia)
- Future local: faster-whisper / whisper.cpp

**TTS (Voice)**
- Primary: ElevenLabs or OpenAI TTS
- Future local: Piper, Coqui, XTTS

**Audio Infrastructure**
- Virtual audio: VB-Audio Virtual Cable (Windows) / BlackHole (macOS) / PulseAudio null sink (Linux)
- Alternative: pure Web Audio API + MediaStream injection if possible inside Playwright

**Managed Alternatives (to reduce fragility)**
- Recall.ai or Meeting Baas for the “Joiner + audio websocket” layer

**Config**
- `.env` (see `.env.example`)
- YAML persona definitions in `docs/personas/`

---

## 7. Repository Structure (Scaffold)

```
lonely-meet-ai/
├── README.md
├── SPEC.md                     ← this file
├── docs/
│   ├── LOCAL_LLM_SETUP.md      ← how to run with Ollama / LM Studio
│   ├── diagrams/               ← architecture & sequence diagrams
│   └── personas/               ← example persona prompts
├── src/
│   ├── __init__.py
│   ├── main.py                 ← entrypoint / CLI
│   ├── orchestrator.py         ← state machine
│   ├── joiner/
│   │   ├── __init__.py
│   │   └── playwright_joiner.py
│   ├── detector/
│   │   ├── __init__.py
│   │   └── participant_detector.py
│   ├── ears/
│   │   ├── __init__.py
│   │   ├── stt_deepgram.py
│   │   └── caption_scraper.py
│   ├── brain/
│   │   ├── __init__.py
│   │   └── llm_persona.py      ← multi-provider (local + cloud)
│   ├── voice/
│   │   ├── __init__.py
│   │   ├── tts_elevenlabs.py
│   │   └── audio_injector.py
│   └── config/
│       ├── __init__.py
│       └── settings.py         ← LLM_PROVIDER, LLM_BASE_URL, etc.
├── tests/
│   └── ...
├── scripts/
│   └── setup_virtual_audio.md
├── .env.example
├── requirements.txt
└── docker/                     ← optional later
```

---

## 8. Non-Goals (v1)

- Multi-party conversations (bot should stay silent when others join)
- Camera / visual avatar
- Persistent memory across meetings (beyond simple history window)
- Mobile support
- Production multi-tenant SaaS

---

## 9. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Google Meet DOM changes break selectors | Prefer managed services; keep selector map versioned; monitoring alerts |
| High latency ruins conversation feel | Stream STT + LLM + TTS; measure end-to-end latency budget (<2–3 s ideal). Prefer small local models |
| Audio injection reliability across OS | Document platform-specific virtual audio setup; provide scripts |
| Cost of continuous STT/TTS | Only activate when lonely; use silence detection aggressively; local LLM eliminates LLM cost |
| Legal / ToS | Personal use / practice tool; do not claim official integration |

---

## 10. Next Immediate Steps

1. ✅ Scaffold the repository structure + this SPEC + local LLM support.
2. Implement minimal Playwright joiner that can enter a Meet and stay connected.
3. Implement participant count polling + lonely state machine.
4. Add Deepgram streaming STT path (or caption scraper for quick testing).
5. Wire `LLMPersona` (already supports local) and print responses (no TTS yet).
6. Solve audio injection on one platform (start with Linux or macOS).
7. End-to-end demo with a fixed persona + local Ollama model.

---

*This specification is living. Update it as architectural decisions solidify.*
