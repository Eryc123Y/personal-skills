"""Narration audio via Gemini 3.8 TTS, one wav per line, for timings.py audio mode.

    GEMINI_API_KEY=... python tts_gemini.py lines.txt voice/
    VOICE=Kore STYLE="calm, warm" TTS_MODEL=gemini-3.8-flash-tts python tts_gemini.py lines.txt voice/
    python tts_gemini.py lines.txt voice/ --per-line      # one request per line (old behaviour)

Requests are the scarce resource: the API counts requests per model per day
(100 on the project this was built with), not audio length. So by default the
lines of a file are read in as few requests as possible: consecutive lines are
joined with `<long pause>` tags into even chunks of about CHUNK_SECONDS of
speech (TTS_CHUNK_SECONDS in nominal seconds, default 480, about 5 min of real
speech; one request returns at most ~655 s),
broken only between slides (ids like A0-03.2 belong to slide A0-03), and each
chunk's audio is cut back into one file per line at its longest silences.
A chunk whose cut cannot be verified is asked once more, then halved at a slide
boundary: long reads keep the voice even, so a line is read alone only last.
After a run every line is measured (pitch, loudness, speaking rate) and lines
far from the film's median are listed in voice_check.tsv; --redo-outliers
remakes them. --batch sends the chunks through the Batch API instead (half
price, quota separate from the daily request cap, results within 24 h; the job
is remembered in OUT/.batch.json, so re-running resumes it).

Files are named NN_<id>.wav. Existing files are kept: a chunk is requested only
when none of its lines exist yet; otherwise missing lines are made one by one
(delete a file to redo that line).

A daily quota error stops the run at once with the wait time the API reports;
a per-minute limit waits and retries. Uses only the standard library and
numpy. Never print or log the API key.
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path

import numpy as np

MODEL = os.environ.get("TTS_MODEL", "gemini-3.8-flash-lite-tts")
VOICE = os.environ.get("VOICE", "Charon")
# The docs advise short or empty style strings; long direction blocks make the voice drift.
STYLE = os.environ.get("STYLE", "")
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
RATE = 24000                      # Gemini TTS output: 24 kHz mono 16-bit
# Speech per request. One request returns at most 16,384 output tokens = 25 tokens per second of audio,
# about 655 s; one long read keeps the voice most even, but very long reads can drift and are harder to cut.
# Measured speech is ~1.5x faster than the nominal CPS below, so 480 nominal s is ~5 min of real audio.
CHUNK_SECONDS = min(float(os.environ.get("TTS_CHUNK_SECONDS", "480")), 600.0)
CPS = {"cjk": 3.0, "latin": 2.6}  # rough spoken units per second, only for chunking and checks
CJK = re.compile(r"[㐀-鿿豈-﫿]")


class QuotaExhausted(SystemExit):
    pass


def read_lines(path: Path) -> list[tuple[str, str]]:
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            seg_id, _, text = line.partition("|")
            rows.append((seg_id.strip(), text.strip()))
    return rows


def expected_seconds(text: str) -> float:
    cjk = len(CJK.findall(text))
    words = len(re.findall(r"[A-Za-z0-9]+", CJK.sub(" ", text)))
    return cjk / CPS["cjk"] + words / CPS["latin"] + 0.3


# ---------------------------------------------------------------- API

def _retry_delay(err: dict) -> float:
    for detail in err.get("details", []):
        if detail.get("@type", "").endswith("RetryInfo"):
            return float(detail.get("retryDelay", "0s").rstrip("s") or 0)
    return 0.0


def _is_daily(err: dict) -> bool:
    text = json.dumps(err)
    return "per_day" in text or "PerDay" in text


def request_body(text: str) -> dict:
    part: dict = {"text": text}
    if STYLE:
        part["speech_metadata"] = {"style": STYLE}
    return {
        "contents": [{"parts": [part]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}},
        },
    }


def audio_of(response: dict) -> np.ndarray:
    return to_pcm(base64.b64decode(response["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]))


def synth(key: str, text: str) -> bytes:
    """One generateContent request; returns 16-bit mono PCM samples at RATE."""
    body = request_body(text)
    req = urllib.request.Request(ENDPOINT.format(model=MODEL), data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                payload = json.load(resp)
            return audio_of(payload)
        except urllib.error.HTTPError as exc:
            err = json.loads(exc.read() or b"{}").get("error", {})
            if exc.code == 429 and _is_daily(err):
                hours = _retry_delay(err) / 3600
                raise QuotaExhausted(f"daily TTS quota for {MODEL} is used up; it resets in about {hours:.1f} h. "
                                     "Lines done so far are kept; re-run later.")
            if exc.code in (429, 500, 503) and attempt < 4:
                wait = max(_retry_delay(err), 5 * 2 ** attempt)
                print(f"  HTTP {exc.code}, retrying in {wait:.0f} s", flush=True)
                time.sleep(min(wait, 120))
                continue
            raise SystemExit(f"TTS request failed: HTTP {exc.code} {err.get('message', '')[:300]}")
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < 4:
                print(f"  network error ({exc}), retrying", flush=True)
                time.sleep(5 * 2 ** attempt)
                continue
            raise SystemExit(f"TTS request failed: {exc}")
    raise SystemExit("TTS request failed after retries")


def to_pcm(data: bytes) -> np.ndarray:
    if data[:4] == b"RIFF":
        with wave.open(io.BytesIO(data)) as w:
            if w.getframerate() != RATE or w.getnchannels() != 1 or w.getsampwidth() != 2:
                raise SystemExit("unexpected TTS audio format")
            data = w.readframes(w.getnframes())
    return np.frombuffer(data, dtype="<i2").copy()


def write_wav(path: Path, pcm: np.ndarray) -> None:
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.astype("<i2").tobytes())


# ---------------------------------------------------------------- splitting

def silences(pcm: np.ndarray, threshold_db: float = -40.0, min_len: float = 0.25) -> list[tuple[float, float]]:
    """Silent spans (start, end) in seconds, from a 10 ms RMS envelope."""
    hop = RATE // 100
    frames = len(pcm) // hop
    x = pcm[: frames * hop].astype(np.float64).reshape(frames, hop) / 32768.0
    db = 20 * np.log10(np.sqrt((x ** 2).mean(axis=1)) + 1e-9)
    quiet = db < threshold_db
    spans, start = [], None
    for i, q in enumerate(np.append(quiet, False)):
        if q and start is None:
            start = i
        elif not q and start is not None:
            if (i - start) * 0.01 >= min_len:
                spans.append((start * 0.01, i * 0.01))
            start = None
    return spans


def _cuts_dp(inner, expected, total):
    """Choose one silence per line boundary, in order: each boundary prefers a long silence close to where the
    text says it should fall (cumulative expected length, scaled to the real total). Dynamic programming over
    (boundary, silence); returns the chosen silences or None."""
    k = len(expected) - 1
    if k == 0:
        return []
    cum = np.cumsum(expected)[:-1] / np.sum(expected) * total
    n = len(inner)
    if n < k:
        return None
    mids = np.array([(a + b) / 2 for a, b in inner])
    lens = np.array([b - a for a, b in inner])
    spread = max(1.5, 0.06 * total)                      # how far a boundary may sit from its estimate
    score = lambda j, i: 2.0 * min(lens[i], 1.2) - abs(mids[i] - cum[j]) / spread
    best = np.full((k, n), -np.inf)
    back = np.zeros((k, n), dtype=int)
    for i in range(n):
        best[0, i] = score(0, i)
    for j in range(1, k):
        run, arg = -np.inf, -1
        for i in range(n):
            if i - 1 >= 0 and best[j - 1, i - 1] > run:
                run, arg = best[j - 1, i - 1], i - 1
            if arg >= 0:
                best[j, i] = run + score(j, i)
                back[j, i] = arg
    i = int(np.argmax(best[k - 1]))
    if not np.isfinite(best[k - 1, i]):
        return None
    chosen = [i]
    for j in range(k - 1, 0, -1):
        i = int(back[j, i])
        chosen.append(i)
    return [inner[i] for i in reversed(chosen)]


def split(pcm: np.ndarray, texts: list[str]) -> list[np.ndarray] | None:
    """Cut a chunk into len(texts) lines at silences chosen by _cuts_dp; None if the result looks wrong."""
    total = len(pcm) / RATE
    inner = [s for s in silences(pcm) if s[0] > 0.05 and s[1] < total - 0.05]
    exp = np.array([expected_seconds(t) for t in texts])
    cuts = _cuts_dp(inner, exp, total)
    if cuts is None:
        return None
    if cuts and min(b - a for a, b in cuts) < 0.3:       # a line break is always a clear pause
        return None
    edges = [0.0] + [x for a, b in cuts for x in (a + 0.08, b - 0.08)] + [total]
    pieces = [pcm[int(edges[2 * i] * RATE): int(edges[2 * i + 1] * RATE)] for i in range(len(texts))]
    got = np.array([len(p) / RATE for p in pieces])
    ratio = (got / got.sum()) / (exp / exp.sum())
    if np.any(ratio < 0.5) or np.any(ratio > 2.0):    # a cut fell inside a line, or two lines merged
        return None
    return [trim(p) for p in pieces]


def trim(pcm: np.ndarray, keep: float = 0.08) -> np.ndarray:
    spans = silences(pcm, min_len=0.05)
    total = len(pcm) / RATE
    start = spans[0][1] - keep if spans and spans[0][0] <= 0.01 else 0.0
    end = spans[-1][0] + keep if spans and spans[-1][1] >= total - 0.01 else total
    return pcm[int(max(start, 0) * RATE): int(min(end, total) * RATE)]


# ---------------------------------------------------------------- voice consistency

def profile(pcm: np.ndarray) -> tuple[float, float]:
    """(median pitch in Hz, loudness of voiced frames in dBFS) from 40 ms frames; pitch by autocorrelation."""
    hop, win = RATE // 100, RATE // 25
    x = pcm.astype(np.float64) / 32768.0
    f0s, levels = [], []
    lo, hi = RATE // 320, RATE // 70                   # 70-320 Hz covers speaking voices
    for start in range(0, len(x) - win, hop * 2):
        fr = x[start:start + win]
        rms = np.sqrt((fr ** 2).mean())
        if rms < 0.01:
            continue
        fr = fr - fr.mean()
        ac = np.correlate(fr, fr, "full")[win - 1:]
        lag = lo + int(np.argmax(ac[lo:hi]))
        if ac[lag] > 0.35 * ac[0]:                       # clearly periodic: a voiced frame
            f0s.append(RATE / lag)
            levels.append(20 * np.log10(rms))
    if not f0s:
        return float("nan"), float("nan")
    return float(np.median(f0s)), float(np.median(levels))


def check(rows, path, z_limit: float = 3.5) -> list[tuple[int, str, str]]:
    """Measure every line (pitch, loudness, speaking rate) and flag lines far from the film's median
    (robust z-score over the median absolute deviation). Writes voice_check.tsv next to the audio."""
    stats = []
    for i, seg_id, text in rows:
        f = path(i, seg_id)
        if not f.exists():
            continue
        with wave.open(str(f)) as w:
            pcm = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
        f0, db = profile(pcm)
        rate = expected_seconds(text) / max(len(pcm) / RATE, 0.1)   # >1 means faster than the nominal pace
        stats.append((i, seg_id, text, f0, db, rate, len(pcm) / RATE))
    if len(stats) < 5:
        return []
    cols = np.array([[s[3], s[4], s[5]] for s in stats])
    med = np.nanmedian(cols, axis=0)
    mad = np.nanmedian(np.abs(cols - med), axis=0) * 1.4826 + 1e-9
    z = np.abs(cols - med) / mad
    short = np.array([s_[6] < 2.5 for s_ in stats])
    z[short, :2] = 0.0                                   # pitch and level are unreliable on very short lines
    flagged = []
    out = path(0, "x").parent / "voice_check.tsv"
    with out.open("w", encoding="utf-8") as fh:
        fh.write("line\tpitch_hz\tlevel_db\trate\tflag\n")
        for s_, zz in zip(stats, z):
            bad = bool(np.nanmax(zz) > z_limit)
            fh.write(f"{s_[1]}\t{s_[3]:.0f}\t{s_[4]:.1f}\t{s_[5]:.2f}\t{'!' if bad else ''}\n")
            if bad:
                flagged.append(s_[:3])
    print(f"voice check: median pitch {med[0]:.0f} Hz, level {med[1]:.1f} dB, rate x{med[2]:.2f}; "
          f"{len(flagged)} of {len(stats)} lines flagged (see {out.name})")
    for _, seg_id, _ in flagged:
        print(f"  ! {seg_id}")
    return flagged


# ---------------------------------------------------------------- chunking

def group_of(seg_id: str) -> str:
    """Lines named like A0-03.2 belong to slide A0-03; chunks only break between slides."""
    return seg_id.rsplit(".", 1)[0] if "." in seg_id else seg_id


def chunks(rows: list[tuple[int, str, str]]) -> list[list[tuple[int, str, str]]]:
    """Even chunks of about CHUNK_SECONDS, broken only where the slide changes (unless one slide is longer)."""
    total = sum(expected_seconds(r[2]) for r in rows)
    n = max(1, int(np.ceil(total / CHUNK_SECONDS)))
    target = total / n
    out, cur = [], []
    secs = lambda rs: sum(expected_seconds(r[2]) for r in rs)
    for row in rows:
        new_group = not cur or group_of(row[1]) != group_of(cur[-1][1])
        if cur and new_group and secs(cur) >= target:
            out.append(cur)
            cur = []
        elif cur and secs(cur) + expected_seconds(row[2]) > CHUNK_SECONDS:
            # full in the middle of a slide: cut at the last slide boundary inside the chunk, if there is one
            cuts = [k for k in range(1, len(cur)) if group_of(cur[k][1]) != group_of(cur[k - 1][1])]
            k = cuts[-1] if cuts else len(cur)
            out.append(cur[:k])
            cur = cur[k:]
        cur.append(row)
    return out + ([cur] if cur else [])


def halves(group):
    """Split a chunk in two, at the slide boundary nearest its middle."""
    mid = len(group) // 2
    cuts = [k for k in range(1, len(group)) if group_of(group[k][1]) != group_of(group[k - 1][1])]
    k = min(cuts, key=lambda c: abs(c - mid)) if cuts else mid
    return group[:k], group[k:]


# ---------------------------------------------------------------- batch mode

API = "https://generativelanguage.googleapis.com/v1beta/"


def _call(key: str, url: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.load(resp)


def batch_run(key, groups, path, state_file: Path, wait_min: float) -> list[list[tuple[int, str, str]]]:
    """Submit the chunks as one Batch API job (half price, its own quota), wait up to wait_min minutes, then write
    the lines. The job name is kept in state_file, so a later run resumes instead of submitting again.
    Returns the chunks whose audio could not be cut reliably (to be redone with ordinary requests)."""
    if state_file.exists():
        state = json.loads(state_file.read_text())
    else:
        todo = [g for g in groups if not any(path(i, s).exists() for i, s, _ in g)]
        if not todo:
            return []
        reqs = [{"request": request_body(" <long pause> ".join(t for _, _, t in g)), "metadata": {"key": f"chunk-{k}"}}
                for k, g in enumerate(todo)]
        job = _call(key, f"{API}models/{MODEL}:batchGenerateContent",
                    {"batch": {"display_name": state_file.parent.name, "input_config": {"requests": {"requests": reqs}}}})
        state = {"name": job["name"], "chunks": todo}
        state_file.write_text(json.dumps(state, ensure_ascii=False))
        print(f"submitted batch {job['name']}: {len(todo)} chunk(s) to {MODEL}", flush=True)
    t_end = time.time() + wait_min * 60
    while True:
        job = _call(key, API + state["name"])
        st = job.get("metadata", {}).get("state", "")
        if job.get("done"):
            break
        if time.time() > t_end:
            print(f"batch {state['name']} is {st}; run the same command again later to collect it")
            return []
        time.sleep(60)
    if not st.endswith("SUCCEEDED"):                    # BATCH_STATE_* in practice, JOB_STATE_* in older docs
        state_file.unlink()                              # failed, cancelled or expired: nothing to collect
        raise SystemExit(f"batch {state['name']} ended as {st}: {json.dumps(job.get('error', {}))[:300]}")
    resp = job.get("response", {})
    if "responsesFile" in resp:
        url = f"https://generativelanguage.googleapis.com/download/v1beta/{resp['responsesFile']}:download?alt=media"
        req = urllib.request.Request(url, headers={"x-goog-api-key": key})
        with urllib.request.urlopen(req, timeout=600) as r:
            items = [json.loads(l) for l in r.read().decode().splitlines() if l.strip()]
    else:
        items = resp.get("inlinedResponses", {})
        items = items.get("inlinedResponses", items) if isinstance(items, dict) else items
    by_key = {}
    for k, it in enumerate(items):
        name = (it.get("metadata") or {}).get("key") or it.get("key") or f"chunk-{k}"
        by_key[name] = it.get("response")
    failed = []
    for k, g in enumerate(state["chunks"]):
        r = by_key.get(f"chunk-{k}")
        pieces = split(audio_of(r), [t for _, _, t in g]) if r else None
        if pieces is None:
            failed.append([tuple(x) for x in g])
            continue
        for (i, seg_id, _), piece in zip(g, pieces):
            write_wav(path(i, seg_id), piece)
        print(f"{g[0][1]}…{g[-1][1]}: {len(g)} lines from the batch", flush=True)
    state_file.unlink()
    return failed


# ---------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lines", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--per-line", action="store_true", help="one request per line")
    ap.add_argument("--batch", action="store_true", help="use the Batch API (half price, own quota, up to 24 h)")
    ap.add_argument("--wait", type=float, default=90, help="minutes to wait for a batch before exiting (default 90)")
    ap.add_argument("--check", action="store_true", help="only measure the existing lines and flag outliers")
    ap.add_argument("--redo-outliers", action="store_true", help="delete flagged lines, then make them again")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    rows = [(i, seg_id, text) for i, (seg_id, text) in enumerate(read_lines(args.lines), 1)]
    path = lambda i, seg_id: args.out / f"{i:02d}_{seg_id}.wav"
    if args.check:
        check(rows, path)
        return
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY is not set")
    if args.redo_outliers:
        for i, seg_id, _ in check(rows, path):
            path(i, seg_id).unlink()
    requests = 0

    def one_by_one(group):
        nonlocal requests
        for i, seg_id, text in group:
            if not path(i, seg_id).exists():
                write_wav(path(i, seg_id), trim(synth(key, text)))
                requests += 1
                print(f"{path(i, seg_id).name}: ok", flush=True)

    def as_chunk(group, depth=0):
        """One request for the whole chunk; if its audio cannot be cut reliably, retry once, then halve it."""
        nonlocal requests
        if len(group) == 1 or any(path(i, s).exists() for i, s, _ in group):
            one_by_one(group)
            return
        pcm = synth(key, " <long pause> ".join(text for _, _, text in group))
        requests += 1
        pieces = split(pcm, [text for _, _, text in group])
        if pieces is None and depth == 0:
            print(f"  {group[0][1]}…{group[-1][1]}: pauses unclear, asking once more", flush=True)
            pcm = synth(key, " <long pause> ".join(text for _, _, text in group))
            requests += 1
            pieces = split(pcm, [text for _, _, text in group])
        if pieces is None:
            a, b = halves(group)
            print(f"  {group[0][1]}…{group[-1][1]}: still unclear; splitting into two requests", flush=True)
            as_chunk(a, depth + 1)
            as_chunk(b, depth + 1)
            return
        for (i, seg_id, _), piece in zip(group, pieces):
            write_wav(path(i, seg_id), piece)
        print(f"{group[0][1]}…{group[-1][1]}: {len(group)} lines from one request", flush=True)

    groups = [[r] for r in rows] if args.per_line else chunks(rows)
    if args.batch and not args.per_line:
        groups = batch_run(key, groups, path, args.out / ".batch.json", args.wait)
        if not groups and any(not path(i, s).exists() for i, s, _ in rows):
            return                                          # still waiting for the batch
    for group in groups:
        as_chunk(group)
    print(f"done: {requests} ordinary request(s) to {MODEL}")
    check(rows, path)


if __name__ == "__main__":
    main()
