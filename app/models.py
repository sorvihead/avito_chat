from app import db
from datetime import datetime


chat_user = db.Table(
    'chat-user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship(
        'User', secondary=chat_user,
        primaryjoin=(chat_user.c.chat_id == id),
        lazy='dynamic',
    )
    messages = db.relationship('Message', backref='chat', lazy='dynamic')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    chats = db.relationship(
        'Chat', secondary=chat_user,
        primaryjoin=(chat_user.c.user_id == id),
        order_by=Chat.created_at.desc,
        lazy='dynamic',
    )


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
