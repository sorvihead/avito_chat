from app import db
from app.models import User
from app.models import Message
from app.models import Chat
from app.messages import bp
from app.schemas import MessageSchema
from app.schemas import ChatSchema

from flask import jsonify
from flask import request

from marshmallow import ValidationError

from sqlalchemy.exc import IntegrityError, ArgumentError

chat_schema = ChatSchema()
msg_schema = MessageSchema()
msgs_schema = MessageSchema(many=True)


@bp.route('/get', methods=['POST'])
def get_messages():
    chat_info = request.get_json()
    if not chat_info:
        return jsonify({"errors": "missing data"}), 400
    errors = chat_schema.validate(chat_info, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400
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
        return jsonify({"errors": [e for e in err.args]}), 400
    except IntegrityError:
        return jsonify({"errors": "required field is expected"}), 400
    except ValidationError as err:
        return jsonify({"errors": [e for e in err.args]}), 400

    return msg_schema.jsonify(msg)
