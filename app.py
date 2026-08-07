import os, time, shutil, threading, uuid, re, json, traceback
import subprocess, random, requests
import yt_dlp
from flask import Flask, request, jsonify, send_file, Response

# Load .env for local dev
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Configuration ──────────────────────────────────────────────────────────
app = Flask(__name__, static_folder='.', static_url_path='')
DOWNLOAD_FOLDER = 'downloads'

# --- Clear downloads folder on startup ---
if os.path.exists(DOWNLOAD_FOLDER):
    try:
        shutil.rmtree(DOWNLOAD_FOLDER)
        print("🧹 Startup Cleanup: Old downloads cleared.")
    except Exception as e:
        print(f"⚠️ Startup Cleanup failed: {e}")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

tasks = {}


def _ensure_ffmpeg():
    """Ensure ffmpeg binary is available. Auto-install imageio-ffmpeg if missing from PATH."""
    import sys
    ffmpeg_exe = shutil.which('ffmpeg')
    if ffmpeg_exe:
        return ffmpeg_exe

    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        print("⚙  ffmpeg not found on PATH — auto-installing imageio-ffmpeg...")
        try:
            res = subprocess.run([sys.executable, '-m', 'pip', 'install', 'imageio-ffmpeg', '-q'], capture_output=True, text=True)
            if res.returncode == 0:
                import imageio_ffmpeg
                ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                print("✔  imageio-ffmpeg installed successfully!")
        except Exception as e:
            print(f"⚠️  Could not auto-install imageio-ffmpeg: {e}")

    if ffmpeg_exe and os.path.exists(ffmpeg_exe):
        ffmpeg_dir = os.path.dirname(ffmpeg_exe)
        if ffmpeg_dir not in os.environ.get("PATH", ""):
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
        return ffmpeg_exe

    return 'ffmpeg'


FFMPEG_PATH = _ensure_ffmpeg()


def sanitize_filename(name, max_len=60):
    """Remove/replace characters that are illegal in filenames."""
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    name = name.strip('. ')
    return name[:max_len] if len(name) > max_len else name


def get_youtube_metadata(url):
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={requests.utils.quote(url)}&format=json"
        res = requests.get(oembed_url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return {
                'title': data.get('title'),
                'artist': data.get('author_name'),
                'album': 'YouTube',
                'cover_url': data.get('thumbnail_url')
            }
    except Exception as e:
        print(f"[Meta] Failed YouTube oEmbed: {e}")

    try:
        video_id = None
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0].split('&')[0]
        elif 'v=' in url:
            video_id = url.split('v=')[1].split('&')[0].split('?')[0]
        if video_id:
            return {
                'title': None,
                'artist': None,
                'album': 'YouTube',
                'cover_url': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            }
    except:
        pass
    return None


