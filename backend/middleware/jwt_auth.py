from functools import wraps
from flask import request, jsonify, g
from utils.token_utils import decode_jwt


def jwt_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Decode and verify token
        payload = decode_jwt(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Store user_id in Flask's g object for route access
        g.user_id = payload['user_id']
        
        return f(*args, **kwargs)
    
    return decorated


def get_current_user_id() -> str:
    """Get current authenticated user's ID"""
    return getattr(g, 'user_id', None)
