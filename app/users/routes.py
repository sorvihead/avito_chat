from app import db
from app.models import User
from app.users import bp
from app.schemas import UserSchema

from flask import jsonify
from flask import request

from sqlalchemy.exc import IntegrityError, ArgumentError

user_schema = UserSchema()


@bp.route('/add', methods=['POST'])
def add_user():
    if request.content_type == 'application/json':
        user_info = request.json
        errors = user_schema.validate(user_info)
        if errors:
            return jsonify(errors), 400
        try:
            user = user_schema.load(user_info)
            db.session.add(user)
            db.session.commit()
        except ArgumentError as err:
            return jsonify({"error":[error for error in err.args]}), 400
        
        return jsonify(user.id)

    else:
        return jsonify({"error": "not a json"}), 400