def embed_metadata(filepath, metadata):
    if not metadata:
        return

    title = metadata.get('title')
    artist = metadata.get('artist')
    album = metadata.get('album', '')
    cover_url = metadata.get('cover_url')

    if not title and not artist:
        return

    base, ext = os.path.splitext(filepath)
    temp_out = base + "_tagged" + ext
    cover_temp = None

    try:
        if cover_url:
            try:
                cover_res = requests.get(cover_url, timeout=10)
                if cover_res.status_code == 200:
                    cover_temp = base + "_cover.jpg"
                    with open(cover_temp, 'wb') as f:
                        f.write(cover_res.content)
            except Exception as e:
                print(f"[Meta] Failed cover download: {e}")

        cmd = [FFMPEG_PATH, '-y', '-i', filepath]
        ext_lower = ext.lower()

        if ext_lower == '.mp3':
            if cover_temp:
                cmd.extend(['-i', cover_temp, '-map', '0:a', '-map', '1:0',
                             '-c:a', 'copy', '-c:v', 'mjpeg', '-id3v2_version', '3'])
            else:
                cmd.extend(['-c:a', 'copy'])
            if title:  cmd.extend(['-metadata', f'title={title}'])
            if artist: cmd.extend(['-metadata', f'artist={artist}'])
            if album:  cmd.extend(['-metadata', f'album={album}'])

        elif ext_lower == '.mp4':
            if cover_temp:
                cmd.extend(['-i', cover_temp, '-map', '0', '-map', '1',
                             '-c', 'copy', '-disposition:v:1', 'attached_pic'])
            else:
                cmd.extend(['-c', 'copy'])
            if title:  cmd.extend(['-metadata', f'title={title}'])
            if artist: cmd.extend(['-metadata', f'artist={artist}'])
            if album:  cmd.extend(['-metadata', f'album={album}'])

        elif ext_lower == '.wav':
            if cover_temp:
                cmd.extend(['-i', cover_temp, '-map', '0:a', '-map', '1:0',
                             '-c:a', 'copy', '-c:v', 'mjpeg', '-write_id3v2', '1'])
            else:
                cmd.extend(['-c:a', 'copy', '-write_id3v2', '1'])
            if title:  cmd.extend(['-metadata', f'title={title}'])
            if artist: cmd.extend(['-metadata', f'artist={artist}'])
            if album:  cmd.extend(['-metadata', f'album={album}'])

        else:
            cmd.extend(['-c', 'copy'])
            if title:  cmd.extend(['-metadata', f'title={title}'])
            if artist: cmd.extend(['-metadata', f'artist={artist}'])
            if album:  cmd.extend(['-metadata', f'album={album}'])

        cmd.append(temp_out)
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            shutil.move(temp_out, filepath)
        else:
            print(f"[ffmpeg] Metadata embed failed (code {result.returncode})")
            if os.path.exists(temp_out):
                os.remove(temp_out)
    except Exception as e:
        print(f"[ffmpeg] Error: {e}")
        if 'temp_out' in dir() and os.path.exists(temp_out):
            os.remove(temp_out)
    finally:
        if cover_temp and os.path.exists(cover_temp):
            os.remove(cover_temp)


# ── Background cleanup (every 5 min) ──────────────────────────────────────
def background_cleanup():
    while True:
        time.sleep(300)
        t = time.time()
        for root, dirs, files in os.walk(DOWNLOAD_FOLDER, topdown=False):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    if os.path.getmtime(fp) < t - 300:
                        os.unlink(fp)
                except:
                    pass
            for d in dirs:
                dp = os.path.join(root, d)
                try:
                    if not os.listdir(dp):
                        os.rmdir(dp)
                except:
                    pass

threading.Thread(target=background_cleanup, daemon=True).start()


# ── Middleware / Hooks ───────────────────────────────────────────────────
@app.after_request
def add_header(response):
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response


# ── Routes ────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_file('index.html')



