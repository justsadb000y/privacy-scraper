import os
import platform
import json
import time
import cloudscraper
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

def get_embedded_chromium_path():
    base = os.path.dirname(os.path.abspath(__file__))
    browser_root = os.path.join(base, "..", "playwright-browsers")

    if not os.path.exists(browser_root):
        raise FileNotFoundError(f"Playwright browser directory not found at {browser_root}")

    chromium_dirs = [d for d in os.listdir(browser_root) if d.startswith("chromium-")]
    if not chromium_dirs:
        raise FileNotFoundError("No Chromium installation found in playwright-browsers.")

    chromium_dir = chromium_dirs[0]  # usa o primeiro encontrado
    chromium_path = os.path.join(browser_root, chromium_dir)

    system = platform.system()
    if system == "Windows":
        return os.path.join(chromium_path, "chrome-win", "chrome.exe")
    else:
        raise RuntimeError(f"Unsupported OS: {system}")

class PrivacyScraper:
    def __init__(self):
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
        self.token_v1 = None
        self.token_v2 = None
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        self.scraper = cloudscraper.create_scraper()

    def login(self):
        self.playwright = sync_playwright().start()
        path = get_embedded_chromium_path()
        self.browser = self.playwright.chromium.launch(headless=False, executable_path=path)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

        print("Acessando a página inicial...")
        self.page.goto("https://privacy.com.br")
        time.sleep(3)

        print("Enviando login via fetch JS na página...")
        result = self.page.evaluate(f"""
            async () => {{
                const response = await fetch("https://service.privacy.com.br/auth/login", {{
                    method: "POST",
                    headers: {{
                        "Content-Type": "application/json"
                    }},
                    body: JSON.stringify({{
                        Email: "{self.email}",
                        Password: "{self.password}",
                        Document: null,
                        Locale: "pt-BR",
                        CanReceiveEmail: true
                    }})
                }});
                return await response.text();
            }}
        """)

        try:
            tokens = json.loads(result)
            self.token_v1 = tokens.get("tokenV1")
            self.token_v2 = tokens.get("token")
        except Exception as e:
            print("Erro ao extrair tokens:", str(e))
            self.browser.close()
            self.playwright.stop()
            return False

        if self.token_v1 and self.token_v2:
            print("Login bem-sucedido.")
            self.authorize_tokens()
            return True
        else:
            print("Erro no login: tokens ausentes.")
            self.browser.close()
            self.playwright.stop()
            return False

    def authorize_tokens(self):
        url = f"https://privacy.com.br/strangler/Authorize?TokenV1={self.token_v1}&TokenV2={self.token_v2}"
        self.playwright_get(url)

    def playwright_get(self, url, extra_headers: dict = None):
        headers = {
            "Authorization": f"Bearer {self.token_v2}",
            "Referer": "https://privacy.com.br/",
            **(extra_headers or {})
        }
        return self.page.evaluate(f"""
            async () => {{
                const response = await fetch("{url}", {{
                    method: "GET",
                    headers: {json.dumps(headers)}
                }});
                return await response.text();
            }}
        """)

    def get_profiles(self):
        url = "https://service.privacy.com.br/profile/UserFollowing?page=0&limit=30&nickName="
        result = self.playwright_get(url)
        profiles = json.loads(result)
        return [profile["profileName"] for profile in profiles]

    def get_total_media_count(self, profile_name):
        url = f"https://privacy.com.br/profile/{profile_name}/Mosaico"
        result = self.playwright_get(url)
        soup = BeautifulSoup(result, 'html.parser')
        total_match = soup.find('a', class_='filter-button selected')
        photos_match = soup.find('a', href=f"/profile/{profile_name}/Fotos")
        videos_match = soup.find('a', href=f"/profile/{profile_name}/Videos")

        def parse_number(text):
            return int(text.split()[0].replace('.', '')) if text else 0

        total = parse_number(total_match.text if total_match else None)
        photos = parse_number(photos_match.text if photos_match else None)
        videos = parse_number(videos_match.text if videos_match else None)

        return total, photos, videos

    def get_posts(self, profile_name, skip=0):
        unix_timestamp = int(time.time() * 1000)
        url = f"https://privacy.com.br/Profile?handler=PartialPosts&skip={skip}&take=10&nomePerfil={profile_name}&filter=mosaico&_={unix_timestamp}"
        result = self.playwright_get(url)
        return json.loads(result)

    def download_image(self, url, filename):
        uri = url.split("hls/", 1)[-1]
        headers = {"referer": "https://privacy.com.br/", 'X-Content-Uri': uri }

        try:
            response = self.scraper.get(url, headers=headers, stream=True)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
        except Exception as e:
            print(f"Erro ao baixar imagem {url}: {e}")

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
