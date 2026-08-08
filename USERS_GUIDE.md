# 📖 MultiLoader User Guide — The Real Universal Downloader 😎

Welcome to the official **MultiLoader User Guide**! MultiLoader is equipped with the full power of `yt-dlp`, allowing you to download video and audio from over **1000+ websites** seamlessly.

---

## 🎯 Quick Troubleshooting Checklist ⚠️

> [!IMPORTANT]
> **If a download fails or throws an error:**
> 1. **Update Python:** MultiLoader performs best on **Python 3.10 or Python 3.14**. If you have an older version of Python installed on your computer (e.g. 3.8/3.9), **please upgrade or reinstall Python**!
> 2. **Update yt-dlp:** Websites update their anti-bot protections almost daily. Always keep `yt-dlp` on the latest version by running:
>    ```bash
>    pip install -U yt-dlp -r requirements.txt
>    ```
> 3. **Re-install Requirements:** If you switched or upgraded Python versions, remember to reinstall requirements using `py -m pip install -U -r requirements.txt`.

---

## 🚀 Table of Contents

1. [Getting Started](#getting-started)
2. [YouTube Downloads](#youtube-downloads)
3. [Spotify Downloads](#spotify-downloads)
4. [Instagram Downloads](#instagram-downloads)
5. [TikTok Downloads](#tiktok-downloads)
6. [X (Twitter) & Facebook Downloads](#x-twitter--facebook-downloads)
7. [Reddit & Adult Sites (PornHub, etc.)](#reddit--adult-sites)
8. [1000+ Other Supported Sites](#1000-other-supported-sites)
9. [Ngrok Remote Access Setup](#ngrok-remote-access-setup)
10. [Cookies & Authentication Guide](#cookies--authentication-guide)
11. [Troubleshooting & FAQs](#troubleshooting--faqs)

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/ailovegenshinyt/Project-MultiLoader.git
cd Project-MultiLoader
pip install -U yt-dlp -r requirements.txt
```

### 2. Launching the App
Run the backend with:
```bash
python app.py
# Or if using Windows Launcher:
py app.py
```

### 3. Choose Access Mode
- **Mode [1] Local:** Open `http://localhost:8080` in your web browser.
- **Mode [2] Ngrok:** Public HTTPS URL generated for accessing from mobile phones or external networks.

---

## 🎬 YouTube Downloads

- **Single Videos / Shorts:** Paste any YouTube video or Shorts link (e.g., `https://www.youtube.com/watch?v=...` or `https://youtube.com/shorts/...`). Choose MP4 (up to 4K) or MP3/WAV.
- **Playlists:** Paste a playlist link. MultiLoader will download every track, embed metadata, and pack everything automatically into a downloadable `.zip` file.

---

## 🎵 Spotify Downloads

- **Tracks, Albums & Playlists:** Paste any Spotify link (`https://open.spotify.com/track/...`, `playlist/...`, or `album/...`).
- **How it works:** MultiLoader resolves the track titles, finds the best quality matching stream via `yt-dlp`, downloads it, embeds the album cover art, title, artist name, and ID3 tags, and delivers an MP3 or lossless WAV (or a `.zip` for albums/playlists).

---

## 📸 Instagram Downloads

- **Reels & Posts:** Copy and paste Instagram Post/Reel links directly into MultiLoader.
- **Stories / Private Profiles:** For private accounts or stories, export your browser cookies into `.env` under `INSTAGRAM_COOKIES=./cookies/instagram_cookies.txt` or log in on Chrome/Edge on the host PC for auto-cookie extraction.

---

## 🎵 TikTok Downloads

- **Videos & Slideshows:** Paste any TikTok video URL or short share link (`vm.tiktok.com`).
- **Automatic Browser Cookies:** MultiLoader automatically detects logged-in Chrome or Edge sessions to bypass TikTok rehydration / bot checks natively.

---

## 🐦 X (Twitter) & Facebook Downloads

- **X / Twitter:** Supports tweet videos, GIFs, and media links.
- **Facebook:** Supports public posts, watch videos, and reels. For private groups/videos, configure `FACEBOOK_COOKIES` in your `.env`.

---

## 🤖 Reddit & Adult Sites (PornHub, etc.)

- **Reddit:** Downloads `v.redd.it` videos and automatically merges video and audio streams seamlessly using FFmpeg.
- **PornHub & 18+ Platforms:** Fully supported! Select video format and resolution (1080p, 720p, etc.). For premium-only videos, provide cookies in `.env`.

---

## 🌐 1000+ Other Supported Sites

MultiLoader inherits the universal extractor engine of `yt-dlp`. You can download from:
- **Vimeo**, **Dailymotion**, **Bilibili**, **Twitch Clips/VODs**
- **SoundCloud**, **Bandcamp**, **Mixcloud**
- **NicoNico**, **Streamable**, **Loom**, and 1000+ more!

*If it plays video or audio on the web, MultiLoader can download it!*

---

## 🌐 Ngrok Remote Access Setup

To download videos on your phone using MultiLoader running on your PC:
1. Sign up for free at [ngrok.com](https://ngrok.com).
2. Copy your Auth Token from your Ngrok dashboard.
3. Put `NGROK_AUTHTOKEN=your_token_here` in `.env` OR type it when prompted by `py app.py`.
4. Select Mode `[2]` when launching. Share the `https://xxxx.ngrok-free.dev` link to any phone!

---

## 🍪 Cookies & Authentication Guide

If a site requires login (like private IG accounts or age-gated videos):
1. Install a browser extension like **Get cookies.txt LOCALLY** (Chrome/Firefox).
2. Export your cookies for the target site as a `.txt` file into the `cookies/` folder.
3. In `.env`, set the path to your cookie file:
   ```env
   INSTAGRAM_COOKIES=./cookies/instagram_cookies.txt
   TIKTOK_COOKIES=./cookies/tiktok_cookies.txt
   ```

---

## 🔧 Troubleshooting & FAQs

### ❓ Issue: "Download failed or unable to extract rehydration/data"
- **Solution 1:** Update Python! Make sure you are using Python 3.10+ (or 3.14). Older versions like Python 3.8 have broken SSL/subprocesses.
- **Solution 2:** Update `yt-dlp`: Run `pip install -U yt-dlp`.
- **Solution 3:** Reinstall requirements: Run `py -m pip install -U -r requirements.txt`.

### ❓ Issue: "File not found" when download finishes
- Hard refresh your web browser (`Ctrl + F5` or `Shift + F5`) to clear the cached JavaScript file!

---

**Enjoy the REAL MultiLoader experience! 😎**