@app.route('/download', methods=['POST'])
def start_download():
    data = request.json
    url, fmt, quality = data.get('url'), data.get('format'), data.get('quality')
    if not url:
        return jsonify({'error': 'URL required'}), 400

    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        'status': 'processing',
        'logs': [],
        'progress': [],       # structured progress events for UI
        'download_url': None,
        'filename': None
    }

    def emit_log(task, msg):
        """Append a human-readable log line."""
        task['logs'].append(msg)

    def emit_progress(task, ptype, **kwargs):
        """Emit a structured progress event for the progress bar."""
        task['progress'].append(json.dumps({'type': ptype, **kwargs}))

    def run(task_id, url, fmt, quality):
        task = tasks[task_id]

        try:
            # ── Spotify Identity Resolver ──────────────────────────────────
            if 'spotify.com' in url:
                emit_log(task, "🔍 Resolving Spotify track identity...")
                search_query = ""
                try:
                    track_id = url.split('track/')[1].split('?')[0]
                    api_url = f"https://api.spotifydown.com/metadata/track/{track_id}"
                    sp_headers = {
                        "Origin": "https://spotifydown.com",
                        "Referer": "https://spotifydown.com/",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                    res = requests.get(api_url, headers=sp_headers, timeout=15)
                    if res.status_code == 200:
                        sdata = res.json()
                        if sdata.get('success'):
                            title  = sdata.get('title', 'Unknown')
                            artist = sdata.get('artists', sdata.get('artist', 'Unknown'))
                            album  = sdata.get('album', 'Unknown')
                            cover  = sdata.get('cover', sdata.get('cover_url', ''))
                            task['metadata'] = {
                                'title': title, 'artist': artist,
                                'album': album, 'cover_url': cover
                            }
                            search_query = f"{title} {artist}".strip()
                            emit_log(task, f"✅ Identified: {title} — {artist}")
                        else:
                            raise Exception("Metadata API returned no success.")
                    else:
                        raise Exception(f"Metadata API Status {res.status_code}")

                except Exception as e:
                    emit_log(task, f"⚠️ Spotify metadata fallback: {e}")
                    try:
                        o_res = requests.get(f"https://open.spotify.com/oembed?url={url}", timeout=10)
                        if o_res.status_code == 200:
                            o_data = o_res.json()
                            raw_title = o_data.get('title', 'Unknown')
                            thumbnail = o_data.get('thumbnail_url', '')
                            author    = o_data.get('author_name', '')
                            if ' - ' in raw_title:
                                parts = raw_title.rsplit(' - ', 1)
                                clean_title  = parts[0].strip()
                                clean_artist = parts[1].strip() if not author else author
                            else:
                                clean_title  = raw_title
                                clean_artist = author if author else 'Unknown Artist'
                            task['metadata'] = {
                                'title': clean_title, 'artist': clean_artist,
                                'album': 'Spotify', 'cover_url': thumbnail
                            }
                            search_query = f"{clean_title} {clean_artist}".strip()
                    except:
                        pass

                if not search_query:
                    raise Exception("Could not identify Spotify track. Please check the link.")

                url = f"ytsearch1:{search_query}"
                emit_log(task, f"🔀 Redirecting to YouTube: {search_query}")

            elif 'youtube.com' in url or 'youtu.be' in url:
                yt_meta = get_youtube_metadata(url)
                if yt_meta:
                    task['metadata'] = yt_meta

            # ── Detect playlist vs single ─────────────────────────────────
            is_playlist = ('list=' in url or '/playlist' in url) and 'spotify.com' not in url

            # ── Build yt-dlp options ──────────────────────────────────────
            abs_download_path = os.path.abspath(DOWNLOAD_FOLDER)
            temp_dir_name = f"yt_{int(time.time())}_{uuid.uuid4().hex[:6]}"
            temp_dir = os.path.join(abs_download_path, temp_dir_name)
            os.makedirs(temp_dir, exist_ok=True)

            ext_label = 'mp3' if fmt == 'audio' else ('wav' if fmt == 'wav' else 'mp4')

            # Track playlist progress counters
            playlist_state = {'current': 0, 'total': 0, 'current_title': ''}

            def progress_hook(d):
                if d['status'] == 'downloading':
                    title = d.get('info_dict', {}).get('title', 'Unknown')
                    playlist_state['current_title'] = title
                    downloaded = d.get('downloaded_bytes', 0) or 0
                    total_b    = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
                    pct = min(int((downloaded / total_b) * 100), 99)

                    n     = playlist_state['current']
                    total = playlist_state['total'] or 1

                    emit_progress(task, 'downloading',
                                  title=title, percent=pct,
                                  n=n, total=total)

                elif d['status'] == 'finished':
                    title = d.get('info_dict', {}).get('title', 'Unknown')
                    playlist_state['current'] += 1
                    n     = playlist_state['current']
                    total = playlist_state['total'] or 1
                    emit_log(task, f"⬇️  Downloaded: {title}")
                    emit_progress(task, 'downloaded', title=title, n=n, total=total)

            def pp_hook(d):
                stage = d.get('postprocessor', '')
                title = playlist_state['current_title'] or 'track'
                n     = playlist_state['current']
                total = playlist_state['total'] or 1

                if d['status'] == 'started':
                    if stage == 'EmbedThumbnail':
                        emit_log(task, f"🖼️  Embedding Thumbnail: {title}")
                        emit_progress(task, 'postprocess', stage='EmbedThumbnail',
                                      label='Embedding Thumbnail', n=n, total=total)
                    elif stage == 'FFmpegMetadata':
                        emit_log(task, f"🏷️  Writing Tags: {title}")
                        emit_progress(task, 'postprocess', stage='Metadata',
                                      label='Writing Tags', n=n, total=total)
                    elif stage == 'FFmpegExtractAudio':
                        emit_log(task, f"🎵  Converting to {ext_label.upper()}: {title}")
                        emit_progress(task, 'postprocess', stage='ExtractAudio',
                                      label=f'Converting to {ext_label.upper()}', n=n, total=total)

            ydl_opts = {
                'ffmpeg_location': FFMPEG_PATH,
                'outtmpl': os.path.join(temp_dir, '%(playlist_index)s - %(title)s.%(ext)s'
                                        if is_playlist else '%(title)s.%(ext)s'),
                'cookiefile': 'cookies.txt', 
                'quiet': True, 'no_warnings': True,
                'user_agent': random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
                ]),
                'progress_hooks': [progress_hook],
                'postprocessor_hooks': [pp_hook],
                'overwrites': True, 'nooverwrites': False,
                'nocheckcertificate': True,
                'cache_dir': False,
                'legacy_server_connect': True,
                'retries': 5,
                'fragment_retries': 5,
                'socket_timeout': 20,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['tv_embedded', 'ios', 'android', 'web'],
                    }
                },
                'youtube_include_dash_manifest': True,
            }

            if fmt == 'video':
                res = {'4k': '2160', '1080p': '1080', '720p': '720', '480p': '480'}.get(quality, '1080')
                ydl_opts['format'] = f'bestvideo[height<={res}]+bestaudio/bestvideo+bestaudio/best/bestaudio'
                ydl_opts['merge_output_format'] = 'mp4'
                ydl_opts['writethumbnail'] = True
                ydl_opts['postprocessors'] = [{'key': 'FFmpegMetadata'}, {'key': 'EmbedThumbnail'}]
            else:
                br = {'4k': '320', '1080p': '256', '720p': '192', '480p': '128'}.get(quality, '320')
                ext = 'mp3' if fmt == 'audio' else 'wav'
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [
                    {'key': 'FFmpegExtractAudio', 'preferredcodec': ext, 'preferredquality': br},
                    {'key': 'FFmpegMetadata'},
                    {'key': 'EmbedThumbnail'},
                ]

            # Pre-extract info to get playlist total count
            emit_log(task, "🔌 Connecting to source...")
            emit_progress(task, 'connecting')

            try:
                with yt_dlp.YoutubeDL({**ydl_opts, 'quiet': True, 'extract_flat': 'in_playlist'}) as ydl_flat:
                    flat_info = ydl_flat.extract_info(url, download=False)
                    entries = flat_info.get('entries') if flat_info else []
                    playlist_state['total'] = len(entries) if entries else 1
                    playlist_state['current'] = 0
                    playlist_title = flat_info.get('title', 'Playlist') if flat_info else 'Playlist'
            except Exception:
                playlist_state['total'] = 1
                playlist_title = 'Playlist'

            total = playlist_state['total']
            if total > 1:
                emit_log(task, f"📋 Playlist: {playlist_title} ({total} tracks)")
            else:
                emit_log(task, f"🎯 Starting download...")

            # ── Actual download ───────────────────────────────────────────
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

            all_found = [f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]

            entries = (info or {}).get('entries', []) if info else []
            is_multi = len(entries) > 1 or total > 1

            if is_multi:
                # ── Playlist → ZIP ────────────────────────────────────────
                safe_title = sanitize_filename(playlist_title)
                zip_name = safe_title if safe_title else f"Playlist_{int(time.time())}"

                emit_log(task, f"🗜️  Compressing Playlist: {playlist_title}...")
                emit_progress(task, 'compressing', label='Compressing Playlist...')

                # Build zip to a staging path OUTSIDE the Flask-watched folder
                # to avoid triggering the debug reloader
                staging_zip = os.path.join(abs_download_path, f"_staging_{uuid.uuid4().hex[:8]}")
                shutil.make_archive(staging_zip, 'zip', temp_dir)

                final_zip_path = os.path.join(abs_download_path, f"{zip_name}.zip")
                # If name conflicts, add a suffix
                if os.path.exists(final_zip_path):
                    final_zip_path = os.path.join(abs_download_path, f"{zip_name}_{int(time.time())}.zip")
                    zip_name = f"{zip_name}_{int(time.time())}"

                shutil.move(f"{staging_zip}.zip", final_zip_path)

                task['filename']     = f"{zip_name}.zip"
                task['download_url'] = f"/files/{zip_name}.zip"
                emit_log(task, f"✅ Playlist ready: {zip_name}.zip")

            else:
                # ── Single file ───────────────────────────────────────────
                if all_found:
                    final_filename = max(all_found, key=lambda f: os.path.getsize(os.path.join(temp_dir, f)))
                    dest = os.path.join(abs_download_path, final_filename)
                    shutil.move(os.path.join(temp_dir, final_filename), dest)
                    task['filename']     = final_filename
                    task['download_url'] = f"/files/{final_filename}"
                    emit_log(task, f"✅ Done! {final_filename}")
                else:
                    raise Exception(f"Download finished but no files found in {temp_dir}")

            # Cleanup temp dir
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

            # Embed metadata for non-video single files (yt-dlp handles video itself)
            if fmt != 'video' and task.get('filename') and not task['filename'].endswith('.zip'):
                filepath = os.path.join(abs_download_path, task['filename'])
                if os.path.exists(filepath):
                    meta = task.get('metadata', {})
                    if not meta.get('title'):
                        clean_title = os.path.splitext(task['filename'])[0]
                        clean_title = re.sub(r'\s*\[[a-zA-Z0-9_-]{11}\\]$', '', clean_title)
                        meta['title'] = clean_title
                    if not meta.get('artist'):
                        meta['artist'] = 'MultiLoader'
                    embed_metadata(filepath, meta)

            emit_progress(task, 'completed')
            task['status'] = 'completed'

        except Exception as e:
            traceback.print_exc()
            task['status'] = 'error'
            task['error'] = str(e)
            emit_log(task, f"❌ Error: {e}")

    threading.Thread(target=run, args=(task_id, url, fmt, quality), daemon=True).start()
    return jsonify({'task_id': task_id})


