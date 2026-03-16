from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ScreenPilot AI Backend",
    description="Backend API for ScreenPilot AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "ScreenPilot AI backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/run")
def run_agent(command: str = Query(..., description="User command")):
    return {
        "status": "success",
        "command": command,
        "actions": [
            {"action": "click", "target": "search box"},
            {"action": "type", "text": command},
            {"action": "keypress", "key": "Enter"}
        ]
    }

@app.get("/run-browser")
def run_browser(command: str = Query(..., description="Browser task")):
    return {
        "status": "success",
        "message": f"Browser automation placeholder for: {command}"
    }