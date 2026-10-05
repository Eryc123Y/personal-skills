"""Narration audio via Gemini 3.8 TTS, one wav per line, for timings.py audio mode.

    GEMINI_API_KEY=... python tts_gemini.py lines.txt voice/
    VOICE=Kore STYLE="calm, warm" TTS_MODEL=gemini-3.8-flash-tts python tts_gemini.py lines.txt voice/
    python tts_gemini.py lines.txt voice/ --per-line      # one request per line (old behaviour)

Requests are the scarce resource: the API counts requests per model per day
(100 on the project this was built with), not audio length. So by default the
lines of a file are read in as few requests as possible: consecutive lines are
joined with `<long pause>` tags into chunks of at most CHUNK_SECONDS of speech
(one chunk per chapter in practice; the output limit is ~10 min of audio), and
each chunk's audio is cut back into one file per line at its longest silences.
A chunk whose cut cannot be verified (wrong number of pauses, or a line far
from its expected length) falls back to one request per line.

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
CHUNK_SECONDS = 240               # speech per request; well under the ~10 min output limit
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


def synth(key: str, text: str) -> bytes:
    """One generateContent request; returns 16-bit mono PCM samples at RATE."""
    part: dict = {"text": text}
    if STYLE:
        part["speech_metadata"] = {"style": STYLE}
    body = {
        "contents": [{"parts": [part]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}},
        },
    }
    req = urllib.request.Request(ENDPOINT.format(model=MODEL), data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                payload = json.load(resp)
            data = base64.b64decode(payload["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            return to_pcm(data)
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


def split(pcm: np.ndarray, texts: list[str]) -> list[np.ndarray] | None:
    """Cut a chunk at its len(texts)-1 longest inner silences; None if the result looks wrong."""
    total = len(pcm) / RATE
    inner = [s for s in silences(pcm) if s[0] > 0.05 and s[1] < total - 0.05]
    k = len(texts) - 1
    if len(inner) < k:
        return None
    cuts = sorted(sorted(inner, key=lambda s: s[1] - s[0], reverse=True)[:k])
    if k and min(b - a for a, b in cuts) < 0.45:      # a <long pause> is clearly longer than a comma
        return None
    edges = [0.0] + [x for a, b in cuts for x in (a + 0.08, b - 0.08)] + [total]
    pieces = [pcm[int(edges[2 * i] * RATE): int(edges[2 * i + 1] * RATE)] for i in range(len(texts))]
    exp = np.array([expected_seconds(t) for t in texts])
    got = np.array([len(p) / RATE for p in pieces])
    ratio = (got / got.sum()) / (exp / exp.sum())
    if np.any(ratio < 0.45) or np.any(ratio > 2.2):   # a pause fell inside a line, or two lines merged
        return None
    return [trim(p) for p in pieces]


def trim(pcm: np.ndarray, keep: float = 0.08) -> np.ndarray:
    spans = silences(pcm, min_len=0.05)
    total = len(pcm) / RATE
    start = spans[0][1] - keep if spans and spans[0][0] <= 0.01 else 0.0
    end = spans[-1][0] + keep if spans and spans[-1][1] >= total - 0.01 else total
    return pcm[int(max(start, 0) * RATE): int(min(end, total) * RATE)]


# ---------------------------------------------------------------- main

def chunks(rows: list[tuple[int, str, str]]) -> list[list[tuple[int, str, str]]]:
    out, cur, secs = [], [], 0.0
    for row in rows:
        s = expected_seconds(row[2])
        if cur and secs + s > CHUNK_SECONDS:
            out.append(cur)
            cur, secs = [], 0.0
        cur.append(row)
        secs += s
    return out + ([cur] if cur else [])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lines", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--per-line", action="store_true", help="one request per line")
    args = ap.parse_args()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY is not set")
    args.out.mkdir(parents=True, exist_ok=True)
    rows = [(i, seg_id, text) for i, (seg_id, text) in enumerate(read_lines(args.lines), 1)]
    path = lambda i, seg_id: args.out / f"{i:02d}_{seg_id}.wav"
    requests = 0

    def one_by_one(group):
        nonlocal requests
        for i, seg_id, text in group:
            if not path(i, seg_id).exists():
                write_wav(path(i, seg_id), trim(synth(key, text)))
                requests += 1
                print(f"{path(i, seg_id).name}: ok", flush=True)

    groups = [[r] for r in rows] if args.per_line else chunks(rows)
    for group in groups:
        if len(group) == 1 or any(path(i, s).exists() for i, s, _ in group):
            one_by_one(group)
            continue
        pcm = synth(key, " <long pause> ".join(text for _, _, text in group))
        requests += 1
        pieces = split(pcm, [text for _, _, text in group])
        if pieces is None:
            print(f"  could not split the chunk {group[0][1]}…{group[-1][1]} reliably; "
                  "falling back to one request per line", flush=True)
            one_by_one(group)
            continue
        for (i, seg_id, _), piece in zip(group, pieces):
            write_wav(path(i, seg_id), piece)
        print(f"{group[0][1]}…{group[-1][1]}: {len(group)} lines from one request", flush=True)
    print(f"done: {requests} request(s) to {MODEL}")


if __name__ == "__main__":
    main()