@app.route('/progress/<task_id>')
def progress(task_id):
    def generate():
        log_idx  = 0
        prog_idx = 0
        while True:
            task = tasks.get(task_id)
            if not task:
                break

            # Send pending log lines
            while log_idx < len(task['logs']):
                yield f"event: log\ndata: {task['logs'][log_idx]}\n\n"
                log_idx += 1

            # Send pending progress events
            while prog_idx < len(task['progress']):
                yield f"event: progress\ndata: {task['progress'][prog_idx]}\n\n"
                prog_idx += 1

            if task['status'] == 'completed':
                yield f"event: completed\ndata: {json.dumps({'download_url': task['download_url'], 'filename': task['filename']})}\n\n"
                break
            if task['status'] == 'error':
                yield f"event: error\ndata: {task['error']}\n\n"
                break

            time.sleep(0.3)

    return Response(generate(), mimetype='text/event-stream')


@app.route('/files/<path:filename>')
def serve_file(filename):
    fp = os.path.join(DOWNLOAD_FOLDER, filename)
    if not os.path.exists(fp):
        for root, _, files in os.walk(DOWNLOAD_FOLDER):
            if filename in files:
                fp = os.path.join(root, filename)
                break
    return send_file(fp, as_attachment=True, download_name=filename) if os.path.exists(fp) else ("File not found", 404)



