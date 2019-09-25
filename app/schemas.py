from app import ma
from app import db
from app.models import User
from app.models import Chat
from app.models import Message

from marshmallow import ValidationError
from marshmallow import post_load
from marshmallow import validates_schema
from marshmallow.fields import Nested, Str, Integer, DateTime, Pluck


class BaseSchema(ma.ModelSchema):
    class Meta:
        sqla_session = db.session


class UserSchema(ma.ModelSchema):
    id = Integer(required=False, data_key="user")
    username = Str(required=True)
    created_at = DateTime(required=False)
    chats = Nested("ChatSchema", many=True, exclude=("users", ), required=False)

    class Meta(BaseSchema.Meta):
        model = User
    

class ChatSchema(ma.ModelSchema):
    id = Integer(required=False, data_key="chat")
    name = Str(required=True)
    created_at = DateTime(required=False)
    messages = Nested('MessageSchema', many=True, exclude=('chat', ), required=False)
    users = Pluck('UserSchema', 'id', many=True, required=True)

    class Meta(BaseSchema.Meta):
        model = Chat

    
    @validates_schema
    def validate_length_users(self, data, **kwargs):
        if len(data["users"]) < 2:
            raise ValidationError("Chat must contain >= 2 users")


class MessageSchema(ma.ModelSchema):
    id = Integer(required=False)
    text = Str(required=True)
    created_at = DateTime(required=False)
    author = Nested('UserSchema', only=("id", ), required=True)
    chat = Nested('ChatSchema', only=("id", ), required=True)

    class Meta(BaseSchema.Meta):
        model = Message
        
