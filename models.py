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

# [Siam] - Campaign model storing all essential campaign details
# [Siam] - status defaults to "pending" so all new campaigns go to admin review queue
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))                    #[Siam] - Campaign title
    description = db.Column(db.Text)                     #[Siam] - Purpose and description
    goal_amount = db.Column(db.Float)                    #[Siam] - Funding goal amount
    current_amount = db.Column(db.Float, default=0)      #[Siam] - Tracks total raised 
    duration = db.Column(db.Integer)                     #[Siam] - Campaign duration
    category = db.Column(db.String(100))                 #[Siam] - Campaign category
    status = db.Column(db.String(20), default="pending") #[Siam] - Defaults to pending for admin queue;
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# [Hridoy] - CampaignUpdate model for attaching supporting info (brief plan or budget summary)
class CampaignUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)                       # [Hridoy] - The supporting info content
    created_at = db.Column(db.DateTime, default=datetime.utcnow)       # [Hridoy] - Timestamp of the update
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))  # [Hridoy] - Link to the campaign
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))          # [Hridoy] - Link to the creator