# ── Terminal Colors (Windows VT100 auto-enable) ───────────────────────────────
def _enable_ansi():
    """Force Windows CMD to interpret ANSI escape codes."""
    if os.name == 'nt':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            pass

_enable_ansi()

# ANSI shortcuts
_R  = '\033[0m'
_B  = '\033[1m'          # Bold
_DM = '\033[2m'          # Dim
_MG = '\033[95m'         # Bright Magenta
_CY = '\033[96m'         # Bright Cyan
_GN = '\033[92m'         # Bright Green
_YL = '\033[93m'         # Bright Yellow
_RD = '\033[91m'         # Bright Red
_BL = '\033[94m'         # Bright Blue
_GY = '\033[90m'         # Dark Gray


def _c(color, text, bold=False):
    prefix = _B if bold else ''
    return f"{prefix}{color}{text}{_R}"


def print_banner():
    lines = [
        r"  ███╗   ███╗██╗   ██╗██╗  ████████╗██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ ",
        r"  ████╗ ████║██║   ██║██║  ╚══██╔══╝██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗",
        r"  ██╔████╔██║██║   ██║██║     ██║   ██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝",
        r"  ██║╚██╔╝██║██║   ██║██║     ██║   ██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗",
        r"  ██║ ╚═╝ ██║╚██████╔╝███████╗██║   ███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║",
        r"  ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝",
    ]
    # Gradient: magenta → cyan across lines
    colors = [_MG, _MG, '\033[38;5;171m', '\033[38;5;135m', _CY, _CY]
    print()
    for line, color in zip(lines, colors):
        print(f"{_B}{color}{line}{_R}")
    print()
    tag_line = (
        f"  {_GY}◈{_R}  "
        f"{_c(_CY,'Premium Video & Music Downloader')}  "
        f"{_GY}|{_R}  "
        f"{_c(_MG,'YouTube')} {_GY}•{_R} {_c(_GN,'Spotify')}  "
        f"{_GY}|{_R}  "
        f"{_c(_YL,'4K & Playlist Support')}"
        f"  {_GY}◈{_R}"
    )
    print(tag_line)
    print()
    print(f"  {_GY}{'─' * 78}{_R}")
    print()


