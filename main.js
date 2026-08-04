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
        return url.includes('youtube.com') || url.includes('youtu.be') || url.includes('spotify.com');
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
                headers: { 'Content-Type': 'application/json' },
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
                window.location.href = encodeURI(result.download_url);
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
        if (!url)           { alert('Please paste a link first!'); return; }
        if (!isValidUrl(url)) { alert('Invalid link! We support YouTube and Spotify.'); return; }
        startDownload(url);
    });

    urlInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') downloadBtn.click();
    });
});
