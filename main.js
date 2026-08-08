document.addEventListener('DOMContentLoaded', () => {
    const downloadBtn  = document.getElementById('downloadBtn');
    const urlInput     = document.getElementById('urlInput');
    const progressArea = document.getElementById('progressArea');
    const progressBar  = document.getElementById('progressBar');
    const progressPct  = document.getElementById('progressPct');
    const progressTrack = document.getElementById('progressTrack');
    const statusIcon   = document.getElementById('statusIcon');
    const statusText   = document.getElementById('statusText');
    const terminalBody = document.getElementById('terminalBody');
    const platformIndicator = document.getElementById('platformIndicator');

    // ── Platform Detection ──────────────────────────────────────────────
    const PLATFORMS = [
        { pattern: /youtube\.com|youtu\.be/i,          name: 'YouTube',      emoji: '🎬', color: '#FF0000' },
        { pattern: /spotify\.com/i,                    name: 'Spotify',      emoji: '🎵', color: '#1DB954' },
        { pattern: /instagram\.com|instagr\.am/i,      name: 'Instagram',    emoji: '📸', color: '#E4405F' },
        { pattern: /tiktok\.com|vm\.tiktok\.com/i,     name: 'TikTok',       emoji: '🎵', color: '#000000' },
        { pattern: /twitter\.com|x\.com|t\.co/i,       name: 'X (Twitter)',  emoji: '🐦', color: '#1DA1F2' },
        { pattern: /facebook\.com|fb\.watch/i,         name: 'Facebook',     emoji: '📘', color: '#1877F2' },
        { pattern: /reddit\.com|redd\.it/i,            name: 'Reddit',       emoji: '🤖', color: '#FF4500' },
        { pattern: /pornhub\.com/i,                    name: 'PornHub',      emoji: '🔞', color: '#FFA31A' },
        { pattern: /vimeo\.com/i,                      name: 'Vimeo',        emoji: '🎥', color: '#1AB7EA' },
        { pattern: /soundcloud\.com/i,                 name: 'SoundCloud',   emoji: '🔊', color: '#FF5500' },
        { pattern: /twitch\.tv/i,                      name: 'Twitch',       emoji: '🟣', color: '#9146FF' },
        { pattern: /dailymotion\.com/i,                name: 'Dailymotion',  emoji: '📺', color: '#0066DC' },
        { pattern: /bilibili\.com|b23\.tv/i,           name: 'Bilibili',     emoji: '📺', color: '#00A1D6' },
        { pattern: /pinterest\.com/i,                  name: 'Pinterest',    emoji: '📌', color: '#BD081C' },
        { pattern: /tumblr\.com/i,                     name: 'Tumblr',       emoji: '📝', color: '#36465D' },
        { pattern: /snapchat\.com/i,                   name: 'Snapchat',     emoji: '👻', color: '#FFFC00' },
        { pattern: /linkedin\.com/i,                   name: 'LinkedIn',     emoji: '💼', color: '#0A66C2' },
        { pattern: /bandcamp\.com/i,                   name: 'Bandcamp',     emoji: '🎸', color: '#629AA9' },
        { pattern: /mixcloud\.com/i,                   name: 'Mixcloud',     emoji: '🎧', color: '#5000FF' },
        { pattern: /nicovideo\.jp|nico\.ms/i,          name: 'NicoNico',     emoji: '📺', color: '#252525' },
    ];

    function detectPlatform(url) {
        for (const p of PLATFORMS) {
            if (p.pattern.test(url)) return p;
        }
        if (url.startsWith('http://') || url.startsWith('https://')) {
            return { name: 'Website', emoji: '🌐', color: '#8b5cf6' };
        }
        return null;
    }

    let platformDebounce = null;
    urlInput.addEventListener('input', () => {
        clearTimeout(platformDebounce);
        platformDebounce = setTimeout(() => {
            const url = urlInput.value.trim();
            if (!url) {
                platformIndicator.style.display = 'none';
                return;
            }
            const p = detectPlatform(url);
            if (p) {
                platformIndicator.innerHTML = `<span class="platform-dot" style="background:${p.color}"></span> ${p.emoji} ${p.name}`;
                platformIndicator.style.display = 'flex';
                platformIndicator.style.borderColor = p.color + '40';
            } else {
                platformIndicator.style.display = 'none';
            }
        }, 300);
    });

    // ── Helpers ──────────────────────────────────────────────────────────
    function setProgress(pct, animated = true) {
        const clamped = Math.min(Math.max(pct, 0), 100);
        progressBar.style.width = `${clamped}%`;
        progressPct.textContent = `${Math.round(clamped)}%`;
        if (animated) {
            progressBar.classList.add('active');
        } else {
            progressBar.classList.remove('active');
        }
    }

    function setStatus(icon, text) {
        statusIcon.textContent = icon;
        statusText.textContent = text;
    }

    function setTrackLabel(n, total) {
        if (total > 1) {
            progressTrack.textContent = `Track ${n} / ${total}`;
        } else {
            progressTrack.textContent = '';
        }
    }

    function appendLog(text, cls = '') {
        const d = document.createElement('div');
        d.textContent = text;
        if (cls) d.className = cls;
        terminalBody.appendChild(d);
        terminalBody.scrollTop = terminalBody.scrollHeight;
    }

    function resetUI() {
        setProgress(0);
        setStatus('⏳', 'Preparing...');
        progressTrack.textContent = '';
        terminalBody.innerHTML = '<div>▸ MultiLoader Engine started</div>';
        progressArea.style.display = 'block';
    }

    // ── Validation ───────────────────────────────────────────────────────
    function isValidUrl(url) {
        // Accept any HTTP(S) URL — yt-dlp supports 1000+ sites
        return url.startsWith('http://') || url.startsWith('https://');
    }

    // ── Download Flow ─────────────────────────────────────────────────────
    async function startDownload(url) {
        const fmt     = document.getElementById('formatSelect').value;
        const quality = document.getElementById('qualitySelect').value;

        downloadBtn.disabled    = true;
        downloadBtn.textContent = 'Processing...';
        resetUI();

        try {
            const res = await fetch('/download', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'ngrok-skip-browser-warning': 'true'
                },
                body: JSON.stringify({ url, format: fmt, quality }),
            });
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.error || 'Failed to start task');
            }

            const { task_id } = await res.json();
            listenToProgress(task_id);

        } catch (err) {
            console.error(err);
            appendLog(`> ERROR: ${err.message}`, 'log-error');
            setStatus('❌', `Error: ${err.message}`);
            downloadBtn.disabled    = false;
            downloadBtn.textContent = 'Try Again';
        }
    }

    function listenToProgress(task_id) {
        const sse = new EventSource(`/progress/${task_id}`);

        // ── Log events: append to terminal ───────────────────────────────
        sse.addEventListener('log', e => {
            const text = e.data;
            let cls = '';
            if (text.startsWith('❌') || text.toLowerCase().startsWith('error')) cls = 'log-error';
            if (text.startsWith('✅')) cls = 'log-done';
            appendLog(text, cls);
        });

        // ── Progress events: drive the bar ───────────────────────────────
        sse.addEventListener('progress', e => {
            let d;
            try { d = JSON.parse(e.data); } catch { return; }

            const type  = d.type;
            const n     = d.n     || 0;
            const total = d.total || 1;
            const title = d.title || '';

            switch (type) {

                case 'connecting':
                    setStatus('🔌', 'Connecting...');
                    setProgress(2);
                    break;

                case 'downloading': {
                    // Per-track download percent mapped into that track's slice
                    // Each track gets an equal slice of 0–85% of the bar
                    const trackPct = d.percent || 0;          // 0-99 within the track
                    const sliceSize = total > 0 ? 85 / total : 85;
                    const base = total > 1 ? ((n - 1) / total) * 85 : 0;
                    const fill = base + (trackPct / 100) * sliceSize;

                    setProgress(Math.max(fill, 3));
                    setTrackLabel(n, total);

                    const label = title
                        ? (total > 1 ? `⬇️  [${n}/${total}] ${title}` : `⬇️  ${title}`)
                        : '⬇️  Downloading...';
                    setStatus('⬇️', total > 1 ? `[${n}/${total}] ${title}` : title || 'Downloading...');
                    break;
                }

                case 'downloaded': {
                    // A track just finished downloading — snap to that track's boundary
                    const sliceSize = total > 0 ? 85 / total : 85;
                    const filled = total > 1 ? (n / total) * 85 : 60;
                    setProgress(filled);
                    setTrackLabel(n, total);
                    break;
                }

                case 'postprocess': {
                    const stage = d.stage || '';
                    const label = d.label || stage;
                    const sliceSize = total > 0 ? 85 / total : 85;
                    const base = total > 1 ? ((n - 1) / total) * 85 : 0;

                    let extraPct = 0;
                    if (stage === 'ExtractAudio')  extraPct = sliceSize * 0.4;
                    if (stage === 'Metadata')       extraPct = sliceSize * 0.7;
                    if (stage === 'EmbedThumbnail') extraPct = sliceSize * 0.9;

                    setProgress(Math.min(base + extraPct + (total > 1 ? 0 : 60), 92));
                    setStatus(
                        stage === 'EmbedThumbnail' ? '🖼️' :
                        stage === 'Metadata'       ? '🏷️' :
                        stage === 'ExtractAudio'   ? '🎵' : '⚙️',
                        title ? `${label}: ${title}` : label
                    );
                    break;
                }

                case 'compressing':
                    setProgress(93);
                    setStatus('🗜️', 'Compressing Playlist...');
                    progressBar.classList.add('active');
                    break;

                case 'completed':
                    // handled in 'completed' SSE event
                    break;
            }
        });

        // ── Completed ────────────────────────────────────────────────────
        sse.addEventListener('completed', e => {
            sse.close();
            const result = JSON.parse(e.data);

            setProgress(100, false);
            setStatus('✅', `Done! ${result.filename}`);
            progressTrack.textContent = '';
            appendLog(`✅ Ready: ${result.filename}`, 'log-done');

            // Trigger download
            setTimeout(() => {
                window.location.href = '/files/' + encodeURIComponent(result.filename);
                downloadBtn.disabled    = false;
                downloadBtn.textContent = 'Start New Download';
            }, 800);
        });

        // ── Error ────────────────────────────────────────────────────────
        sse.addEventListener('error', e => {
            if (e.data) {
                setStatus('❌', `Error: ${e.data}`);
                appendLog(`❌ ${e.data}`, 'log-error');
            } else if (sse.readyState !== EventSource.CLOSED) {
                console.error('SSE connection error', e);
            }
            sse.close();
            progressBar.classList.remove('active');
            downloadBtn.disabled    = false;
            downloadBtn.textContent = 'Try Again';
        });
    }

    // ── Event listeners ──────────────────────────────────────────────────
    downloadBtn.addEventListener('click', () => {
        const url = urlInput.value.trim();
        if (!url) { alert('Please paste a link first!'); return; }
        if (!isValidUrl(url)) { alert('Please enter a valid URL starting with http:// or https://'); return; }
        startDownload(url);
    });

    urlInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') downloadBtn.click();
    });
});
