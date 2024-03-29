from app import db

from datetime import datetime

from sqlalchemy import event

from sqlalchemy.exc import ArgumentError
from sqlalchemy.exc import InvalidRequestError

chat_user = db.Table(
    'chat-user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User')  # FIXME


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='chat', lazy='dynamic', order_by=Message.created_at.desc())
    users = db.relationship(
        'User', secondary=chat_user,
        primaryjoin=(chat_user.c.chat_id == id),
        lazy='dynamic'
    )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    chats = db.relationship(
        'Chat', secondary=chat_user,
        primaryjoin=(chat_user.c.user_id == id),
        lazy='dynamic',
    )


@event.listens_for(Message, 'init')
def recieve_message_init(target, args, kwargs):
    author, chat = kwargs['author'], kwargs['chat']
    author = User.query.get(author.id)
    chat = Chat.query.get(chat.id)

    if author in chat.users:
        return kwargs
    else:
        raise InvalidRequestError("author must be in a chat")


@event.listens_for(Chat, 'init')
def recieve_chat_init(target, args, kwargs):
    chat_name = kwargs.get('name')
    chat = Chat.query.filter_by(name=chat_name).first()
    if chat:
        raise InvalidRequestError("Chat name must be an unique")
    users = kwargs['users']
    for user in users:
        user = User.query.get(user.id)
        if not user:
            raise ArgumentError("User not found")
    return kwargs


@event.listens_for(User, 'init')
def recieve_user_init(target, args, kwargs):
    username = kwargs.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        raise InvalidRequestError("Username must be an unique")
    return kwargs