def startup_menu():
    """Interactive startup menu — choose Local or Ngrok access mode."""
    print_banner()

    W = 46
    border_color = _CY
    print(f"  {_B}{border_color}╔{'═' * W}╗{_R}")
    print(f"  {_B}{border_color}║{'  🚀  ACCESS MODE SETUP  '.center(W)}║{_R}")
    print(f"  {_B}{border_color}╠{'═' * W}╣{_R}")
    print(f"  {_B}{border_color}║{_R}  {_c(_GN,'[1]',True)}  {_c(_YL,'🏠  Local Only')}"
          f"{'':12}{_GY}localhost:8080{_R}      {_B}{border_color}║{_R}")
    print(f"  {_B}{border_color}║{_R}  {_c(_GN,'[2]',True)}  {_c(_MG,'🌐  Ngrok Tunnel')}"
          f"{'':10}{_GY}public URL anywhere{_R} {_B}{border_color}║{_R}")
    print(f"  {_B}{border_color}╚{'═' * W}╝{_R}")
    print()

    while True:
        try:
            choice = input(f"  {_B}{_CY}❯ Choose mode [1/2]:{_R} ").strip()
        except (EOFError, KeyboardInterrupt):
            choice = '1'

        if choice == '1':
            return 'local'
        elif choice == '2':
            return 'ngrok'
        else:
            print(f"  {_RD}⚠  Invalid choice. Please enter 1 or 2.{_R}")


