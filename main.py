from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from automation import run_browser_task
from gemini_agent import plan_action

import os

# create screenshot folder
os.makedirs("screenshots", exist_ok=True)

app = FastAPI(
    title="ScreenPilot AI Backend",
    description="Backend API for ScreenPilot AI",
    version="1.0.0"
)

# CORS (for Vercel frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve screenshots
app.mount("/screenshots", StaticFiles(directory="screenshots"), name="screenshots")


@app.get("/")
def home():
    return {"message": "ScreenPilot AI backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/plan")
def plan(command: str = Query(..., description="User command")):
    result = plan_action(command)
    return result


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

        file = result["screenshot"].replace("\\", "/").split("/")[-1]

        result["screenshot_url"] = f"https://screenpilot-ai-gemini-powered-browser-9kk0.onrender.com/screenshots/{file}"

    return result
