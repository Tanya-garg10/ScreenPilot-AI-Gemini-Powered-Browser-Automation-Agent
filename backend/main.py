from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from automation import run_browser_task
from gemini_agent import plan_action
import os

# Create screenshots folder if it doesn't exist
os.makedirs("screenshots", exist_ok=True)

app = FastAPI(
    title="ScreenPilot AI Backend",
    description="Backend API for ScreenPilot AI",
    version="1.0.0"
)

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve screenshots as static files
app.mount("/screenshots", StaticFiles(directory="screenshots"), name="screenshots")


@app.get("/")
def home():
    return {
        "message": "ScreenPilot AI backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/plan")
def plan(command: str = Query(..., description="User command")):
    return plan_action(command)


@app.get("/run")
def run_agent(command: str = Query(..., description="User command")):
    return {
        "status": "success",
        "command": command,
        "actions": [
            {"action": "analyze_command"},
            {"action": "generate_plan"},
            {"action": "execute_browser_task"}
        ]
    }


@app.get("/run-browser")
def run_browser(command: str = Query(..., description="Browser task")):
    result = run_browser_task(command)

    if result.get("status") == "success" and result.get("screenshot"):
        screenshot_file = result["screenshot"].replace("\\", "/").split("/")[-1]
        result["screenshot_url"] = f"http://127.0.0.1:8001/screenshots/{screenshot_file}"

    return result