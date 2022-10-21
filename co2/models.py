from werkzeug.security import generate_password_hash, check_password_hash
from authlib.jose import jwt
from flask import current_app
from datetime import datetime
from .extensions import db
from .functions import now_time


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    jf = db.Column(db.Integer, default=0)
    jf_yesterday = db.Column(db.Integer, default=0)
    logs = db.relationship('Log', back_populates='author', cascade='all')
    day_logs = db.relationship('DayLog', back_populates='author', cascade='all')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self):
        header = {'alg': 'HS256'}
        payload = {
            'id': self.id
        }
        return jwt.encode(
            header, payload, str(current_app.config['SECRET_KEY'])
        ).decode()


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    co2_l = db.Column(db.Integer)
    o_type = db.Column(db.Text)
    unit = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='logs')


class DayLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.String(10), default=now_time)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='day_logs')
