## [English Version](https://github.com/justsadb000y/privacy-scraper/blob/main/README-en.md)

# 🔒 Privacy Scraper

Ferramenta para baixar conteúdos exclusivamente de perfis dos quais você já é assinante.

---

## 🎬 Configuração do FFmpeg

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

## 🚀 Executável (recomendado)

1. Faça o download do executável diretamente nas [releases](https://github.com/justsadb000y/privacy-scraper/releases).
2. Extraia o conteúdo do arquivo ZIP.
3. Edite o arquivo `.env` na pasta extraída conforme o exemplo abaixo:

```env
EMAIL=seuemail@gmail.com
PASSWORD=suasenha123
WORKERS=5
```

4. Execute o arquivo executável para iniciar o programa.

5. Após iniciar, siga as instruções:

- Escolha o número correspondente ao perfil desejado.
- Digite `0` para baixar conteúdos de todos os perfis disponíveis.
- Selecione o tipo de mídia que deseja baixar:
  - `1` para Fotos
  - `2` para Vídeos
  - `3` para Ambos

---

## ⚙️ Execução manual (via Python)

### 1. Instalar dependências e recursos

Abra o terminal na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Altere o arquivo `.env` na pasta raiz do projeto com o seguinte formato:

```env
EMAIL=seuemail@gmail.com
PASSWORD=suasenha123
WORKERS=5
```

### 3. Executar o script

Execute o script principal:

```bash
python privacy_scraper.py
```

---

## 📌 Observações

- Garanta que suas credenciais no arquivo `.env` estejam corretas.
- Certifique-se de que possui autorização para baixar o conteúdo dos perfis selecionados.

---