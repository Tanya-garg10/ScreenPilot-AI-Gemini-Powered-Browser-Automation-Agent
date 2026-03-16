from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from automation import run_browser_task
from gemini_agent import plan_action

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

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

app.mount("/screenshots", StaticFiles(directory=str(SCREENSHOTS_DIR)), name="screenshots")


@app.get("/")
def home():
    return {"message": "ScreenPilot AI backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/plan")
def plan(command: str = Query(..., description="User command")):
    return plan_action(command)


@app.get("/run")
def run_agent(command: str = Query(..., description="User command")):
    return {
        "status": "success",
        "command": command,
        "actions": [
            {"step": 1, "action": "analyze_command"},
            {"step": 2, "action": "generate_plan"},
            {"step": 3, "action": "execute_browser"}
        ]
    }


@app.get("/run-browser")
def run_browser(command: str = Query(..., description="Browser task")):
    result = run_browser_task(command)

    if result.get("status") == "success" and result.get("screenshot"):
        file_name = Path(result["screenshot"]).name
        result["screenshot_url"] = (
            f"https://screenpilot-ai-gemini-powered-browser-9kk0.onrender.com/screenshots/{file_name}"
        )

    return result
