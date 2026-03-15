# [Saad] - Creates this config file first and pushes to GitHub

import os

class Config:
    SECRET_KEY = "supersecretkey"                       # [Saad]  - App secret key
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"  # [Saad]  - Database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False              # [Saad]  - Disable modification tracking