from app import db
from app.models import User
from app.users import bp

from flask import jsonify
from flask import request

from sqlalchemy.exc import IntegrityError


@bp.route('/add', methods=['POST'])
def add_user():
    if request.content_type == 'application/json':
        username = request.json.get('username')
        user = User(username=username)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return jsonify({"error":"Invalid username"}), 400
        
        return jsonify(user.id)

    else:
        return jsonify({"error": "not a json"}), 400
