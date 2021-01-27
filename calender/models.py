from datetime import datetime
from calender import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True)
    email = db.Column(db.String(140), index=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship('Event', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DATE, index=True)
    time = db.Column(db.TIME, index=True)
    event = db.Column(db.String(200))
    category = db.Column(db.String(10), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Event: {} on {} {} by {}>'.format(self.event, str(self.date), str(self.time), self.user_id)
