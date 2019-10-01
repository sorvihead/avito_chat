from app import db
from app import ma

from app.models import Chat
from app.models import User
from app.schemas import UserSchema
from app.schemas import ChatSchema
from app.schemas import MessageSchema
from app.chats.helpers import get_sorted_chats
from app.errors.errors import error_response

from app.chats import bp

from flask import jsonify
from flask import request

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import ArgumentError

chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)
user_schema = UserSchema()


@bp.route('/add', methods=["POST"])
def add_chat():
    if request.content_type == "application/json":
        chat_info = request.get_json()
        try:
            errors = chat_schema.validate(chat_info)
        except ArgumentError as err:
            return error_response(status_code=404, message=[e for e in err.args])
        if errors:
            return error_response(status_code=400, message=errors)
        try:
            chat = chat_schema.load(chat_info)
            db.session.add(chat)
            db.session.commit()
            return jsonify(chat.id), 201
        except ArgumentError as err:
            return error_response(status_code=404, message=[e for e in err.args])
        except InvalidRequestError as err:
            return error_response(status_code=400)


@bp.route('/get', methods=["POST"])
def get_chats():
    if request.content_type == 'application/json':
        user_info = request.json
        if not user_info.get('user'):
            return error_response(status_code=400, message="missing field user")
        try:
            user_id = int(user_info.get('user'))
        except ValueError:
            return error_response(status_code=400, message="user id must be an integer")
        user = User.query.get_or_404(user_id)
        chats = get_sorted_chats(user.chats)
        return chats_schema.jsonify(chats), 200