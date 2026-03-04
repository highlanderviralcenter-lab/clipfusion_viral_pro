"""ClipFusion — Transcriber. Whisper com timestamps."""
import subprocess, json, os, tempfile, shutil


def transcribe(video_path: str, model: str = "tiny",
               language: str = "pt", progress_cb=None) -> dict:
    def log(m):
        if progress_cb: progress_cb(m)
    log("Extraindo áudio...")
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "audio.wav")
    try:
        r = subprocess.run(
            ["ffmpeg", "-y", "-i", video_path,
             "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", wav],
            capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-300:])
        log(f"Transcrevendo [{model}]...")
        r2 = subprocess.run(
            ["whisper", wav, "--model", model, "--language", language,
             "--output_format", "json", "--output_dir", tmp,
             "--fp16", "False", "--verbose", "False"],
            capture_output=True, text=True)
        if r2.returncode != 0:
            raise RuntimeError(r2.stderr[-300:])
        with open(os.path.join(tmp, "audio.json"), encoding="utf-8") as f:
            data = json.load(f)
        segs = [{"start": round(s["start"], 2), "end": round(s["end"], 2),
                 "text": s["text"].strip()} for s in data.get("segments", [])]
        log(f"✅ {len(segs)} segmentos transcritos.")
        return {"full_text": " ".join(s["text"] for s in segs), "segments": segs}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def fmt_time(s: float) -> str:
    return f"{int(s//3600):02d}:{int((s%3600)//60):02d}:{int(s%60):02d}"
