# 🚀 MultiLoader — Universal Multi-Platform Media Downloader 😎

> **The Ultimate Self-Hosted Downloader for YouTube, Spotify, Instagram, TikTok, X (Twitter), Facebook, PornHub & 1000+ Sites!**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B%20%2F%203.14-blue?style=flat-square&logo=python)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Flask](https://img.shields.io/badge/Backend-Flask-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![yt-dlp](https://img.shields.io/badge/Powered%20by-yt--dlp%202026.07%2B-red?style=flat-square)](https://github.com/yt-dlp/yt-dlp)
[![1000+ Sites Supported](https://img.shields.io/badge/Supported--Sites-1000%2B-brightgreen?style=flat-square)](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

---

## ✨ What is MultiLoader?

MultiLoader is a **real, universal, high-performance downloader** built with a **stunning Liquid Glass UI**. Powered by `yt-dlp` under the hood, MultiLoader can grab video and audio from virtually **ANY platform on the internet** — YouTube, Spotify, TikTok, Instagram, X/Twitter, Facebook, Reddit, PornHub, and **1000+ more**!

---

## 💡 CRITICAL NOTE: Update Python & Dependencies First! ⚠️

> [!IMPORTANT]
> **If you encounter ANY extraction errors, failed downloads, or strange backend exceptions:**
> 1. **Update Python:** Ensure you are on **Python 3.10+** (Python 3.14 recommended). If your machine has an older Python version (like 3.8/3.9), **please update or reinstall Python**!
> 2. **Update yt-dlp & Requirements:** Platforms constantly update their anti-bot algorithms. Always run:
>    ```bash
>    pip install -U yt-dlp -r requirements.txt
>    ```
> 3. **Clear old environments:** If you upgraded Python, make sure you reinstall the packages using `py -m pip install -r requirements.txt`.

---

## 🎯 Supported Platforms & Features

| Platform | Supported Content | Notes / Features |
|----------|------------------|------------------|
| 🎬 **YouTube** | Videos, Shorts, Playlists, Channels (up to 4K) | Auto DASH manifest & TV client bypass |
| 🎵 **Spotify** | Tracks, Albums, Playlists | Auto-resolves YouTube streams + Embeds Album Art & ID3 Tags |
| 📸 **Instagram** | Posts, Reels, Stories, IGTV | Auto-detects browser cookies / `.env` cookies support |
| 🎵 **TikTok** | Videos, Slideshows, Audio | Web bypass & auto browser cookies integration |
| 🐦 **X (Twitter)** | Videos, GIFs, Media Tweets | High quality MP4 extraction |
| 📘 **Facebook** | Public Videos, Reels, Watch links | High quality HD stream merger |
| 🤖 **Reddit** | v.redd.it videos & clips | Audio and video merged automatically |
| 🔞 **PornHub** | Full Videos, Clips | Multi-quality selector |
| 🌐 **1000+ Sites** | Vimeo, Dailymotion, Bilibili, Twitch, etc. | Powered by `yt-dlp` universal extractor engine |

---

## 💎 Features

- 🎨 **Liquid Glass UI:** Modern glassmorphism with dynamic live platform badges.
- ⚡ **Real-Time SSE Progress:** Smooth progress bars and live colorized terminal logs.
- 🗜️ **Playlist ZIP Compression:** Downloads multi-track playlists and packs them into a clean `.zip` automatically.
- 🏷️ **Automatic Metadata & Cover Art:** Auto-embeds title, artist, album, and thumbnail cover art into audio files.
- 🌐 **Ngrok Dynamic Tunneling:** Easy one-click remote access setup so you can download from your phone or anywhere.
- 🍪 **Automatic Browser Cookie Support:** Auto-detects Chrome, Edge, Firefox, Brave, and Opera cookies for private/age-gated downloads.

---

## 🚀 Quick Start Guide

### 1️⃣ Requirements
- **Python 3.10+** (Recommended: Python 3.14) -> [Download Python](https://www.python.org/downloads/)
- **FFmpeg** (Auto-installed by MultiLoader, or download from [ffmpeg.org](https://ffmpeg.org/))

### 2️⃣ Installation

```bash
# Clone the repository
git clone https://github.com/ailovegenshinyt/Project-MultiLoader.git
cd Project-MultiLoader

# Install requirements
pip install -r requirements.txt
```

### 3️⃣ Run MultiLoader

```bash
python app.py
# Or on Windows with multiple Python versions:
py app.py
```

Choose **Option [1]** for local network (`http://localhost:8080`) or **Option [2]** for public **Ngrok tunnel**!

---

## 🌐 Remote Access via Ngrok

Want to access MultiLoader from your phone while on mobile data?

1. Add your free Ngrok token into `.env`:
   ```env
   NGROK_AUTHTOKEN=your_token_here
   ```
2. Start MultiLoader (`python app.py`) and select **Option 2**.
3. Open the generated HTTPS URL on any phone or device worldwide!

---

## 📁 Environment Setup (`.env`)

For private accounts or age-gated videos, you can add cookie file paths in `.env`:

```env
# Ngrok Remote Access Token
NGROK_AUTHTOKEN=your_authtoken_here

# Optional: Manual Cookie Paths
YOUTUBE_COOKIES=./cookies/youtube_cookies.txt
SPOTIFY_COOKIES=./cookies/spotify_cookies.txt
INSTAGRAM_COOKIES=./cookies/instagram_cookies.txt
TIKTOK_COOKIES=./cookies/tiktok_cookies.txt
X_COOKIES=./cookies/x_cookies.txt
FACEBOOK_COOKIES=./cookies/facebook_cookies.txt
PORNHUB_COOKIES=./cookies/pornhub_cookies.txt
```

---

## 📄 License & Disclaimer

- **License:** MIT License
- **Disclaimer:** MultiLoader is built for educational and personal archival purposes only. Please respect copyright laws and platform terms of service.

**Made with ❤️ by CoR3 · Zero**
