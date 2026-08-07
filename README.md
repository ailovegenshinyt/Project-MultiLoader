```
# MultiLoader 🎵

**Premium Multi-Source Downloader with Liquid Glass UI**

A fast, beautiful self-hosted downloader for **YouTube** (videos & playlists) and **Spotify** (tracks, albums & playlists).  
Built with a modern glassmorphism interface, real-time progress streaming, and automatic metadata + thumbnail embedding.

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![Flask](https://img.shields.io/badge/backend-Flask-green)
![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red)

---

## ✨ Features

- 🎬 **YouTube** — Single videos and full playlists (up to 4K)
- 🎵 **Spotify** — Tracks, albums & playlists (resolved via YouTube search)
- 📊 **Real-time progress** — Live progress bar + terminal-style log via Server-Sent Events
- 🏷️ **Metadata embedding** — Title, artist, album + cover art automatically embedded
- 🧹 **Auto cleanup** — Downloads folder is cleared on startup and every 5 minutes
- 📱 **Mobile friendly** — Clean responsive UI that works well on phones and tablets
- ⚡ **Playlist ZIP** — Multi-track downloads are automatically packed into a single ZIP
- 🎨 **Liquid Glass UI** — Animated blobs, glassmorphism cards, smooth transitions

---

## 📦 Supported Formats

| Type   | Format | Qualities                          |
|--------|--------|------------------------------------|
| Video  | MP4    | 4K, 1080p, 720p, 480p             |
| Audio  | MP3    | 320 / 256 / 192 / 128 kbps        |
| Audio  | WAV    | Lossless                           |

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/ailovegenshinyt/Project-MulitLoader.git
cd Project-MulitLoader
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** You also need [FFmpeg](https://ffmpeg.org/) installed and available in your system PATH.

### 3. Run the app

```bash
python app.py
```

When you start the app you will see a menu:

- **Local mode** → Access at `http://localhost:8080`
- **Public mode (ngrok)** → Creates a public link

#### To use Public mode (ngrok):

1. Get a free authtoken from [ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken)
2. Open `app.py` and find this line (around line 651):

```python
NGROK_AUTHTOKEN = "YOUR_NGROK_AUTNTOKEN"
```

3. Replace `"YOUR_NGROK_AUTNTOKEN"` with your real ngrok authtoken
4. Run the app again and choose Public mode

---

## 🛠️ Tech Stack

| Layer              | Technology                          |
|--------------------|-------------------------------------|
| Backend            | Python, Flask                       |
| Downloader engine  | yt-dlp                              |
| Media processing   | FFmpeg                              |
| Frontend           | Vanilla HTML / CSS / JavaScript     |
| Real-time updates  | Server-Sent Events (SSE)            |
| HTTP helpers       | requests, curl_cffi                 |

---

## 📁 Project Structure

```
Project-MulitLoader/
├── app.py              # Flask backend + download logic
├── index.html          # Main UI
├── style.css           # Liquid Glass design system
├── main.js             # Frontend logic + SSE progress
├── requirements.txt    # Python dependencies
└── downloads/          # Temporary download storage (auto-cleaned)
```

---

## 🔧 How it works

1. Paste a YouTube or Spotify URL
2. Choose format (Video / MP3 / WAV) and quality
3. Backend creates a background task and returns a `task_id`
4. Frontend connects to `/progress/<task_id>` via SSE
5. Live progress events update the progress bar and terminal log
6. When finished, the file (or ZIP for playlists) is served for download
7. Metadata and cover art are embedded for audio files

---

## ⚠️ Disclaimer

This project is intended for **personal and educational use only**.  
Please respect the terms of service of YouTube, Spotify, and copyright laws in your country.  
The author is not responsible for any misuse of this software.

---

## 👤 Author

**CoR3 Coding-R**  
GitHub: [ailovegenshinyt](https://github.com/ailovegenshinyt)

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

© 2026 MultiLoader — Open Source & Community Driven
```
