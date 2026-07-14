from flask import Blueprint, request, jsonify
from app.services.auth import require_auth
from app.models import User, Scan
from app.extensions import db

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/profile', methods=['GET'])
@require_auth
def get_profile():
    user = User.query.get(request.uid)

    if not user:
        return jsonify({"error": "User not found"}), 404

    scan_count = Scan.query.filter_by(user_id=request.uid).count()
    latest_scan = Scan.query.filter_by(user_id=request.uid).order_by(Scan.created_at.desc()).first()

    return jsonify({
        "uid": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
        "scan_count": scan_count,
        "latest_scan_id": latest_scan.id if latest_scan else None,
        "latest_scan_date": latest_scan.created_at.isoformat() if latest_scan else None
    }), 200