import os
import re
import urllib.parse
import chardet
import ffmpeg
import shutil
import json
from tqdm import tqdm

DOWNLOAD_DIR = "downloads"

class MediaDownloader:
    def __init__(self, scraper):
        self.scraper = scraper

    def download_file(self, url, filename, tokenContent, pbar=None):
        uri = url.split("hls/", 1)[-1]
        headers = {
            "referer": "https://privacy.com.br/",
            "Content": tokenContent,
            'X-Content-Uri': uri
        }

        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            response = self.scraper.get(url, headers=headers, stream=True)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                if pbar:
                    pbar.update(1)
                return True
            else:
                print(f"[ERRO] Falha ao baixar {url}: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERRO] Falha ao baixar {url}: {e}")
            return False

    def get_best_quality_m3u8(self, main_m3u8_url, main_m3u8_content):
        lines = main_m3u8_content.split('\n')
        best_quality_url = None
        max_bandwidth = 0
        current_bandwidth = 0

        for line in lines:
            if line.startswith('#EXT-X-STREAM-INF'):
                bandwidth_match = re.search(r'BANDWIDTH=(\d+)', line)
                if bandwidth_match:
                    current_bandwidth = int(bandwidth_match.group(1))
            elif line.strip() and not line.startswith('#'):
                if current_bandwidth > max_bandwidth:
                    max_bandwidth = current_bandwidth
                    best_quality_url = urllib.parse.urljoin(main_m3u8_url, line.strip())

        return best_quality_url

    def process_m3u8(self, m3u8_url, base_path, tokenContent):
        m3u8_filename = os.path.join(base_path, "playlist.m3u8")

        if self.download_file(m3u8_url, m3u8_filename, tokenContent):
            with open(m3u8_filename, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            modified_content = []

            for line in lines:
                if line.startswith('#EXT-X-SESSION-KEY') or line.startswith('#EXT-X-KEY'):
                    uri_match = re.search(r'URI="([^"]+)"', line)
                    if uri_match:
                        key_url = uri_match.group(1)
                        parsed = urllib.parse.urlparse(key_url)
                        original_key_name = os.path.basename(parsed.path)

                        new_key_name = f"{original_key_name}.key"
                        key_path = os.path.join(base_path, new_key_name)

                        if self.download_file(key_url, key_path, tokenContent) and os.path.exists(key_path):
                            new_line = line.replace(uri_match.group(0), f'URI="{new_key_name}"')
                            modified_content.append(new_line)
                        else:
                            print(f"[AVISO] Não foi possível baixar ou salvar a chave: {key_url}")
                            modified_content.append(line)
                    else:
                        modified_content.append(line)

                elif line.strip() and not line.startswith('#'):
                    segment_url = urllib.parse.urljoin(m3u8_url, line.strip())
                    segment_filename = os.path.join(base_path, os.path.basename(segment_url))

                    if self.download_file(segment_url, segment_filename, tokenContent):
                        modified_content.append(os.path.basename(segment_filename))
                    else:
                        print(f"[ERRO] Falha ao baixar segmento: {segment_url}")
                        modified_content.append(line)
                else:
                    modified_content.append(line)

            with open(m3u8_filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(modified_content))

            return m3u8_filename

        return None

    def convert_m3u8_to_mp4(self, input_file, output_file):
        try:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"Arquivo não encontrado: {input_file}")

            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            try:
                ffmpeg.input(input_file, allowed_extensions='ALL').output(
                    output_file,
                    vcodec='copy',
                    acodec='copy',
                    loglevel='error'
                ).overwrite_output().run()
                return True
            except ffmpeg.Error:
                print("[WARN] Conversão rápida falhou, tentando reencode...")

                ffmpeg.input(input_file, allowed_extensions='ALL').output(
                    output_file,
                    vcodec='libx264',
                    acodec='aac',
                    preset='ultrafast',
                    crf=23,
                    loglevel='error'
                ).overwrite_output().run()
                return True
        except Exception as e:
            print(f"[ERRO] Falha na conversão do vídeo: {e}")
            return False

    def clean_temp_files(self, base_path):
        try:
            shutil.rmtree(base_path)
        except Exception as e:
            print(f"[ERRO] Falha ao remover arquivos temporários: {e}")


