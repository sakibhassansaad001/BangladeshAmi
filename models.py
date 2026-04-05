from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    university_name = db.Column(db.String(200))
    role = db.Column(db.String(20), default="user")


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    goal_amount = db.Column(db.Float)
    current_amount = db.Column(db.Float, default=0)
    duration = db.Column(db.Integer)
    category = db.Column(db.String(100))
    crowdfunding_type = db.Column(db.String(100))
    status = db.Column(db.String(20), default="pending")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)




