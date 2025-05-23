from flask import Blueprint, jsonify
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return jsonify({"status": "API is running"})

@main_bp.route('/api/data')
@login_required
def protected_data():
    return jsonify({"data": "This is protected data"})