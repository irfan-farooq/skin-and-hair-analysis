from flask import Blueprint, request, jsonify
from app.services.auth import require_auth
from app.services.weather import get_weather_advice

weather_bp = Blueprint('weather', __name__, url_prefix='/api/weather')

@weather_bp.route('/advice', methods=['GET'])
@require_auth
def weather_advice():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"error": "lat and lon query params required"}), 400

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({"error": "lat and lon must be numbers"}), 400

    result = get_weather_advice(lat, lon)
    return jsonify(result), 200