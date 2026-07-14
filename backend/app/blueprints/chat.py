from flask import Blueprint, request, jsonify
from app.services.auth import require_auth

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route('/ask', methods=['POST'])
@require_auth
def ask():
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data['message'].strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Placeholder — swap this block out when Reyhan's TF-IDF chatbot is ready
    # from app.ml.chatbot import get_response
    # reply = get_response(user_message)
    reply = f"Chatbot not ready yet. You asked: '{user_message}'"

    return jsonify({
        "message": user_message,
        "reply": reply
    }), 200