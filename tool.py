from http.server import BaseHTTPRequestHandler
from playwright.sync_api import sync_playwright
from faker import Faker
import json
import urllib.parse

fake = Faker()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Get the link from the request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        target_url = data.get("url")

        if not target_url:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing URL")
            return

        result = self.run_automation(target_url)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def run_automation(self, url):
        # Use Playwright
        with sync_playwright() as p:
            # NOTE: To run this on Vercel, you usually connect to a remote browser
            # because Vercel doesn't have a local browser installed.
            # Example using Browserless.io (you can get a free API key):
            # browser = p.chromium.connect_over_cdp("wss://chrome.browserless.io?token=YOUR_API_KEY")
            
            # For local testing, use:
            browser = p.chromium.launch(headless=True)
            
            context = browser.new_context()
            page = context.new_page()

            try:
                # 1. Go to website
                page.goto(url, wait_until="networkidle")

                # 2. Generate data
                data = {
                    "first": fake.first_name(),
                    "last": fake.last_name(),
                    "email": fake.email(),
                    "password": fake.password()
                }

                # 3. Put data in form (using common selectors)
                # Playwright is smart: 'input[name="firstname"]' works for most modern sites
                page.fill('input[name*="first"]', data["first"])
                page.fill('input[name*="last"]', data["last"])
                page.fill('input[type="email"]', data["email"])
                page.fill('input[type="password"]', data["password"])

                # 4. Press the button
                # Finds a button that has "Create" or "Sign" in the text
                page.click('button:has-text("Create"), button:has-text("Sign"), input[type="submit"]')
                
                # Wait a moment for result
                page.wait_for_timeout(3000)

                return {"status": "success", "email_used": data["email"]}

            except Exception as e:
                return {"status": "error", "message": str(e)}
            finally:
                browser.close()
