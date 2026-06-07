import os
import uuid
from flask import Blueprint, request, jsonify
from services.caption_service import transcribe_audio
from services.video_service import build_reel

upload_bp = Blueprint("upload", __name__)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

ALLOWED_AUDIO = {"mp3", "wav", "m4a", "ogg", "webm"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_AUDIO


@upload_bp.route("/api/upload-audio", methods=["POST"])
def upload_audio():
    """
    Accept an audio file upload, transcribe it, then generate a reel.
    Form fields: file (audio), template, watermark
    """
    if "file" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid audio file. Allowed: mp3, wav, m4a, ogg, webm"}), 400

    template = request.form.get("template", "motivational")
    watermark = request.form.get("watermark", "")

    job_id = str(uuid.uuid4())
    ext = file.filename.rsplit(".", 1)[1].lower()
    audio_path = os.path.join(UPLOAD_DIR, f"{job_id}.{ext}")
    file.save(audio_path)

    output_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")

    try:
        # 1. Transcribe the audio
        captions = transcribe_audio(audio_path)

        # 2. Build reel using the uploaded audio directly
        build_reel(
            captions=captions,
            audio_path=audio_path,
            template=template,
            watermark=watermark,
            output_path=output_path,
            job_id=job_id,
        )

        download_url = f"/api/download/{job_id}"
        return jsonify({"job_id": job_id, "download_url": download_url, "captions": captions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
