import json
import os
from faster_whisper import WhisperModel

# Input media (prefer audio if available)
AUDIO_PATH = os.path.join("videos", "68de6cf20000000007034715.mp3")
VIDEO_PATH = os.path.join("videos", "68de6cf20000000007034715.mp4")

INPUT_PATH = AUDIO_PATH if os.path.exists(AUDIO_PATH) else VIDEO_PATH

OUTPUT_RAW = "faster_whisper_raw.json"
OUTPUT_SENT = "faster_whisper_sentences.json"

# Init model (cpu/bfloat16 for widest compatibility)
# You can switch to "medium" or enable GPU by setting device="cuda", compute_type="float16"
model = WhisperModel("small", device="cpu", compute_type="int8")

# Transcribe with word timestamps
segments, info = model.transcribe(
    INPUT_PATH,
    language="en",
    task="transcribe",
    word_timestamps=True,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=300),
)

# Collect raw segments and words
raw_segments = []
for seg in segments:
    raw_words = []
    if seg.words:
        for w in seg.words:
            raw_words.append({
                "word": w.word,
                "start": round(w.start or 0.0, 2),
                "end": round(w.end or 0.0, 2),
                "prob": round(getattr(w, "probability", 0.0), 4),
            })
    raw_segments.append({
        "id": seg.id,
        "start": round(seg.start or 0.0, 2),
        "end": round(seg.end or 0.0, 2),
        "text": seg.text,
        "avg_logprob": getattr(seg, "avg_logprob", None),
        "words": raw_words,
    })

raw_output = {
    "language": info.language,
    "language_probability": getattr(info, "language_probability", None),
    "duration": getattr(info, "duration", None),
    "segments": raw_segments,
}

with open(OUTPUT_RAW, "w", encoding="utf-8") as f:
    json.dump(raw_output, f, ensure_ascii=False, indent=2)

# Derive sentence-level segments using words and punctuation
sentences = []
current_words = []

# Helper to flush a sentence
def flush_sentence():
    if not current_words:
        return
    start = current_words[0]["start"]
    end = current_words[-1]["end"]
    text = "".join([w["word"] for w in current_words]).strip()
    if text:
        sentences.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "text": text,
        })
    current_words.clear()

# Iterate words across segments in order
for seg in raw_segments:
    for w in seg["words"]:
        token = w["word"]
        current_words.append(w)
        if token.endswith(".") or token.endswith("!") or token.endswith("?"):
            flush_sentence()

# Flush remaining
flush_sentence()

with open(OUTPUT_SENT, "w", encoding="utf-8") as f:
    json.dump({"sentences": sentences}, f, ensure_ascii=False, indent=2)

print(f"Saved raw to {OUTPUT_RAW}")
print(f"Saved sentences to {OUTPUT_SENT}")