def _ensure_pyngrok():
    """Try to import pyngrok, auto-install if missing, return module or None."""
    try:
        import importlib.util
        if importlib.util.find_spec("pyngrok") is None:
            raise ImportError("not installed")
        from pyngrok import ngrok
        return ngrok
    except ImportError:
        print(f"\n  {_YL}⚙  pyngrok not found — auto-installing...{_R}")
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', 'pyngrok', '-q'],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  {_RD}❌  Install failed:{_R} {result.stderr.strip()}")
            return None
        try:
            from pyngrok import ngrok
            print(f"  {_GN}✔  pyngrok installed successfully!{_R}")
            return ngrok
        except ImportError as e:
            print(f"  {_RD}❌  Still cannot import pyngrok: {e}{_R}")
            return None


if __name__ == '__main__':
    import sys
    PORT = 8080

    mode = startup_menu()

    if mode == 'ngrok':
        ngrok = _ensure_pyngrok()

        if ngrok is None:
            print(f"\n  {_YL}⚠  Falling back to Local mode.{_R}\n")
        else:
            try:
                authtoken = os.environ.get("NGROK_AUTHTOKEN", "").strip()
                if authtoken.upper() in ["YOUR_NGROK_AUTHTOKEN", "YOUR_AUTHTOKEN", ""]:
                    authtoken = ""

                if not authtoken:
                    print(f"\n  {_CY}🔑  Ngrok Authtoken setup (for unique dynamic URLs):{_R}")
                    print(f"  {_GY}    Tip: Add NGROK_AUTHTOKEN=your_token to your .env file to skip this step!{_R}")
                    print(f"  {_GY}    Get your free token at: https://dashboard.ngrok.com/get-started/your-authtoken{_R}")
                    try:
                        authtoken = input(f"  {_B}{_CY}❯ Enter your Ngrok Auth Token (or press Enter to use saved system token):{_R} ").strip()
                    except (EOFError, KeyboardInterrupt):
                        authtoken = ""

                if authtoken:
                    print(f"\n  {_CY}⚙  Authenticating with ngrok...{_R}")
                    ngrok.set_auth_token(authtoken)

                print(f"  {_CY}🔌  Opening unique tunnel on port {PORT}...{_R}")
                tunnel = ngrok.connect(PORT)
                public_url = tunnel.public_url

                pad = 40
                url_display = public_url.ljust(pad)
                print()
                print(f"  {_B}{_GN}╔{'═' * (pad + 22)}╗{_R}")
                print(f"  {_B}{_GN}║{'':3}🌐  NGROK TUNNEL ACTIVE{'':{pad - 1}}║{_R}")
                print(f"  {_B}{_GN}╠{'═' * (pad + 22)}╣{_R}")
                print(f"  {_B}{_GN}║{_R}  {_GY}Public URL :{_R}  {_B}{_CY}{url_display}{_R}  {_B}{_GN}║{_R}")
                print(f"  {_B}{_GN}║{_R}  {_GY}Local URL  :{_R}  {_GY}http://localhost:{PORT}{' ' * (pad - 13)}{_B}{_GN}║{_R}")
                print(f"  {_B}{_GN}╚{'═' * (pad + 22)}╝{_R}")
                print()
                print(f"  {_GY}Share the public URL above to access MultiLoader from anywhere.{_R}")
                print(f"  {_GY}Press Ctrl+C to stop the server and disconnect the tunnel.{_R}")
                print()

            except Exception as e:
                import traceback
                print(f"\n  {_RD}❌  Ngrok error: {e}{_R}")
                traceback.print_exc()
                print(f"  {_YL}⚠  Falling back to Local mode.{_R}\n")
    else:
        print()
        print(f"  {_GN}✔  Starting in Local mode →  {_B}{_CY}http://localhost:{PORT}{_R}")
        print()

    print(f"  {_GY}{'─' * 78}{_R}")
    print()

    # use_reloader=False is CRITICAL — prevents Flask from restarting when a
    # zip/mp3 is written to disk, which would wipe the downloads folder.
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)
