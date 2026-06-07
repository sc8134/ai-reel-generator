import os
import uuid
from flask import Blueprint, request, jsonify
from services.caption_service import generate_captions
from services.tts_service import text_to_speech
from services.video_service import build_reel

generate_bp = Blueprint("generate", __name__)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@generate_bp.route("/api/generate-reel", methods=["POST"])
def generate_reel():
    """
    Generate a reel from text input.
    Body JSON: { text, template, voice, watermark }
    """
    data = request.get_json()
    if not data or not data.get("text"):
        return jsonify({"error": "text is required"}), 400

    text = data["text"].strip()
    template = data.get("template", "motivational")
    voice = data.get("voice", "alloy")
    watermark = data.get("watermark", "")

    job_id = str(uuid.uuid4())
    output_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")

    try:
        # 1. Generate captions from text via AI
        captions = generate_captions(text)

        # 2. Generate TTS audio
        audio_path = text_to_speech(text, voice=voice, job_id=job_id)

        # 3. Build the reel with FFmpeg
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


@generate_bp.route("/api/download/<job_id>", methods=["GET"])
def download_reel(job_id):
    from flask import send_file
    path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
    return send_file(path, mimetype="video/mp4", as_attachment=True, download_name="reel.mp4")
