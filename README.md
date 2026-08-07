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
- **Public URL:** Use ngrok tunnel (optional)

**That's it!** 🎉 Start downloading immediately.

---

## 🌐 Public Mode (Optional)

Want to access MultiLoader from anywhere? Use **ngrok**:

1. Get a free authtoken: [ngrok.com/sign-up](https://dashboard.ngrok.com/get-started/your-authtoken)
2. Set in `.env`:
   ```env
   NGROK_AUTHTOKEN=your_token_here
   ```
3. Run `python app.py` and select **Public Tunnel**

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

---

## 🚧 Roadmap

- ✅ YouTube videos & playlists
- ✅ Spotify tracks & albums
- ✅ Liquid Glass UI
- ⏳ TikTok & Instagram support
- ⏳ Batch download scheduling
- ⏳ Format conversion (MP4→WebM, etc.)
- ⏳ Docker containerization
- ⏳ PyPI package release

[See full roadmap →](ROADMAP.md)

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

## 📊 Stats & Support

- **Stars:** Show love with a ⭐ if this helped you!
- **Issues:** [Report bugs](https://github.com/ailovegenshinyt/Project-MultiLoader/issues)
- **Discussions:** [Join community](https://github.com/ailovegenshinyt/Project-MultiLoader/discussions)

---

## 👤 Creator

**CoR3 Coding-R** — Open source enthusiast  
- GitHub: [@ailovegenshinyt](https://github.com/ailovegenshinyt)
- 🌟 If you like this project, please star it!

---

## 📄 License

**MIT License** — You're free to use, modify, and share this project.

```
Copyright © 2026 MultiLoader Contributors
See LICENSE file for details
```

---

## 🔗 Quick Links

- 📖 [Documentation](CONTRIBUTING.md)
- 🚀 [Roadmap](ROADMAP.md)
- 🐛 [Report Issue](https://github.com/ailovegenshinyt/Project-MultiLoader/issues)
- 💬 [Join Discussion](https://github.com/ailovegenshinyt/Project-MultiLoader/discussions)
- ⭐ [Star on GitHub](https://github.com/ailovegenshinyt/Project-MultiLoader)

---

**Made with ❤️ by the Open Source Community**
