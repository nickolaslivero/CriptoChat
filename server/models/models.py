from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_chat_association = db.Table('user_chat_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
)

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    chats = db.relationship('Chat', secondary=user_chat_association, back_populates='users')

    def __repr__(self):
        return f"User('{self.username}')"


class Chat(db.Model):
    __tablename__ = "chat"

    id = db.Column(db.Integer, primary_key=True)

    users = db.relationship('User', secondary=user_chat_association, back_populates='chats')

    def __repr__(self):
        return f"Chat('{self.id}')"