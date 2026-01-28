from datetime import datetime
from bson import ObjectId
import bcrypt


class User:
    """User model for MongoDB"""
    
    def __init__(self, db):
        self.collection = db['users']
        # Create unique index on email
        self.collection.create_index('email', unique=True)
    
    def create(self, name: str, email: str, password: str) -> dict:
        """Create a new user with hashed password"""
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_doc = {
            'name': name,
            'email': email.lower(),
            'password_hash': password_hash,
            'created_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(user_doc)
        user_doc['_id'] = result.inserted_id
        return self._serialize(user_doc)
    
    def find_by_email(self, email: str) -> dict | None:
        """Find user by email"""
        user = self.collection.find_one({'email': email.lower()})
        if user:
            return user
        return None
    
    def find_by_id(self, user_id: str) -> dict | None:
        """Find user by ID"""
        try:
            user = self.collection.find_one({'_id': ObjectId(user_id)})
            if user:
                return self._serialize(user)
        except Exception:
            pass
        return None
    
    def verify_password(self, user: dict, password: str) -> bool:
        """Verify password against stored hash"""
        return bcrypt.checkpw(password.encode('utf-8'), user['password_hash'])
    
    def _serialize(self, user: dict) -> dict:
        """Serialize user document (exclude password)"""
        return {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'created_at': user['created_at'].isoformat()
        }
