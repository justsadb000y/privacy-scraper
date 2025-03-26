from source.scraper import PrivacyScraper
from source.media import MediaDownloader, download_and_process_video, process_posts
import subprocess
import sys
import os
import shutil
import subprocess

DOWNLOAD_DIR = "downloads"

def main():
    scraper = PrivacyScraper()

    if scraper.login():
        media_downloader = MediaDownloader(scraper.scraper)
        profiles = scraper.get_profiles()

        if profiles:
            print("Perfis disponíveis:\n")
            for idx, name in enumerate(profiles):
                print(f"{idx + 1}. {name}")

            selected_input = input("\nDigite os números dos perfis desejados (separados por vírgula): ")
            selected_indices = []
            try:
                selected_indices = [int(i.strip()) - 1 for i in selected_input.split(",") if i.strip().isdigit()]
            except Exception as e:
                print(f"Erro ao interpretar seleção: {e}")
                return

            selected_profiles = [profiles[i] for i in selected_indices if 0 <= i < len(profiles)]

            if not selected_profiles:
                print("Nenhum perfil válido selecionado. Encerrando.")
                return

            print("\nTipo de mídia:")
            print("1. Fotos")
            print("2. Vídeos")
            print("3. Ambos")
            media_type = input("Digite o número da opção desejada: ").strip()
            if media_type not in ["1", "2", "3"]:
                print("Tipo de mídia inválido. Encerrando.")
                return

            for profile in selected_profiles:
                print(f"\n[PROCESSANDO PERFIL]: {profile}")
                process_posts(scraper, media_downloader, profile, media_type)

        else:
            print("Nenhum perfil encontrado.")
        scraper.close()
    else:
        print("Falha no login.")

if __name__ == "__main__":
    main()
