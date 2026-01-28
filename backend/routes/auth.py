from flask import Blueprint, request, jsonify, current_app
from pymongo.errors import DuplicateKeyError
from models import User
from utils.token_utils import generate_jwt
from middleware.jwt_auth import jwt_required, get_current_user_id

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def get_user_model():
    """Get User model instance"""
    return User(current_app.db)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Register a new user"""
    data = request.get_json()
    
    # Validate required fields
    if not all(key in data for key in ['name', 'email', 'password']):
        return jsonify({'error': 'Name, email, and password are required'}), 400
    
    name = data['name'].strip()
    email = data['email'].strip()
    password = data['password']
    
    # Validate password length
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    try:
        user_model = get_user_model()
        user = user_model.create(name, email, password)
        token = generate_jwt(user['id'])
        
        current_app.logger.info(f"New user registered: {email}")
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': user
        }), 201
        
    except DuplicateKeyError:
        current_app.logger.warning(f"Registration failed - email exists: {email}")
        return jsonify({'error': 'Email already registered'}), 409


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT"""
    # Rate limit: 5 logins per minute
    if hasattr(current_app, 'limiter'):
       limit = current_app.limiter.limit("5 per minute")
       limit(request.endpoint)

    data = request.get_json()
    
    if not all(key in data for key in ['email', 'password']):
        return jsonify({'error': 'Email and password are required'}), 400
    
    user_model = get_user_model()
    user = user_model.find_by_email(data['email'])
    
    if not user or not user_model.verify_password(user, data['password']):
        current_app.logger.warning(f"Failed login attempt for: {data.get('email', 'unknown')}")
        return jsonify({'error': 'Invalid email or password'}), 401
    
    token = generate_jwt(str(user['_id']))
    
    current_app.logger.info(f"Successful login for: {user['email']}")
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email']
        }
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required
def get_profile():
    """Get current user profile"""
    user_model = get_user_model()
    user = user_model.find_by_id(get_current_user_id())
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user}), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    """Logout user (client should discard token)"""
    # In a production app, you might want to blacklist the token
    # For this implementation, the client simply discards the token
    return jsonify({'message': 'Logged out successfully'}), 200
