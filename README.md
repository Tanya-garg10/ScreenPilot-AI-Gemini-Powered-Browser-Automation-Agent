# ScreenPilot AI

ScreenPilot AI is a Gemini-powered browser automation agent that understands natural language commands and performs web tasks automatically.

## Features

- Natural language browser automation
- Gemini-based intent detection
- Devpost project search
- Website navigation
- Gmail compose flow
- Screenshot capture and preview
- FastAPI backend
- Playwright browser automation

## How It Works

1. User enters a text or voice command
2. Gemini analyzes the command and creates an action plan
3. Playwright executes the action in the browser
4. The app captures the final screen and returns the result

## Example Commands

- `open github`
- `AI hackathons on Devpost`
- `python internships`
- `write email to HR about internship opportunity`

## Tech Stack

- Python
- FastAPI
- Playwright
- Gemini API
- HTML
- JavaScript

## Project Structure

```bash
screenpilot-ai/
│
├── backend/
│   ├── main.py
│   ├── automation.py
│   ├── gemini_agent.py
│   └── screenshots/
│
├── frontend/
│   └── index.html
│
└── README.md
````

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/screenpilot-ai.git
cd screenpilot-ai/backend
```

### 2. Install dependencies

```bash
py -m pip install fastapi uvicorn playwright google-genai
py -m playwright install
```

### 3. Add Gemini API key

Set your API key before running:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

### 4. Start backend

```bash
py -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

### 5. Open frontend

Open `frontend/index.html` in the browser.

## Demo Flow

1. Open GitHub using natural language
2. Search AI hackathons on Devpost
3. Open Gmail compose using an email command
4. Show screenshot-based output

## Challenges

* Automation detection on some websites
* Converting general commands into structured browser actions
* Building a reliable browser automation workflow

## Future Improvements

* Voice-first interaction
* Multi-step task automation
* Smarter screen understanding
* Cross-application automation

## License

This project was built for the Gemini Live Agent Challenge.
