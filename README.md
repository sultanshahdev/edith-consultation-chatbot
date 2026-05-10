# 🎓 Consultation Chatbot (GenAI)

> A production-ready, domain-specific AI consultation chatbot powered by the **Google Gemini GenAI API**, built with a modular backend architecture and deployed on **Streamlit Community Cloud**.

[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://consultation-chatbot.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Gemini API](https://img.shields.io/badge/Gemini-3.1--flash--lite-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Live App](#-live-app)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Module Breakdown](#-module-breakdown)
- [Prompt Engineering Design](#-prompt-engineering-design)
- [Conversation Memory System](#-conversation-memory-system)
- [Tech Stack](#-tech-stack)
- [Local Setup & Installation](#-local-setup--installation)
- [Deployment](#-deployment)
- [Example Queries](#-example-queries)
- [Error Handling & Logging](#-error-handling--logging)
- [Future Improvements](#-future-improvements)

---

## 🧠 Project Overview

The **Consultation Chatbot** is a production-grade AI application that provides structured, actionable consultation services to users. It leverages Google's **Gemini 3.1 Flash Lite** model for fast, intelligent responses and is built following real-world AI engineering principles.

The project goes beyond a basic chatbot prototype by implementing:

- A **layered, modular backend** with clear separation of concerns
- **Advanced prompt engineering** using a structured system prompt with enforced response formats
- **Session-based multi-turn conversation memory** to maintain context across interactions
- **Secure API key management** using Streamlit Secrets
- **Centralized logging and custom exception handling**
- **Cloud deployment** on Streamlit Community Cloud

The chatbot is designed to help users explore various topics, assess their needs, understand solutions, and evaluate options — all through a natural, conversational interface.

---

## 🚀 Live App

🔗 [https://consult-edith.streamlit.app](https://consult-edith.streamlit.app)

---

## ✨ Features

### 🤖 AI-Powered Consultation
Integrated with the **Google Gemini 2.5 Flash Lite** model to generate fast, high-quality, domain-specific consultation responses. The model is accessed via the `google-genai` Python SDK.

### 📋 Structured Response Format
Every response from the chatbot follows a consistent, prompt-enforced structure:
1. **Insight** — context and understanding
2. **Key Recommendations** — actionable recommendations
3. **Implementation Path** — step-by-step roadmap or resource guidance
4. **Potential Challenges** — honest evaluation of challenges or considerations
5. **Next Actions** — immediate, actionable steps the user can take

### 🧩 Multi-Turn Conversation Memory
The chatbot maintains a **sliding window of the last 5 conversation turns** as context. Each new prompt includes this history, allowing the model to understand evolving conversations and respond to follow-up questions coherently.

### 🛠️ Modular Backend Architecture
The codebase is structured into dedicated, single-responsibility modules for API handling, prompt construction, memory management, response processing, logging, and exception handling — following clean architecture principles.

### 🔐 Secure API Key Management
The Gemini API key is never hardcoded. It is stored and accessed securely via **Streamlit Secrets** (`st.secrets`), making the app safe for cloud deployment.

### 📝 Centralized Logging
All API calls, errors, and significant application events are logged using Python's built-in `logging` module with a consistent timestamp format, enabling effective debugging and monitoring.

### ⚠️ Custom Exception Handling
A dedicated `GeminiAPIException` class is defined for domain-specific error management, with graceful fallback messages displayed to the user on API failures (e.g., quota exhaustion).

### 💬 Interactive Streamlit Chat UI
The UI uses Streamlit's native `st.chat_message` and `st.chat_input` components to deliver a clean, modern chat interface with real-time responses, conversation history, and loading indicators.

---

## 🏗️ System Architecture

The application follows a **unidirectional, layered pipeline architecture**:

```
┌────────────────────────────────────────────┐
│                   User                     │
└────────────────────┬───────────────────────┘
                     │ User Input
                     ▼
┌────────────────────────────────────────────┐
│           Streamlit UI  (app.py)           │
│  - Chat input / output rendering           │
│  - Session state & message history         │
└────────────────────┬───────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────┐
│        Conversation Memory Manager         │
│  (core/memory_manager.py)                  │
│  - Retrieves last N turns as context       │
└────────────────────┬───────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────┐
│           Prompt Manager                   │
│  (core/prompt_manager.py)                  │
│  - Injects system prompt + context         │
│  - Constructs final prompt string          │
└────────────────────┬───────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────┐
│           Gemini API Client                │
│  (core/gemini_client.py)                   │
│  - Authenticates with Gemini API           │
│  - Sends prompt, receives raw response     │
└────────────────────┬───────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────┐
│           Response Handler                 │
│  (core/response_handler.py)                │
│  - Cleans, validates, formats response     │
└────────────────────┬───────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────┐
│         UI Rendering + Memory Update       │
│  - Displays final response to user         │
│  - Updates memory with this turn           │
└────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Consultation_Chatbot_GenAI/
│
├── app.py                    # Main Streamlit application entry point
├── requirements.txt          # Python dependencies
│
├── core/                     # Core backend logic
│   ├── gemini_client.py      # Gemini API integration
│   ├── prompt_manager.py     # Prompt engineering & construction
│   ├── memory_manager.py     # Conversation memory management
│   └── response_handler.py   # Response processing & formatting
│
├── utils/                    # Utility modules
│   ├── logger.py             # Centralized logging configuration
│   └── exceptions.py         # Custom exception definitions
│
├── config/                   # Application configuration
│   └── settings.py           # App-level constants and settings
│
└── assets/                   # UI assets
    └── ui_styles.py          # Custom CSS for chat interface styling
```

---

## 🔍 Module Breakdown

### `app.py` — Application Entry Point

The main Streamlit application that orchestrates the entire pipeline. It is responsible for:

- Configuring the Streamlit page (title, icon, layout)
- Initializing and persisting `ConversationMemory` and message history across reruns using `st.session_state`
- Instantiating backend modules: `GeminiClient`, `PromptManager`, `ResponseHandler`
- Rendering all previous messages from session state on each page load
- Accepting user input via `st.chat_input` and coordinating the full request-response cycle
- Updating conversation memory and message history after each response

**Key design decision:** `st.session_state` is used for both the raw message list (for UI rendering) and the `ConversationMemory` object (for prompt construction), keeping display logic and API context logic independent.

---

### `core/gemini_client.py` — Gemini API Client

Handles all communication with the Google Gemini GenAI API.

- Retrieves the API key securely from `st.secrets`
- Raises a `ValueError` immediately on initialization if the key is missing, preventing silent failures
- Uses the `google-genai` Python SDK (`genai.Client`) to instantiate the API client
- Sends prompts to the **`gemini-2.5-flash-lite`** model via `client.models.generate_content()`
- Catches all API exceptions, logs the error, and returns a user-friendly fallback message

```python
# Model used
self.model_name = "gemini-2.5-flash-lite"
```

---

### `core/prompt_manager.py` — Prompt Engineering Layer

Constructs the final prompt sent to the Gemini model by combining a structured system prompt, conversation context, and the user's current query.

**System Prompt Design:**
```
You are a professional Consultation AI.

RULES:
- Provide structured, realistic consultation guidance.
- Avoid generic motivation or vague advice.
- Base suggestions on available information and best practices.
- If information is missing, ask clarifying questions.
- Never fabricate guarantees or unrealistic promises.
- Always provide actionable next steps.

RESPONSE FORMAT:
1. Insight
2. Key Recommendations
3. Implementation Path
4. Potential Challenges
5. Next Actions
``` 

The `build_prompt()` method combines this system instruction with:
- The conversation context string (from `ConversationMemory`)
- The current user query

This three-part structure (system + context + query) is a standard **few-shot / role-prompting** pattern that significantly improves response quality and consistency.

---

### `core/memory_manager.py` — Conversation Memory

Implements a simple but effective **sliding window memory** system.

- Stores each turn as a formatted string: `"User: <input>\nAdvisor: <response>"`
- Enforces a configurable `max_turns` limit (default: `5`) to prevent prompt bloat and token overflow
- Removes the oldest turn when the limit is exceeded (`history.pop(0)`)
- Exposes `get_context()` which joins all stored turns into a single string, ready to be injected into the prompt

```python
# Memory window size (configurable via config/settings.py)
MAX_MEMORY_TURNS = 5
```

---

### `core/response_handler.py` — Response Processor

A lightweight processing layer that validates and cleans the model's raw output before displaying it to the user.

- Returns a fallback message if the API response is empty or `None`
- Strips leading/trailing whitespace from the response text
- Acts as the final quality gate before UI rendering — designed to be extended with additional formatting or post-processing logic

---

### `utils/logger.py` — Centralized Logger

Configures a Python `logging` instance used throughout the application.

```python
# Log format
"%(asctime)s | %(levelname)s | %(message)s"
```

- Log level is set to `INFO`, capturing standard application events and errors
- The logger is named `"ConsultationChatbotGenAI"` for easy filtering in log outputs
- Used primarily in `gemini_client.py` to log API errors

---

### `utils/exceptions.py` — Custom Exceptions

Defines application-specific exception classes for structured error management.

```python
class GeminiAPIException(Exception):
    pass
```

`GeminiAPIException` provides a semantic wrapper around Gemini API failures, enabling future `try/except` blocks to differentiate between API errors and other runtime exceptions with precision.

---

### `config/settings.py` — Application Settings

Centralizes application-level constants to avoid magic numbers scattered across the codebase.

```python
APP_NAME = "Consultation Chatbot GenAI"
MAX_MEMORY_TURNS = 5
```

This configuration-driven design makes adjustments (e.g., changing memory window size) a single-point change.

---

### `assets/ui_styles.py` — UI Styling

Contains custom CSS injected into the Streamlit interface to enhance the visual appearance of chat messages. Designed to be extended with richer styling as needed.

---

## 🧪 Prompt Engineering Design

The prompt follows a **role + rules + format + context + query** pattern, which is one of the most reliable structures for instruction-following language models.

| Prompt Section        | Purpose                                                                 |
|-----------------------|---------|
| **Role Definition**   | Establishes the model's persona as a "professional Consultation AI"   |
| **Rules**             | Constrains model behavior — prevents hallucination, vague advice, etc.  |
| **Response Format**   | Enforces a structured 5-section output for every response               |
| **Conversation Context** | Provides the sliding window of past turns for continuity             |
| **User Query**        | The current question from the user                                      |

This design ensures responses are **consistent, structured, and domain-constrained** regardless of how the user phrases their question.

---

## 🧩 Conversation Memory System

The memory system uses a **FIFO (First-In, First-Out) sliding window** approach:

```
Turn 1: User: "I want to be a data scientist"   → stored
Turn 2: User: "What Python skills do I need?"   → stored, references Turn 1
Turn 3: User: "What about SQL?"                 → stored, references Turns 1–2
...
Turn 6: new turn arrives                        → Turn 1 is dropped (max_turns=5)
```

This approach:
- Keeps prompt length bounded to prevent excessive token usage
- Maintains recent context for coherent follow-up conversations
- Is reset per session (Streamlit re-initializes `st.session_state` on new browser sessions)

---

## 🛠️ Tech Stack

| Component        | Technology                          |
|------------------|-------------------------------------|
| Language         | Python 3.10+                        |
| UI Framework     | Streamlit                           |
| AI Model         | Google Gemini 2.5 Flash Lite        |
| Gemini SDK       | `google-genai`                      |
| Logging          | Python `logging` (stdlib)           |
| Secret Management| Streamlit Secrets (`st.secrets`)    |
| Deployment       | Streamlit Community Cloud           |

---

## ⚙️ Local Setup & Installation

### Prerequisites

- Python 3.10 or higher
- A valid [Google Gemini API Key](https://aistudio.google.com/app/apikey)
- Git

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Avik-Das-567/Consultation_Chatbot_GenAI.git
cd Consultation_Chatbot_GenAI
```

### Step 2 — Create and Activate a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS/Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` contents:**
```
streamlit
google-genai
```

### Step 4 — Configure the Gemini API Key

Create the Streamlit secrets directory and file:

```bash
mkdir .streamlit
```

Create the file `.streamlit/secrets.toml` and add:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

> ⚠️ **Never commit `.streamlit/secrets.toml` to version control.** Add it to your `.gitignore`.

```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

### Step 5 — Run the Application

```bash
streamlit run app.py
```

### Step 6 — Open in Browser

Streamlit will automatically open the app. If it doesn't, visit:

```
http://localhost:8501
```

---

## ☁️ Deployment

This project is deployed on **Streamlit Community Cloud** — a free, managed hosting platform for Streamlit apps connected to GitHub.

### Deployment Steps

1. Push the project to a public GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **"New app"** and select your repository, branch (`main`), and entry point (`app.py`)
4. Under **"Advanced settings"**, add your secret:
   ```
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
5. Click **"Deploy"** — the app will be live within a few minutes

**Live URL:** [https://consultation-chatbot.streamlit.app](https://consultation-chatbot.streamlit.app)

---

## 💬 Example Queries

The chatbot is designed to handle a wide range of consultation queries. Here are some examples:

| Query | What to Expect |
|-------|----------------|
| *"What should I do about...?"* | Structured analysis and recommendations |
| *"How can I approach this problem?"* | Step-by-step guidance and alternative solutions |
| *"What are the pros and cons of...?"* | Balanced evaluation of options |
| *"What's the best way to...?"* | Best practices and recommendations |
| *"What should I consider before...?"* | Key factors and decision-making framework |
| *"I'm considering... what advice do you have?"* | Personalized guidance based on specific situation |

---

## 🚨 Error Handling & Logging

### API Error Handling

The `GeminiClient` wraps all API calls in a `try/except` block. If the API call fails (e.g., due to quota exhaustion, network errors, or invalid responses), the error is:
1. Logged at `ERROR` level with the exception message
2. Caught gracefully — the user sees a friendly fallback message instead of a crash:

```
⚠️ Daily API quota reached or model unavailable.
```

### Missing API Key

If `GEMINI_API_KEY` is not found in `st.secrets`, `GeminiClient.__init__()` raises a `ValueError` immediately. The `app.py` catches this and displays:

```
❌ Gemini API Key not found. Please configure Streamlit Secrets.
```

The app then calls `st.stop()` to halt execution cleanly.

### Empty Responses

The `ResponseHandler` checks for empty or `None` model outputs and returns:

```
⚠️ No response generated.
```

### Log Format

All logs follow this format for easy parsing:

```
2026-04-09 14:32:01,452 | ERROR | Gemini API Error: 429 Resource has been exhausted
```

---

## 🔮 Future Improvements

- **RAG Integration** — connect the chatbot to a vector database (e.g., Pinecone, ChromaDB) populated with consultation resources and knowledge bases for grounded, factual responses
- **Persistent Memory** — replace session-based memory with a database-backed store (e.g., SQLite, Redis) to persist conversations across sessions
- **User Authentication** — add login functionality to save user-specific conversation history
- **Streaming Responses** — use the Gemini streaming API with `st.write_stream()` for a more dynamic typing effect
- **Feedback Loop** — add thumbs up/down buttons on responses to collect user feedback for future prompt tuning
- **Export Conversation** — allow users to download their consultation session as a PDF or text file
- **Multi-language Support** — expand the system prompt to handle queries in multiple languages

---

## 👤 Author

**Sultan Shah** - 
[github](https:www.github.com/sultanshahdev)

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
