import json
from google import genai

client = genai.Client(api_key="YOUR_REAL_GEMINI_API_KEY")

SYSTEM_PROMPT = """
You are an AI browser action planner for ScreenPilot AI.

Return ONLY valid JSON.
Do not use markdown.
Do not explain anything.

Use this exact format:
{
  "intent": "",
  "site": "",
  "url": "",
  "query": "",
  "email": {
    "to": "",
    "subject": "",
    "body": ""
  }
}
"""

def fallback_plan(user_command: str):
    text = user_command.lower().strip()

    if "devpost" in text:
        return {
            "intent": "search_devpost",
            "site": "devpost",
            "url": "",
            "query": user_command.replace("on Devpost", "").replace("on devpost", "").replace("Devpost", "").replace("devpost", "").strip(),
            "email": {"to": "", "subject": "", "body": ""}
        }

    if "github" in text:
        return {
            "intent": "open_site",
            "site": "github",
            "url": "",
            "query": "",
            "email": {"to": "", "subject": "", "body": ""}
        }

    if "youtube" in text:
        return {
            "intent": "open_site",
            "site": "youtube",
            "url": "",
            "query": "",
            "email": {"to": "", "subject": "", "body": ""}
        }

    if "linkedin" in text:
        return {
            "intent": "open_site",
            "site": "linkedin",
            "url": "",
            "query": "",
            "email": {"to": "", "subject": "", "body": ""}
        }

    if "gmail" in text or text == "open mail":
        return {
            "intent": "open_gmail",
            "site": "gmail",
            "url": "",
            "query": "",
            "email": {"to": "", "subject": "", "body": ""}
        }

    if "email" in text or "mail" in text:
        return {
            "intent": "compose_email",
            "site": "gmail",
            "url": "",
            "query": "",
            "email": {
                "to": "",
                "subject": "Application for Software Engineer Role",
                "body": "Hello Recruiter,\n\nI hope you are doing well. I am writing to express my interest in the Software Engineer role. I would love the opportunity to contribute and learn more about the position.\n\nThank you for your time.\n\nBest regards"
            }
        }

    return {
        "intent": "search_web",
        "site": "",
        "url": "",
        "query": user_command,
        "email": {"to": "", "subject": "", "body": ""}
    }


def plan_action(user_command: str):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\nUser command: {user_command}"
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception:
        return fallback_plan(user_command)