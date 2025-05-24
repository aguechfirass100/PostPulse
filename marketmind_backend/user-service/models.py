from datetime import datetime
from bson import ObjectId
import json

class User:
    def __init__(self, username, email, password_hash=None, auth_provider=None, 
                 auth_provider_id=None, profile_image=None, created_at=None, updated_at=None, _id=None):
        self._id = str(ObjectId()) if _id is None else _id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.auth_provider = auth_provider  # 'local', 'google', 'facebook'
        self.auth_provider_id = auth_provider_id  # ID from auth provider if using social login
        self.profile_image = profile_image
        self.created_at = datetime.utcnow().isoformat() if created_at is None else created_at
        self.updated_at = datetime.utcnow().isoformat() if updated_at is None else updated_at

    @classmethod
    def from_dict(cls, data):
        """Create a User object from a dictionary"""
        return cls(
            _id=data.get('_id'),
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            auth_provider=data.get('auth_provider'),
            auth_provider_id=data.get('auth_provider_id'),
            profile_image=data.get('profile_image'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    

    def to_dict(self):
        """Convert User object to a dictionary"""
        return {
            '_id': self._id,
            'username': self.username,
            'email': self.email,
            'auth_provider': self.auth_provider,
            'profile_image': self.profile_image,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def to_json(self):
        """Convert User object to a JSON string"""
        return json.dumps(self.to_dict())

    def safe_dict(self):
        """Return a dictionary without sensitive data"""
        data = self.to_dict()
        data.pop('password_hash', None)
        data.pop('auth_provider_id', None)
        return data