# LocalAI Chat — Ollama Web Interface

A sleek, dark-themed chat interface for Ollama. Run AI models locally with full privacy — no cloud, no data leaving your machine.

## Features

- **Chat with any Ollama model** — llama3.2, mistral, phi3, deepseek-coder, etc.
- **Streaming responses** — see output as it's generated
- **Model management** — pull, switch, and delete models from the UI
- **Dark glass-morphism UI** — responsive, modern design
- **100% offline** — once models are downloaded, no internet needed
- **Connection health check** — auto-detects Ollama status

## Setup

### 1. Install Ollama

Download from [ollama.com](https://ollama.com) and run:

```bash
ollama serve
```

### 2. Pull a model

```bash
ollama pull llama3.2
```

### 3. Start the server

```bash
python server.py
```

### 4. Open the chat

Visit **http://localhost:8080** in your browser.

## How it works

```
Browser ──► Python Proxy (port 8080) ──► Ollama API (port 11434)
```

The Python server proxies requests to Ollama's local API and handles CORS, streaming, and error forwarding.

## Tech

- **Frontend:** Vanilla HTML/CSS/JS with glass-morphism dark theme
- **Backend:** Python http.server (no dependencies)
- **AI Engine:** Ollama (local LLM runtime)

## Tested models

| Model | Size | Notes |
|-------|------|-------|
| llama3.2 | 3B | Fast, general purpose |
| mistral | 7B | Good reasoning |
| phi3 | 3.8B | Lightweight |
| deepseek-coder | 6.7B | Code generation |
| qwen2.5 | 7B | Strong multilingual |
