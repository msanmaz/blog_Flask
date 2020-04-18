from datetime import datetime
from app import db , login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(62), index=True, unique=True,nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_has = db.Column(db.String(500))
    posts = db.relationship('Post', backref='author', lazy='dynamic')


    def set_password(self, password):
        self.password_has = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_has,password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


