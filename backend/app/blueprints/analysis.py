from flask import Blueprint, request, jsonify
from app.services.auth import require_auth
from app.models import Scan
from app.extensions import db
import json
import os
import tempfile

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')

@analysis_bp.route('/scan', methods=['POST'])
@require_auth
def scan():
    from app.engine.recommender import get_advice
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Save uploaded image to a temp file so Reyhan's function can read it by path
    suffix = os.path.splitext(image.filename)[1] or '.jpg'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        image.save(tmp.name)
        tmp_path = tmp.name

    try:
        from app.ml.analysis import analyze_face
        results = analyze_face(tmp_path)
    except Exception as e:
        os.unlink(tmp_path)
        return jsonify({"error": f"ML pipeline failed: {str(e)}"}), 500
    finally:
        # Always delete the temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    if "error" in results:
        return jsonify({"error": results["error"]}), 422

    # Pull out values cleanly
    skin = results.get("skin", {})
    lip = results.get("lip_color", {})
    face = results.get("face_shape", {})
    acne = results.get("acne", {})
    eye = results.get("eye_color", {})
    hair = results.get("hair_texture", {})
    dark = results.get("dark_circles", {})

    new_scan = Scan(
        user_id=request.uid,
        skin_tone=skin.get("tone"),
        undertone=skin.get("undertone"),
        acne_severity=acne.get("overall_severity"),
        acne_zones=json.dumps(acne.get("detections", [])),
        face_shape=face.get("shape"),
        hair_type=hair.get("type"),
        eye_color=eye.get("color"),
        lip_color=lip.get("color"),
        health_score=None,
        advice_json=json.dumps(get_advice(results))
    )

    db.session.add(new_scan)
    db.session.commit()

    return jsonify({
        "scan_id": new_scan.id,
        "results": {
            "skin_tone": skin.get("tone"),
            "undertone": skin.get("undertone"),
            "skin_hex": skin.get("hex"),
            "lip_color": lip.get("color"),
            "lip_hex": lip.get("hex"),
            "face_shape": face.get("shape"),
            "face_shape_confidence": face.get("confidence"),
            "acne_severity": acne.get("overall_severity"),
            "acne_count": acne.get("count"),
            "acne_detections": acne.get("detections"),
            "eye_color": eye.get("color"),
            "hair_type": hair.get("type"),
            "dark_circles": dark.get("severity"),
            "advice": get_advice(results)
        }
    }), 200