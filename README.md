## [English Version](https://github.com/justsadb000y/privacy-scraper/blob/main/README-en.md)

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

- Ensure your credentials in the `.env` file are correct.
- Make sure you have permission to download content from the selected profiles.

---
