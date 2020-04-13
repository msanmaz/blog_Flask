from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(62), index=True, unique=True)
    email = db.Column(db.String(120), index=True)
    password_has = db.Column(db.String(50))

    def __repr__(self):
        return '<User {}>'.format(self.username)