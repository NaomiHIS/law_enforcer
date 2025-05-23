from flask import Blueprint, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
import requests
from app import db
from app.models import User
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/discord')
def discord_login():
    return redirect(
        f"{Config.DISCORD_AUTH_URL}?"
        f"client_id={Config.DISCORD_CLIENT_ID}&"
        f"redirect_uri={Config.DISCORD_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=identify%20email"
    )

@auth_bp.route('/callback/discord')
def discord_callback():
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    data = {
        'client_id': Config.DISCORD_CLIENT_ID,
        'client_secret': Config.DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': Config.DISCORD_REDIRECT_URI,
        'scope': 'identify email'
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Получаем токен
    response = requests.post(Config.DISCORD_TOKEN_URL, data=data, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Token exchange failed"}), 400
    
    token_data = response.json()
    
    # Получаем данные пользователя
    headers = {
        'Authorization': f'Bearer {token_data["access_token"]}'
    }
    user_response = requests.get(f'{Config.DISCORD_API_BASE}/users/@me', headers=headers)
    if user_response.status_code != 200:
        return jsonify({"error": "Failed to fetch user data"}), 400
    
    user_data = user_response.json()
    
    # Сохраняем/обновляем пользователя
    user = User.query.filter_by(discord_id=user_data['id']).first()
    if not user:
        user = User(
            discord_id=user_data['id'],
            username=user_data['username'],
            discriminator=user_data['discriminator'],
            avatar=user_data.get('avatar'),
            access_token=token_data['access_token'],
            refresh_token=token_data['refresh_token'],
            is_admin=user_data['id'] in ["YOUR_DISCORD_ID_HERE"]  # Админы
        )
        db.session.add(user)
    else:
        user.access_token = token_data['access_token']
        user.refresh_token = token_data['refresh_token']
    
    db.session.commit()
    login_user(user)
    
    return jsonify({
        "status": "success",
        "user": {
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin,
            "token": token_data['access_token']
        }
    })

@auth_bp.route('/logout')
def logout():
    logout_user()
    return jsonify({"status": "success"})