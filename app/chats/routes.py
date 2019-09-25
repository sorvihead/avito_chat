from app import db
from app import ma

from app.models import Chat
from app.models import User
from app.schemas import UserSchema
from app.schemas import ChatSchema
from app.schemas import MessageSchema
from app.chats.helpers import get_sorted_chats

from app.chats import bp

from flask import jsonify
from flask import request

from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import ArgumentError

chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)
user_schema = UserSchema()


@bp.route('/add', methods=["POST"])
def add_chat():
    if request.content_type == "application/json":
        chat_info = request.json
        errors = chat_schema.validate(chat_info)
        if errors:
            return jsonify(errors), 400
        try:
            chat = chat_schema.load(chat_info)
            db.session.add(chat)
            db.session.commit()
            return jsonify(chat.id)
        except ArgumentError as err:
            return jsonify({"error": [error for error in err.args]}), 400


@bp.route('/get', methods=["POST"])
def get_chats():
    if request.content_type == 'application/json':
        user_info = request.json
        if not user_info.get('user'):
            return jsonify({"error": "missing field user"}), 400
        errors = user_schema.validate(user_info, partial=True)
        if errors:
            return jsonify(errors), 400
        user = User.query.get(user_info.get('user'))
        if not user:
            return jsonify({"error": f"user is not found"}), 404
        chats = get_sorted_chats(user.chats)
        return chats_schema.jsonify(chats)