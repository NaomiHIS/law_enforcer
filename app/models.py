from app import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    discriminator = db.Column(db.String(4), nullable=False)
    avatar = db.Column(db.String(32))
    access_token = db.Column(db.String(128))
    refresh_token = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))