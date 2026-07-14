from flask import Blueprint, jsonify
from app.services.auth import require_auth
from app.models import Scan
from flask import request
import json

history_bp = Blueprint('history', __name__, url_prefix='/api/history')

@history_bp.route('', methods=['GET'])
@require_auth
def get_history():
    scans = Scan.query.filter_by(user_id=request.uid).order_by(Scan.created_at.desc()).all()

    result = []
    for scan in scans:
        result.append({
            "scan_id": scan.id,
            "created_at": scan.created_at.isoformat(),
            "skin_tone": scan.skin_tone,
            "undertone": scan.undertone,
            "acne_severity": scan.acne_severity,
            "acne_zones": json.loads(scan.acne_zones) if scan.acne_zones else [],
            "face_shape": scan.face_shape,
            "hair_type": scan.hair_type,
            "eye_color": scan.eye_color,
            "lip_color": scan.lip_color,
            "health_score": scan.health_score,
            "advice": json.loads(scan.advice_json) if scan.advice_json else {}
        })

    return jsonify({"scans": result, "count": len(result)}), 200