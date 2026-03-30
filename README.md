---
title: Aria AI Chatbot
emoji: 🤖
colorFrom: violet
colorTo: indigo
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# Aria — AI Chatbot

A professional, portfolio-grade AI chatbot built with **Groq API** (Llama 3.3 70B) and **Gradio**.  
Fast responses, full conversation memory, and a clean user interface — ready to deploy on Hugging Face Spaces.

---

## Features

- Natural, friendly conversations with Aria (your AI assistant)
- Full conversation memory — remembers everything said in the session
- Retry last message with one click
- 6 built-in example prompts to get started quickly
- Clean output — no markdown asterisks or hash symbols
- Powered by llama-3.3-70b-versatile via Groq (one of the fastest LLM APIs available)
- Production-ready code with proper error handling

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Llama 3.3 70B Versatile |
| API | Groq Cloud API |
| UI | Gradio 4.x (ChatInterface) |
| Config | python-dotenv |
| Deploy | Hugging Face Spaces |

---

## Local Setup (VS Code, No Virtualenv)

### Step 1 — Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/aria-chatbot.git
cd aria-chatbot
```

### Step 2 — Install dependencies

```bash
pip install groq==0.9.0 gradio==4.44.0 python-dotenv==1.0.1
```

### Step 3 — Create your .env file

```bash
cp .env.example .env
```

Open `.env` and paste your Groq API key:

```
GROQ_API_KEY=your_actual_key_here
```

Get your free key at: https://console.groq.com

### Step 4 — Run the app

```bash
python app.py
```

Open your browser at: http://localhost:7860

---

## GitHub Upload

```bash
git init
git add .
git commit -m "Initial commit: Aria AI Chatbot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/aria-chatbot.git
git push -u origin main
```

---

## Project Structure

```
aria-chatbot/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .env                # Your actual API key (never commit this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## License

MIT License — free to use, modify, and share.