def download_and_process_video(scraper, media_downloader, profile_name, file, token_content):
    base_path = os.path.join(DOWNLOAD_DIR, profile_name, "videos", f"{file['mediaId']}_temp")
    os.makedirs(base_path, exist_ok=True)
    main_m3u8_filename = os.path.join(base_path, "main.m3u8")

    if media_downloader.download_file(file["url"], main_m3u8_filename, token_content):
        with open(main_m3u8_filename, 'rb') as f:
            raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding']
        with open(main_m3u8_filename, 'r', encoding=encoding, errors='replace') as f:
            m3u8_content = f.read()

        best_quality_url = media_downloader.get_best_quality_m3u8(file["url"], m3u8_content)
        if best_quality_url:
            best_m3u8_filename = media_downloader.process_m3u8(best_quality_url, base_path, token_content)
            if best_m3u8_filename and os.path.exists(best_m3u8_filename):
                output_filename = os.path.join(DOWNLOAD_DIR, profile_name, "videos", f"{file['mediaId']}.mp4")
                success = media_downloader.convert_m3u8_to_mp4(best_m3u8_filename, output_filename)
                if not success:
                    print(f"[ERRO] Falha na conversão para vídeo {file['mediaId']}")
    else:
        print(f"[ERRO] Falha ao baixar o M3U8 para o vídeo {file['mediaId']}")

    media_downloader.clean_temp_files(base_path)


def process_posts(scraper, media_downloader, selected_profile_name, media_type):
    total, total_photos, total_videos = scraper.get_total_media_count(selected_profile_name)
    print(f"Total de mídias: {total} (Fotos: {total_photos}, Vídeos: {total_videos})")

    os.makedirs(f"{DOWNLOAD_DIR}/{selected_profile_name}/fotos", exist_ok=True)
    os.makedirs(f"{DOWNLOAD_DIR}/{selected_profile_name}/videos", exist_ok=True)

    skip = 0
    downloaded_count = 0

    progress_total = {
        "1": total_photos,
        "2": total_videos,
        "3": total
    }.get(media_type, total)

    skip = 0

    with tqdm(total=progress_total, desc=f"Baixando mídias de {selected_profile_name}", unit="mídia") as pbar:
        while True:
            posts = scraper.get_posts(selected_profile_name, skip=skip)
            if not posts.get("mosaicItems"):
                break

            for item in posts["mosaicItems"]:
                for file in item.get("files", []):
                    if not file["isLocked"]:
                        file_type = file["type"]
                        file_url = file["url"]

                        if file_type == "image" and media_type in ["1", "3"]:
                            filename = f"{DOWNLOAD_DIR}/{selected_profile_name}/fotos/{file['mediaId']}.jpg"
                            if not os.path.exists(filename):
                                scraper.download_image(file_url, filename)
                                if os.path.exists(filename):
                                    downloaded_count += 1
                            pbar.update(1)

                        elif file_type == "video" and media_type in ["2", "3"]:
                            output_filename = f"{DOWNLOAD_DIR}/{selected_profile_name}/videos/{file['mediaId']}.mp4"
                            if not os.path.exists(output_filename):
                                file_id = file["url"].split("/hls/")[0].split("/")[-1]
                                payload = {'exp': 3600, 'file_id': file_id}
                                token_url = "https://service.privacy.com.br/media/video/token"
                                headers = {
                                    "Content-Type": "application/json",
                                    "Authorization": f"Bearer {scraper.token_v2}"
                                }

                                payload_json = json.dumps(payload)
                                headers_json = json.dumps(headers)

                                token_response = scraper.page.evaluate(f'''
                                    async () => {{
                                        const response = await fetch("{token_url}", {{
                                            method: "POST",
                                            headers: {headers_json},
                                            body: JSON.stringify({payload_json})
                                        }});
                                        return await response.text();
                                    }}
                                ''')

                                try:
                                    token_content = json.loads(token_response).get("content")
                                    if token_content:
                                        before = os.path.exists(output_filename)
                                        download_and_process_video(scraper.scraper, media_downloader, selected_profile_name, file, token_content)
                                        after = os.path.exists(output_filename)
                                        if not before and after:
                                            downloaded_count += 1
                                except Exception as e:
                                    print(f"[ERRO] Falha ao extrair token de vídeo ({file['mediaId']}): {e}")
                                    print(f"Resposta: {token_response}")
                            pbar.update(1)

            skip += 30
            if skip >= total:
                break
    
    print(f"\n[RESUMO] Total de arquivos novos baixados: {downloaded_count}/{progress_total}")