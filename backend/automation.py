from playwright.sync_api import sync_playwright
import os
import urllib.parse
import time
from gemini_agent import plan_action


def run_browser_task(command: str):
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    plan = plan_action(command)

    try:
        intent = plan.get("intent", "")

        # -----------------------------
        # EMAIL DRAFT MODE
        # -----------------------------
        if intent == "compose_email":
            email = plan.get("email", {})

            return {
                "status": "success",
                "message": "Email draft generated successfully",
                "plan": plan,
                "final_url": "",
                "page_title": "Email Draft Preview",
                "screenshot": "",
                "email_preview": {
                    "to": email.get("to", ""),
                    "subject": email.get("subject", ""),
                    "body": email.get("body", "")
                }
            }

        # -----------------------------
        # BROWSER AUTOMATION MODE
        # -----------------------------
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            try:
                final_message = ""

                if intent == "search_devpost":
                    query = urllib.parse.quote(plan.get("query", command))
                    target_url = f"https://devpost.com/search/projects?q={query}"
                    page.goto(target_url, wait_until="domcontentloaded")
                    final_message = f"Searched Devpost for: {plan.get('query', command)}"

                elif intent == "open_site":
                    url = plan.get("url", "").strip()
                    site = plan.get("site", "").strip().lower()

                    if not url:
                        if "github" in site:
                            url = "https://github.com"
                        elif "youtube" in site:
                            url = "https://youtube.com"
                        elif "linkedin" in site:
                            url = "https://linkedin.com"
                        elif "devpost" in site:
                            url = "https://devpost.com"
                        elif "gmail" in site:
                            url = "https://mail.google.com"
                        else:
                            url = "https://www.bing.com/search?q=" + urllib.parse.quote(command)

                    page.goto(url, wait_until="domcontentloaded")
                    final_message = f"Opened site: {url}"

                elif intent == "open_gmail":
                    # Gmail likely needs login, so just open homepage
                    page.goto("https://mail.google.com", wait_until="domcontentloaded")
                    final_message = "Opened Gmail login page"

                else:
                    query = urllib.parse.quote(plan.get("query", command))
                    target_url = f"https://www.bing.com/search?q={query}"
                    page.goto(target_url, wait_until="domcontentloaded")
                    final_message = f"Searched web for: {plan.get('query', command)}"

                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(3000)

                filename = f"result_{int(time.time())}.png"
                screenshot_path = os.path.join(screenshots_dir, filename)
                page.screenshot(path=screenshot_path, full_page=True)

                result = {
                    "status": "success",
                    "message": final_message,
                    "plan": plan,
                    "final_url": page.url,
                    "page_title": page.title(),
                    "screenshot": screenshot_path
                }

            except Exception as e:
                result = {
                    "status": "error",
                    "message": str(e),
                    "plan": plan
                }

            finally:
                browser.close()

            return result

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "plan": {}
        }