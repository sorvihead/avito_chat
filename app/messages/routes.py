from app import db
from app.models import Message
from app.messages import bp
from app.schemas import MessageSchema

from flask import jsonify
from flask import request

from sqlalchemy.exc import IntegrityError, ArgumentError


@bp.route('/get', methods=['POST'])
def get_messages():
    pass


@bp.route('/add', methods=['POST'])
def add_message():
    pass