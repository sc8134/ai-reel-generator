import os
import re


def generate_captions(text: str) -> list[dict]:
    """
    Split text into short punchy caption lines (no API needed).
    Splits on punctuation and enforces max 7 words per line.
    Returns [{text, start, end}, ...]
    """
    sentences = re.split(r'(?<=[.!?,;])\s+', text.strip())

    lines = []
    for sentence in sentences:
        sentence = sentence.strip().rstrip(".,;")
        if not sentence:
            continue
        words = sentence.split()
        for i in range(0, len(words), 7):
            chunk = " ".join(words[i:i + 7])
            if chunk:
                lines.append(chunk)

    # 2.5 seconds per caption line
    captions = []
    for i, line in enumerate(lines):
        captions.append({
            "text": line,
            "start": round(i * 2.5, 2),
            "end": round((i + 1) * 2.5, 2),
        })

    return captions


def transcribe_audio(audio_path: str) -> list[dict]:
    """
    Transcribe uploaded audio using Google Speech Recognition (free, no key needed).
    Splits audio into 30-second chunks and transcribes each.
    Returns [{text, start, end}, ...]
    """
    import speech_recognition as sr
    from pydub import AudioSegment

    recognizer = sr.Recognizer()

    # Convert to WAV if needed
    ext = os.path.splitext(audio_path)[1].lower()
    if ext != ".wav":
        audio = AudioSegment.from_file(audio_path)
        wav_path = audio_path.replace(ext, ".wav")
        audio.export(wav_path, format="wav")
    else:
        wav_path = audio_path

    # Load and split into 30s chunks
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = 30_000
    captions = []
    offset = 0.0

    for i in range(0, len(audio), chunk_ms):
        chunk = audio[i: i + chunk_ms]
        chunk_path = wav_path.replace(".wav", f"_chunk{i}.wav")
        chunk.export(chunk_path, format="wav")

        try:
            with sr.AudioFile(chunk_path) as source:
                data = recognizer.record(source)
            text = recognizer.recognize_google(data)
            # Split chunk transcript into short lines
            words = text.split()
            for j in range(0, len(words), 7):
                line = " ".join(words[j:j + 7])
                start = offset + (j / max(len(words), 1)) * (chunk_ms / 1000)
                end = start + 2.5
                captions.append({"text": line, "start": round(start, 2), "end": round(end, 2)})
        except Exception:
            # Skip unintelligible chunks silently
            pass
        finally:
            if os.path.exists(chunk_path):
                os.remove(chunk_path)

        offset += chunk_ms / 1000

    # Clean up temp wav
    if ext != ".wav" and os.path.exists(wav_path):
        os.remove(wav_path)

    if not captions:
        captions = [{"text": "Audio reel", "start": 0.0, "end": 5.0}]

    return captions
