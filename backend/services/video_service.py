import os
import subprocess
import json
import tempfile
from services.template_generator import get_template_by_id

# Kept for direct dict usage if needed
TEMPLATE_CONFIG = {
    "motivational": {"bg_color": "0f0f0f", "text_color": "white",  "box_color": "FF4500@0.7", "font_size": 72, "boxborderw": 20},
    "gaming":       {"bg_color": "0a0a1a", "text_color": "00FF41", "box_color": "8A2BE2@0.7", "font_size": 68, "boxborderw": 20},
    "spiritual":    {"bg_color": "1a0a2e", "text_color": "E0D7FF", "box_color": "9370DB@0.6", "font_size": 65, "boxborderw": 20},
    "business":     {"bg_color": "0d1b2a", "text_color": "white",  "box_color": "0077B6@0.8", "font_size": 62, "boxborderw": 20},
}

# Backend root = parent of this file's directory
BACKEND_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

# Relative path from backend root — no drive letter, safe for FFmpeg filters
FONT_REL = "assets/fonts/arialbd.ttf"


def _get_audio_duration(audio_path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", audio_path],
        capture_output=True, text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def _esc(text: str) -> str:
    """Escape text for FFmpeg drawtext filter value."""
    return (
        text.replace("\\", "\\\\")
            .replace("'",  "")
            .replace(":",  "\\:")
            .replace("%",  "\\%")
            .replace("\n", " ")
    )


def build_reel(
    captions: list[dict],
    audio_path: str,
    template: str,
    watermark: str,
    output_path: str,
    job_id: str,
) -> None:
    """
    Build a 9:16 vertical reel using FFmpeg.
    FFmpeg is run with cwd=BACKEND_ROOT so all paths inside filter scripts
    can be relative (no Windows drive letter colon issues).
    """
    # Resolve template — supports both old short IDs and new generated IDs
    if template in TEMPLATE_CONFIG:
        cfg = TEMPLATE_CONFIG[template]
        config = {
            "bg_color":   cfg["bg_color"],
            "text_color": cfg["text_color"],
            "box_color":  cfg["box_color"],
            "font_size":  cfg["font_size"],
            "boxborderw": cfg.get("boxborderw", 20),
        }
    else:
        t = get_template_by_id(template)
        config = {
            "bg_color":   t["bg_color"],
            "text_color": t["text_color"],
            "box_color":  t["box_color"],
            "font_size":  t["font_size"],
            "boxborderw": t["boxborderw"],
        }
    duration = _get_audio_duration(audio_path)
    width, height = 1080, 1920
    fs = config["font_size"]
    bw = config["boxborderw"]

    filters = []

    for cap in captions:
        start, end = cap["start"], cap["end"]
        words = cap["text"].split()
        wrapped = [" ".join(words[i:i + 6]) for i in range(0, len(words), 6)]
        total = len(wrapped)
        for li, line in enumerate(wrapped):
            txt = _esc(line)
            y_expr = f"(h-{total * (fs + 8)})/2+{li * (fs + 8)}"
            filters.append(
                f"drawtext=fontfile={FONT_REL}"
                f":text='{txt}'"
                f":fontsize={fs}"
                f":fontcolor={config['text_color']}"
                f":x=(w-text_w)/2"
                f":y={y_expr}"
                f":box=1"
                f":boxcolor={config['box_color']}"
                f":boxborderw={bw}"
                f":enable='between(t,{start},{end})'"
            )

    if watermark:
        wm = _esc(watermark)
        filters.append(
            f"drawtext=fontfile={FONT_REL}"
            f":text='{wm}'"
            f":fontsize=38"
            f":fontcolor=white@0.5"
            f":x=w-text_w-40"
            f":y=h-text_h-60"
        )

    vf_content = ",\n".join(filters) if filters else "null"

    # Write filter to temp file to avoid any shell quoting issues
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8", dir=BACKEND_ROOT
    ) as fscript:
        fscript.write(vf_content)
        script_path = fscript.name

    # Make audio/output paths relative to BACKEND_ROOT for FFmpeg
    try:
        audio_rel = os.path.relpath(audio_path, BACKEND_ROOT).replace("\\", "/")
    except ValueError:
        audio_rel = audio_path  # different drive — use absolute

    try:
        output_rel = os.path.relpath(output_path, BACKEND_ROOT).replace("\\", "/")
    except ValueError:
        output_rel = output_path

    script_rel = os.path.relpath(script_path, BACKEND_ROOT).replace("\\", "/")

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c={config['bg_color']}:size={width}x{height}:rate=30:duration={duration}",
        "-i", audio_rel,
        "-filter_script:v", script_rel,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart",
        output_rel,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=BACKEND_ROOT)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error:\n{result.stderr}")
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)
