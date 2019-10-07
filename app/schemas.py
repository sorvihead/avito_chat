from app import ma
from app import db
from app.models import User
from app.models import Chat
from app.models import Message

from marshmallow import ValidationError
from marshmallow import validates_schema
from marshmallow.fields import Nested, Str, Integer, DateTime, Pluck


class BaseSchema(ma.ModelSchema):
    class Meta:
        sqla_session = db.session


class UserSchema(ma.ModelSchema):
    id = Integer(required=False)
    username = Str(required=True)
    created_at = DateTime(required=False)
    chats = Nested("ChatSchema", many=True, exclude=("users",), required=False)

    class Meta(BaseSchema.Meta):
        model = User

    @validates_schema
    def validate_username(self, data, **kwargs):
        if data.get('id'):
            return
        if not data.get('username'):
            raise ValidationError('Missing username')


class ChatSchema(ma.ModelSchema):
    id = Integer(required=False, data_key="chat")
    name = Str(required=True)
    created_at = DateTime(required=False)
    messages = Nested('MessageSchema', many=True, exclude=('chat',), required=False)
    users = Pluck('UserSchema', 'id', many=True, required=True)

    class Meta(BaseSchema.Meta):
        model = Chat

    @validates_schema
    def validate_name(self, data, **kwargs):
        if data.get('id'):
            return
        elif not data.get('name'):
            raise ValidationError('Missing chat name')


class MessageSchema(ma.ModelSchema):
    id = Integer(required=False)
    text = Str(required=True)
    created_at = DateTime(required=False)
    author = Pluck('UserSchema', "id", required=True)
    chat = Pluck('ChatSchema', "id", required=True)

    class Meta(BaseSchema.Meta):
        model = Message

    @validates_schema
    def validate_text(self, data, **kwargs):
        if not data.get('text'):
            raise ValidationError('Missing text')
