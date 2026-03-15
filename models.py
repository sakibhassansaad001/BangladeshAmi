# [Saad] - Creates this models file first and pushes to GitHub

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


# [Saad]  - User model for authentication and identity
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    university_name = db.Column(db.String(200))
    role = db.Column(db.String(20), default="user")  # [Saad] Leader - Role field to distinguish admin from regular user
