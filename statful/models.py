from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin
from sqlalchemy import func


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    encrypted_password = db.Column(db.String(60))
    activity_id = db.relationship('Activity', backref='user')

    def get_password(self):
        return getattr(self, "_password", None)

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255))
    unit = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    stat_id = db.relationship('Stat', backref='activity')

    def stats_by_day(self):
        stat_date = func.cast(Stat.when, db.Date)
        return db.session.query(stat_date, Stat.occurrences). \
            group_by(stat_date).filter_by(activity_id=self.id). \
            order_by(stat_date).all()

class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    occurrences = db.Column(db.Integer)
    yes_no = db.Column(db.Integer)
    scale = db.Column(db.Integer)
    when = db.Column(db.DateTime)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id', ondelete='CASCADE'), nullable=False)











