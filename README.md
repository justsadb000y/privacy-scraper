## [English Version](#-privacy-scraper-english)

# 🔒 Privacy Scraper

Ferramenta para baixar conteúdos exclusivamente de perfis dos quais você já é assinante.

---

## 🚀 Instalação

### 1. Instalar dependências

Abra o terminal e execute:

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` na pasta raiz do projeto com o seguinte formato:

```env
EMAIL=seuemail@gmail.com
PASSWORD=suasenha123
WORKERS=5
```

---

## ⚙️ Como executar

Execute o script principal:

```bash
python privacy_scraper.py
```

Após iniciar, siga as instruções:

- Escolha o número correspondente ao perfil desejado.
- Digite `0` para baixar conteúdos de todos os perfis disponíveis.
- Selecione o tipo de mídia que deseja baixar:
  - `1` para Fotos
  - `2` para Vídeos
  - `3` para Ambos

---

## 🎬 Configuração do FFmpeg (Opcional)

Para baixar e configurar o FFmpeg, siga estes passos:

1. Baixe o FFmpeg no [GitHub (releases)](https://github.com/BtbN/FFmpeg-Builds/releases).

2. Extraia o arquivo ZIP em uma pasta no seu computador (exemplo: `C:\ffmpeg\bin`).

3. Adicione o caminho do FFmpeg às variáveis de ambiente:

   - Pressione `Win + S` e digite **variáveis de ambiente**.
   - Clique em **Editar as variáveis de ambiente do sistema**.
   - Na janela aberta, clique em **Variáveis de Ambiente**.
   - Em **Variáveis do sistema**, localize e selecione `Path`, clique em **Editar**, depois em **Novo** e adicione o caminho para o FFmpeg (exemplo: `C:\ffmpeg\bin`).

4. Reinicie o terminal para que as mudanças tenham efeito.

---

## 📌 Observações

- Garanta que suas credenciais no arquivo `.env` estejam corretas.
- Certifique-se de que possui autorização para baixar o conteúdo dos perfis selecionados.

---

# 🔒 Privacy Scraper (English)

Tool to download content exclusively from profiles you already subscribe to.

---

## 🚀 Installation

### 1. Install dependencies

Open the terminal and run:

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project's root folder with the following format:

```env
EMAIL=youremail@gmail.com
PASSWORD=yourpassword123
WORKERS=5
```

---

## ⚙️ How to run

Run the main script:

```bash
python privacy_scraper.py
```

After starting, follow the instructions:

- Choose the number corresponding to the desired profile.
- Enter `0` to download content from all available profiles.
- Select the type of media you want to download:
  - `1` for Photos
  - `2` for Videos
  - `3` for Both

---

## 🎬 FFmpeg Setup (Optional)

To download and set up FFmpeg, follow these steps:

1. Download FFmpeg from [GitHub (releases)](https://github.com/BtbN/FFmpeg-Builds/releases).

2. Extract the ZIP file to a folder on your computer (example: `C:\ffmpeg\bin`).

3. Add the FFmpeg path to your environment variables:

   - Press `Win + S` and type **environment variables**.
   - Click **Edit the system environment variables**.
   - In the opened window, click **Environment Variables**.
   - Under **System variables**, select `Path`, click **Edit**, then **New** and add the path to FFmpeg (example: `C:\ffmpeg\bin`).

4. Restart the terminal for changes to take effect.

---

## 📌 Notes

- Ensure your credentials in the `.env` file are correct.
- Make sure you have permission to download content from the selected profiles.

---
