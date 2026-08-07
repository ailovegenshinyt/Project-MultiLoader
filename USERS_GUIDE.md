# 📖 MultiLoader User Guide

Complete guide to downloading videos & music with MultiLoader.

---

## 🎯 Table of Contents

1. [Getting Started](#getting-started)
2. [YouTube Downloads](#youtube-downloads)
3. [Spotify Downloads](#spotify-downloads)
4. [Format & Quality Options](#format--quality-options)
5. [Troubleshooting](#troubleshooting)
6. [Tips & Tricks](#tips--tricks)

---

## 🚀 Getting Started

### Installation

```bash
git clone https://github.com/ailovegenshinyt/Project-MultiLoader.git
cd Project-MultiLoader
pip install -r requirements.txt
python app.py
```

### First Run

1. Open **http://localhost:8080** in your browser
2. You'll see the beautiful Liquid Glass UI
3. Paste a YouTube or Spotify URL
4. Select format & quality
5. Click Download & watch the magic happen ✨

---

## 🎬 YouTube Downloads

### Single Videos

1. Copy a YouTube video URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
2. Paste into MultiLoader
3. Choose:
   - **Format:** MP4 (video) or MP3 (audio)
   - **Quality:** 4K, 1080p, 720p, 480p, 360p
4. Click Download
5. File appears in your browser automatically 🎉

### Playlists

1. Copy playlist URL: `https://www.youtube.com/playlist?list=PLxxxxxx`
2. Paste into MultiLoader
3. All videos in the playlist will be downloaded
4. **Audio playlists** → Downloaded as ZIP file
5. **Video playlists** → Each video separate (or ZIP)

### Best Quality

- **4K (2160p):** Best visuals, ~500MB per video
- **1080p:** Great balance, ~300MB per video
- **720p:** Recommended for most users, ~150MB per video
- **480p:** Mobile-friendly, ~80MB per video

---

## 🎵 Spotify Downloads

### Single Tracks

1. Find track on Spotify: Open in app or copy link
2. Copy URL: `https://open.spotify.com/track/xxxxxxx`
3. Paste into MultiLoader
4. Choose format: **MP3** or **WAV**
5. Download
6. File includes: **Title, Artist, Album, Cover Art** ✨

### Albums

1. Copy album link: `https://open.spotify.com/album/xxxxxxx`
2. Paste into MultiLoader
3. All tracks download as a single ZIP
4. Each track has full metadata embedded

### Playlists

1. Copy playlist: `https://open.spotify.com/playlist/xxxxxxx`
2. Download as ZIP with all tracks
3. Perfect for backup or offline listening

**How it works:** Spotify tracks are found on YouTube, downloaded, and metadata is embedded automatically.

---

## 🎚️ Format & Quality Options

### Video Formats

| Quality | Size | Best For | Example |
|---------|------|----------|----------|
| **4K (2160p)** | 500MB+ | Archival, high-end displays | 4K monitors, TVs |
| **1080p** | 300MB | General purpose | Most laptops |
| **720p** | 150MB | Good balance | Tablets, older laptops |
| **480p** | 80MB | Mobile, streaming | Phones, slow internet |
| **360p** | 40MB | Emergency only | Ultra-slow internet |

### Audio Formats

| Format | Bitrate | Quality | File Size (3 min song) |
|--------|---------|---------|------------------------|
| **MP3** | 320 kbps | High quality | ~7.5 MB |
| **MP3** | 256 kbps | Good quality | ~6 MB |
| **MP3** | 192 kbps | Standard | ~4.5 MB |
| **MP3** | 128 kbps | Basic | ~3 MB |
| **WAV** | Lossless | Perfect quality | ~30 MB |

**Recommendation:** 
- YouTube music → 256 kbps MP3
- Spotify tracks → 320 kbps MP3
- Archiving → WAV

---

## 🔧 Troubleshooting

### "Download not starting"
- Check internet connection
- Verify URL is correct
- Try a different video/track
- Refresh the page

### "Video not found"
- URL may be private or region-locked
- Try a different video
- Check if video still exists on YouTube

### "Audio quality poor"
- Choose higher bitrate (256+ kbps)
- Spotify audio quality depends on YouTube version found
- Try different source if available

### "Large file sizes"
- For video: Choose lower quality (720p instead of 1080p)
- For audio: Use 192 kbps MP3 instead of 320 kbps
- Store on external drive if low on space

### "Slow downloads"
- Check internet speed
- Try during off-peak hours
- Close other bandwidth-heavy apps

### "Permission errors"
- Make sure you have write permissions to downloads folder
- Try running from a different directory

---

## 💡 Tips & Tricks

### Pro Tips

✅ **Batch Downloads:** Paste multiple URLs and download sequentially
✅ **Playlist Organization:** Downloaded playlists auto-organize by artist
✅ **Metadata Accuracy:** Album art & info auto-embed for audio files
✅ **Storage:** Downloads auto-cleanup after 5 minutes (configurable)
✅ **Offline Access:** Use ngrok to share download link publicly

### Keyboard Shortcuts

- `Ctrl+V` → Paste URL
- `Enter` → Start download (when URL pasted)
- `Esc` → Cancel download

### Storage Management

```
Default download folder: ./downloads/
Max folder size: No limit (you control cleanup)
Auto-cleanup: Every 5 minutes
Retention: Configure in app.py
```

### Performance Tips

1. **Limit concurrent downloads** → Download one at a time
2. **Off-peak hours** → Faster downloads at night
3. **Wired connection** → More stable than WiFi
4. **Close browser tabs** → Reduces resource usage

---

## ⚠️ Legal & Ethical Use

✅ **OK to download:**
- Videos you own or created
- Content with explicit permission
- Personal backup of your content
- Educational/research purposes

❌ **Not OK to download:**
- Copyrighted content without permission
- Commercial redistribution
- Circumventing DRM protections (in some countries)

**Always respect creators' rights and your local laws.**

---

## 📞 Need Help?

- 💬 [Ask Questions](https://github.com/ailovegenshinyt/Project-MultiLoader/discussions)
- 🐛 [Report Issues](https://github.com/ailovegenshinyt/Project-MultiLoader/issues)
- 📖 [Read Docs](https://github.com/ailovegenshinyt/Project-MultiLoader#readme)
- 🚀 [Check Roadmap](https://github.com/ailovegenshinyt/Project-MultiLoader/blob/main/ROADMAP.md)

---

**Happy downloading!** 🎉
