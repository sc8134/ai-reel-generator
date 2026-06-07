import os
from gtts import gTTS

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# gTTS accent map — closest matches to the old OpenAI voice names
VOICE_ACCENT_MAP = {
    "alloy":   ("en", "com"),          # US English
    "echo":    ("en", "co.uk"),        # British English
    "fable":   ("en", "com.au"),       # Australian English
    "onyx":    ("en", "co.in"),        # Indian English (deeper cadence)
    "nova":    ("en", "ca"),           # Canadian English
    "shimmer": ("en", "ie"),           # Irish English
}


def text_to_speech(text: str, voice: str = "alloy", job_id: str = "out") -> str:
    """
    Convert text to speech using gTTS (free, no API key needed).
    Returns path to the generated MP3 file.
    """
    lang, tld = VOICE_ACCENT_MAP.get(voice, ("en", "com"))
    output_path = os.path.join(UPLOAD_DIR, f"{job_id}_tts.mp3")

    tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
    tts.save(output_path)

    return output_path
