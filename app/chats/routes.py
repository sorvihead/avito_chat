from app import db
from app.models import Chat
from app.models import User
from app.chats import bp

from flask import jsonify
from flask import request

from sqlalchemy.exc import IntegrityError


@bp.route('/add', methods=["POST"])
def add_chat():
    if request.content_type == "application/json":
        chat_name = request.json.get('name')
        if not chat_name:
            return jsonify({"error": "chat name expected"}), 400

        users = request.json.get('users')
        if not users or len(users) < 2:
            return jsonify({"error": "count of users must be greater 1"}), 400
        users_entities = []
        for user_id in users:
            try:
                user_id = int(user_id)
            except ValueError:
                return jsonify({"error": "user id must be an integer"}), 400
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return jsonify({"error": f"User {user_id} not found"})
            users_entities.append(user)
        try:
            chat = Chat(name=chat_name)
            chat.users = users_entities
            db.session.add(chat)
            db.session.commit()
        except IntegrityError:
            return jsonify({"error": "chat name must be unique"}), 400
        return jsonify(chat.id)
            

