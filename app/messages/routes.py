from app import db
from app.models import User
from app.models import Message
from app.models import Chat
from app.messages import bp
from app.schemas import MessageSchema
from app.schemas import ChatSchema
from app.errors.errors import error_response

from flask import jsonify
from flask import request

from marshmallow import ValidationError

from sqlalchemy.exc import InvalidRequestError, ArgumentError

chat_schema = ChatSchema()
msg_schema = MessageSchema()
msgs_schema = MessageSchema(many=True)


@bp.route('/get', methods=['POST'])
def get_messages():
    chat_info = request.get_json()
    if not chat_info:
        return error_response(status_code=400, message="missing data")
    errors = chat_schema.validate(chat_info, partial=True)
    if errors:
        return error_response(status_code=400, message=errors)
    chat = Chat.query.get_or_404(chat_info.get('chat'))
    return msgs_schema.jsonify(chat.messages), 200


@bp.route('/add', methods=['POST'])
def add_message():
    msg_info = request.get_json()
    try:
        msg = msg_schema.load(msg_info)
        db.session.add(msg)
        db.session.commit()
    except ArgumentError as err:
        return error_response(status_code=404, message=[e for e in err.args])
    except InvalidRequestError as err:
        return error_response(status_code=400, message=[e for e in err.args])
    except ValidationError as err:
        return error_response(status_code=400, message=[e for e in err.args])

    return msg_schema.jsonify(msg), 201
