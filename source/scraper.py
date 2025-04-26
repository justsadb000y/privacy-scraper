import base64
import re
import os
import platform
import json
import time
import cloudscraper
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import logging

load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_FILE = "debug.log"

custom_headers = {
    "referer": "https://privacy.com.br/",
    "origin": "https://privacy.com.br",
    "priority": "u=1, i",
    "accept": "*/*",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

if DEBUG:
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='[%(levelname)s] %(message)s')

def log_debug(msg):
    if DEBUG:
        print(f"[DEBUG] {msg}")
        logging.debug(msg)

def strip_edits_from_image_url(image_url):
    match = re.search(r"https:\/\/[^\/]+\/([^\/?]+)", image_url)
    if not match:
        return image_url

    token = match.group(1)
    padding = '=' * ((4 - len(token) % 4) % 4)
    token_bytes = base64.urlsafe_b64decode(token + padding)
    token_json = json.loads(token_bytes)
    token_json['edits'] = {}
    cleaned_token = base64.urlsafe_b64encode(json.dumps(token_json).encode()).decode().rstrip("=")
    new_url = image_url.replace(token, cleaned_token)
    return new_url

def get_embedded_chromium_path():
    playwright_path = os.path.expanduser("~/.cache/ms-playwright") if os.name != 'nt' else os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'ms-playwright')
    if os.path.exists(playwright_path):
        return
    base = os.path.dirname(os.path.abspath(__file__))
    browser_root = os.path.join(base, "..", "playwright-browsers")
    if not os.path.exists(browser_root):
        raise FileNotFoundError(f"Playwright browser directory not found at {browser_root}")
    chromium_dirs = [d for d in os.listdir(browser_root) if d.startswith("chromium-")]
    if not chromium_dirs:
        raise FileNotFoundError("No Chromium installation found in playwright-browsers.")
    chromium_dir = chromium_dirs[0]
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
        log_debug("PrivacyScraper instanciado")

    def login(self):
        log_debug("Iniciando login...")
        self.playwright = sync_playwright().start()
        path = get_embedded_chromium_path()
        self.browser = self.playwright.chromium.launch(headless=False, executable_path=path)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        log_debug("Navegador iniciado")
        self.page.goto("https://privacy.com.br")
        time.sleep(3)
        log_debug("Página inicial carregada")

        result = self.page.evaluate(f"""
            async () => {{
                const response = await fetch("https://service.privacy.com.br/auth/login", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
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
        print(result)

        try:
            tokens = json.loads(result)
            self.token_v1 = tokens.get("tokenV1")
            self.token_v2 = tokens.get("token")
            log_debug("Tokens extraídos com sucesso")
        except Exception as e:
            log_debug(f"Erro ao extrair tokens: {str(e)}")
            self.browser.close()
            self.playwright.stop()
            return False

        if self.token_v1 and self.token_v2:
            log_debug("Login bem-sucedido")
            self.authorize_tokens()
            return True
        else:
            log_debug(f"Erro no login: tokens ausentes. {result}")
            self.browser.close()
            self.playwright.stop()
            return False

    def authorize_tokens(self):
        url = f"https://privacy.com.br/strangler/Authorize?TokenV1={self.token_v1}&TokenV2={self.token_v2}"
        self.playwright_get(url)
        log_debug("Tokens autorizados")

    def playwright_get(self, url, extra_headers: dict = None):
        headers = {
            "Authorization": f"Bearer {self.token_v2}",
            "Referer": "https://privacy.com.br/",
            **(extra_headers or {})
        }
        log_debug(f"GET para: {url}")
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
        log_debug("Obtendo perfis...")
        url = "https://service.privacy.com.br/profile/UserFollowing?page=0&limit=30&nickName="
        result = self.playwright_get(url, custom_headers)
        profiles = json.loads(result)
        log_debug(f"Perfis obtidos: {[p['profileName'] for p in profiles]}")
        return [profile["profileName"] for profile in profiles]

    def get_total_media_count(self, profile_name):
        log_debug(f"Obtendo contagem de mídias para {profile_name}")
        url = f"https://privacy.com.br/profile/{profile_name}/Mosaico"
        result = self.playwright_get(url, custom_headers)
        soup = BeautifulSoup(result, 'html.parser')
        total_match = soup.find('a', class_='filter-button selected')
        photos_match = soup.find('a', href=f"/profile/{profile_name}/Fotos")
        videos_match = soup.find('a', href=f"/profile/{profile_name}/Videos")

        def parse_number(text):
            return int(text.split()[0].replace('.', '').replace(',', '')) if text else 0

        total = parse_number(total_match.text if total_match else None)
        photos = parse_number(photos_match.text if photos_match else None)
        videos = parse_number(videos_match.text if videos_match else None)
        log_debug(f"Contagens - Total: {total}, Fotos: {photos}, Vídeos: {videos}")
        return total, photos, videos

    def get_posts(self, profile_name, skip=0):
        unix_timestamp = int(time.time() * 1000)
        url = f"https://privacy.com.br/Profile?handler=PartialPosts&skip={skip}&take=50&nomePerfil={profile_name}&filter=mosaico&_={unix_timestamp}"
        log_debug(f"Buscando posts para {profile_name}, skip={skip}")
        result = self.playwright_get(url)
        return json.loads(result)

    def download_image_safe(self, url, filename):
        try:
            headers = {
                "referer": "https://privacy.com.br/",
                "origin": "https://privacy.com.br",
                "priority": "u=1, i",
                "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                "sec-fetch-dest": "image",
                "sec-fetch-mode": "no-cors",
                "sec-fetch-site": "same-site",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
            }
            
            response = self.scraper.get(url, headers=headers, stream=True)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                log_debug(f"[SAFE] Imagem salva: {filename}")
                return True
            elif response.status_code == 413:
                log_debug(f"[SAFE] Erro 413 com altura {height}, tentando menor...")
            else:
                log_debug(f"[SAFE] Erro {response.status_code} ao baixar: {final_url}")
        except Exception as e:
            log_debug(f"[SAFE] Erro ao baixar imagem com fallback: {e}")
        return False


    def download_video_mp4_direct(self, url, filename, token_content):
        log_debug(f"Detectado link direto para MP4: {url}")
        headers = {
            "referer": "https://privacy.com.br/",
            "Content": token_content
        }
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            response = self.scraper.get(url, headers=headers, stream=True)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                log_debug(f"Download direto concluído: {filename}")
                return True
            else:
                log_debug(f"[ERRO] Status {response.status_code} ao baixar mp4 direto: {url}")
        except Exception as e:
            log_debug(f"[ERRO] Exceção ao baixar mp4 direto: {e}")
        return False

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        log_debug("Browser fechado")