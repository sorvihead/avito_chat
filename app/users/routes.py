from app import db
from app.models import User
from app.users import bp
from app.errors.errors import error_response
from app.schemas import UserSchema

from flask import jsonify
from flask import request

from sqlalchemy.exc import InvalidRequestError, ArgumentError

user_schema = UserSchema()


@bp.route('/add', methods=['POST'])
def add_user():
    if request.content_type == 'application/json':
        user_info = request.json
        errors = user_schema.validate(user_info)
        if errors:
            return error_response(status_code=400, message=errors)
        try:
            user = user_schema.load(user_info)
            db.session.add(user)
            db.session.commit()
        except InvalidRequestError as err:
            return error_response(status_code=400, message=[e for e in err.args])
        
        return jsonify(user.id), 201