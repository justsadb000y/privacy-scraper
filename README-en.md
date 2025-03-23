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
