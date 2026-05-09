# JERRY — Personal AI Assistant

**Jerry** is a Jarvis-level, local, and private AI assistant built for Windows. It combines voice interaction, long-term memory, and autonomous PC control—all running entirely on your local machine with zero data sharing.

---

## Brains (Local LLMs)

Jerry is powered by three specialized local LLM brains, switchable on-the-fly:

- **Phi-4 Mini**: Fast, efficient, and surprisingly capable for general tasks.
- **Qwen 2.5 (Coder)**: Optimized for technical tasks, scripting, and logical operations.
- **Qwen 3.5**: The latest powerhouse for complex reasoning and bilingual fluency (mapped to Qwen3:4b).

*All models run via **Ollama**, ensuring 100% privacy and offline operation.*

---

## Key Features

- **Voice First**: Activation via "Hey Jerry" (Wake word) and high-quality voice synthesis (Piper TTS).
- **Bilingual Fluency**: Seamlessly switches between **British English** and **Hindi**.
- **Persistent Memory**: Uses **ChromaDB** to remember past conversations, your preferences, and specific details across sessions.
- **Autonomous PC Control**:
  - Open/Close applications (Chrome, VS Code, Spotify, etc.)
  - File system management (Read, Write, Move, Delete)
  - System monitoring (CPU, RAM, Disk, Battery)
  - Browser automation and web searching
  - Screenshot and Clipboard handling
- **Privacy Controlled**: Sensitive actions (like file deletion or script execution) require your confirmation unless **Auto-mode** is enabled.
- **Dual Interface**:
  - **Terminal UI**: Lightweight, classic interaction with wake-word support.
  - **Streamlit Dashboard**: Modern, interactive web UI for a cleaner chat experience.

---

## Tech Stack

- **Core Orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph) + [LangChain](https://github.com/langchain-ai/langchain)
- **Brains**: Ollama (Phi4, Qwen 2.5, Qwen 3.5)
- **Memory**: ChromaDB (Vector Store)
- **Voice STT**: Faster-Whisper (Local Speech-to-Text)
- **Voice TTS**: Piper TTS (Local Text-to-Speech) / pyttsx3 fallback
- **Wake Word**: OpenWakeWord ("Hey Jerry")
- **Search**: DuckDuckGo (ddgs) + Google Fallback

---

## Setup & Installation

### Prerequisites

- [Ollama](https://ollama.com/) installed and running.
- Python 3.10+ installed.

### Installation & Setup

1. **Clone the repository** to your local machine.
2. **Run the setup script**:

   ```cmd
   setup.bat
   ```

   *This script will:*
   - Verify your Python installation.
   - Install all required libraries from `requirements.txt`.
   - **Automatically pull** the necessary Ollama models (`phi4-mini`, `qwen3:4b`, `qwen2.5-coder:7b`).
   - Initialize a local Git repository for privacy-focused version control.

3. **(Optional) Piper TTS**: For the best voice experience, place `piper.exe` and `.onnx` voice models in `data/piper/`. If not found, Jerry will fallback to the default Windows `pyttsx3` voice.

---

## How to Use

### Starting Jerry

```cmd
python main.py
```

Upon startup, Jerry activates:

- **Terminal UI**: Active wake-word listening ("Hey Jerry").
- **Streamlit Web UI**: Accessible at `http://localhost:8501`.

### Commands

| Command | Result |
|---|---|
| `/status` | View current brain, mode, and memory stats. |
| `/switch` | Toggle between LLM brains (Phi4 / Qwen 2.5 / Qwen 3.5). |
| `/auto` | Toggle Auto-mode (skip confirmation for sensitive tasks). |
| `/voice` | Switch between male and female voice profiles. |
| `/clear` | Clear conversation history. |
| `/quit` | Shut down Jerry. |

---

## Privacy & Safety

Jerry follows a strict **Confirmation First** policy. For any action that modifies your system (deleting files, running scripts, etc.), Jerry will ask: *"Shall I proceed?"*. You can grant permission for that specific action or say *"handle it yourself"* to enable **Auto-mode** for the session.

---
