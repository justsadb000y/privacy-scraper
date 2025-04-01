from source.scraper import PrivacyScraper
from source.media import MediaDownloader, download_and_process_video, process_posts
import inquirer
import os

DOWNLOAD_DIR = "downloads"

def main():
    scraper = PrivacyScraper()

    if scraper.login():
        media_downloader = MediaDownloader(scraper.scraper)
        profiles = sorted(scraper.get_profiles(), key=lambda p: p.lower())

        if profiles:
            profile_choices = [(p.lower(), p) for p in profiles]
            questions = [
                inquirer.Checkbox(
                    'profiles',
                    message="Selecione os perfis para baixar (use espaço para marcar):",
                    choices=profile_choices,
                )
            ]
            answers = inquirer.prompt(questions)
            selected_profiles = answers.get('profiles', [])

            if not selected_profiles:
                print("Nenhum perfil selecionado. Encerrando.")
                return

            media_question = [
                inquirer.List(
                    'media_type',
                    message="Escolha o tipo de mídia para download",
                    choices=[
                        ("Fotos", "1"),
                        ("Vídeos", "2"),
                        ("Ambos", "3")
                    ]
                )
            ]
            media_type_answer = inquirer.prompt(media_question)
            media_type = media_type_answer.get('media_type')

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
