from app import create_app, db
from app.models import User, Chat, Message
from app.schemas import UserSchema, ChatSchema, MessageSchema

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Chat': Chat, 'Message': Message, 'ChatSchema': ChatSchema,
            'UserSchema': UserSchema,
            'MessageSchema': MessageSchema}
