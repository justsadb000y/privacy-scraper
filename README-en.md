## [Versão em Português](https://github.com/justsadb000y/privacy-scraper/blob/main/README.md)

# 🔒 Privacy Scraper

Tool to download content exclusively from profiles to which you already subscribe.

---

## 🎬 FFmpeg Setup

To download and configure FFmpeg, follow these steps:

1. Download FFmpeg from [GitHub (releases)](https://github.com/BtbN/FFmpeg-Builds/releases).

2. Extract the ZIP file to a folder on your computer (e.g., `C:\ffmpeg\bin`).

3. Add the FFmpeg path to your environment variables:

   - Press `Win + S` and type **environment variables**.
   - Click on **Edit the system environment variables**.
   - In the opened window, click **Environment Variables**.
   - Under **System Variables**, locate and select `Path`, click **Edit**, then **New**, and add the FFmpeg path (e.g., `C:\ffmpeg\bin`).

4. Restart your terminal to apply changes.

---

## 🚀 Executable (recommended)

1. Download the executable directly from the [releases](https://github.com/justsadb000y/privacy-scraper/releases).
2. Extract the contents of the ZIP file.
3. Edit the `.env` file in the extracted folder as shown below:

```env
EMAIL=yourmail@gmail.com
PASSWORD=yourpassword123
WORKERS=5
```

4. Run the executable file to start the program.

5. After launching, follow the instructions:

- Choose the number corresponding to the desired profile.
- Enter `0` to download content from all available profiles.
- Select the type of media to download:
  - `1` for Photos
  - `2` for Videos
  - `3` for Both

---

## ⚙️ Manual execution (via Python)

### 1. Install dependencies and resources

Open the terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Modify the `.env` file in the project's root folder as follows:

```env
EMAIL=yourmail@gmail.com
PASSWORD=yourpassword123
WORKERS=5
```

### 3. Run the script

Execute the main script:

```bash
python privacy_scraper.py
```

---

## 📌 Notes

- Ensure your credentials in the `.env` file are correct.
- Make sure you have permission to download content from the selected profiles.

---

