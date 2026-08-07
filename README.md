# 🎵 MultiLoader — Premium Multi-Source Downloader

> **Download YouTube videos & Spotify tracks with a stunning Liquid Glass UI**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Flask](https://img.shields.io/badge/Backend-Flask-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![yt-dlp](https://img.shields.io/badge/Powered%20by-yt--dlp-red?style=flat-square)](https://github.com/yt-dlp/yt-dlp)
[![Open Source](https://img.shields.io/badge/Open-Source-blueviolet?style=flat-square)](https://github.com/ailovegenshinyt/Project-MultiLoader)

---

## ✨ What is MultiLoader?

MultiLoader is a **high-performance, self-hosted downloader** for YouTube and Spotify with a **modern, beautiful Liquid Glass UI**. Download videos, playlists, and tracks in seconds with real-time progress tracking, automatic metadata embedding, and zero ads or tracking.

**Perfect for:** Content creators, music lovers, developers, and anyone who wants a clean, fast download experience.

---

## ⚠️ IMPORTANT: Hosting Requirements

**MultiLoader MUST run on:**
- ✅ Your local machine
- ✅ Your personal server with normal internet
- ✅ VPS/Dedicated server (with residential IP preferred)

**⛔ MultiLoader CANNOT run on:**
- ❌ Google Colab
- ❌ Hugging Face Spaces
- ❌ Replit
- ❌ Public cloud services (AWS Lambda, Google Cloud Functions, etc.)
- ❌ Shared hosting platforms

**WHY?** YouTube detects requests from public cloud services as bots and blocks them. You'll get errors like:
```
ERROR: [youtube] Access denied. The following error occurred while trying to access the URL:
403 Forbidden
```

**SOLUTION:** Install locally or on your own server with a regular internet connection.

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 🎬 **YouTube Downloads** | Videos, playlists, and channels up to 4K |
| 🎵 **Spotify Support** | Tracks, albums & playlists (auto-resolved via YouTube) |
| 💎 **Liquid Glass UI** | Animated glassmorphism design with smooth interactions |
| 📊 **Real-time Progress** | Live progress bar + terminal-style logs via Server-Sent Events |
| 🏷️ **Smart Metadata** | Auto-embeds title, artist, album art, and cover images |
| 🧹 **Auto Cleanup** | Downloads folder self-cleans on startup and every 5 minutes |
| 📱 **Mobile Friendly** | Responsive design works perfectly on phones & tablets |
| ⚡ **ZIP Playlists** | Multi-track downloads auto-packed into single ZIP files |
| 🔒 **Self-Hosted** | 100% private, no tracking, no ads, runs locally |

---

## 🖼️ Screenshots

<img width="1118" height="604" alt="image" src="https://github.com/user-attachments/assets/9a6bbebb-5636-4031-b405-930809b3023e" />

---

## 📦 Supported Formats

| Type | Format | Quality Options |
|------|--------|-----------------|
| 📹 **Video** | MP4 | 4K • 1080p • 720p • 480p • 360p |
| 🎵 **Audio** | MP3 | 320 • 256 • 192 • 128 kbps |
| 🎵 **Audio** | WAV | Lossless quality |

---

## 🚀 Quick Start (2 Minutes)

### 1️⃣ Clone & Setup

```bash
git clone https://github.com/ailovegenshinyt/Project-MultiLoader.git
cd Project-MultiLoader
pip install -r requirements.txt
```

### 2️⃣ Run the App

```bash
python app.py
```

### 3️⃣ Access the UI

- **Local:** Open `http://localhost:8080` in your browser
- **From other devices:** Use ngrok tunnel (see below)

**That's it!** 🎉 Start downloading immediately.

---

## 🌐 Access from Other Devices (ngrok)

Want to access MultiLoader from your phone or another computer?

1. Get a free ngrok account: [ngrok.com/sign-up](https://dashboard.ngrok.com/sign-up)
2. Get your authtoken: [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)
3. Create `.env` file in project folder:
   ```env
   NGROK_AUTHTOKEN=your_authtoken_here
   ```
4. Run:
   ```bash
   python app.py
   ```
5. Choose option **2** for ngrok tunnel
6. Access the public URL from any device

**Note:** This still runs on YOUR machine. ngrok just creates a secure tunnel to it.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| 🐍 **Backend** | Python 3.9+ • Flask |
| ⬇️ **Downloader** | yt-dlp • FFmpeg |
| 🎨 **Frontend** | HTML5 • CSS3 • Vanilla JavaScript |
| 📡 **Real-time** | Server-Sent Events (SSE) |
| 📦 **Libraries** | requests • curl_cffi • Pillow |

---

## 📁 Project Structure

```
Project-MultiLoader/
├── 📄 app.py              # Flask backend + download engine
├── 🎨 index.html          # Main UI & layout
├── 💎 style.css           # Liquid Glass design system
├── ⚙️ main.js             # Frontend logic & SSE progress
├── 📋 requirements.txt     # Python dependencies
├── 📂 downloads/          # Auto-cleaned temporary storage
└── 📖 README.md           # This file
```

---

## 🔄 How It Works

```
1. Paste URL → 2. Choose Format → 3. Start Download
     ↓              ↓                    ↓
   Get URL    Select Quality      Backend task
     ↓              ↓                    ↓
4. Real-time Progress ← 5. Embed Metadata ← 6. Process File
     ↓
7. Download Complete!
```

**Live Flow:**
- Submit YouTube/Spotify URL
- Backend generates unique `task_id`
- Frontend streams progress via Server-Sent Events
- Metadata & thumbnails auto-embedded
- File ready for download (or ZIP for playlists)

---

## 🎓 Requirements

- **Python 3.9+** (Download: [python.org](https://www.python.org/downloads/))
- **FFmpeg** (Auto-installed, or install manually from [ffmpeg.org](https://ffmpeg.org/download.html))
- **Internet connection** (for downloading)
- **~500MB disk space** (for dependencies)
- **Local machine or personal server** (see hosting warning above)

---

## 🤝 Contributing

Love MultiLoader? **Help us make it even better!** 

### Contribute:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit code improvements
- 📝 Improve documentation

[Read Contributing Guide →](CONTRIBUTING.md)

---

## ⚠️ Legal Disclaimer

This tool is for **personal and educational use only**. 

- Respect YouTube, Spotify, and copyright laws in your country
- Only download content you have permission to download
- The author is not responsible for misuse

---

## 📊 Support

- **Issues:** [Report bugs](https://github.com/ailovegenshinyt/Project-MultiLoader/issues)
- **Discussions:** [Join community](https://github.com/ailovegenshinyt/Project-MultiLoader/discussions)
- **Stars:** Show love with a ⭐

---

## 👤 Creator

**CoR3 Coding-R** — Open source enthusiast  
- GitHub: [@ailovegenshinyt](https://github.com/ailovegenshinyt)

---

## 📄 License

**MIT License** — You're free to use, modify, and share this project.

See [LICENSE](LICENSE) for details.

---

**Made with ❤️ by the Open Source Community**
