import os
import jwt
import json
import requests
from datetime import datetime, timedelta
from requests_oauthlib import OAuth2Session
from flask import request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId  # Add this import
from database import Database
from models import User

# JWT Configuration
JWT_SECRET = ''  # Set this to your secret key
JWT_EXPIRATION_HOURS = 24
SERVICE_BASE_URL = os.environ.get('SERVICE_BASE_URL', 'http://localhost:8000')

# OAuth Configurations
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''  # Set these to your Google OAuth credentials
GOOGLE_AUTH_BASE_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

FACEBOOK_CLIENT_ID = 'your_facebook_client_id_here'  # Set this to your Facebook OAuth credentials
FACEBOOK_CLIENT_SECRET = 'your_facebook_client_secret_here'  # Set this to your Facebook OAuth credentials
FACEBOOK_AUTH_BASE_URL = 'https://www.facebook.com/v12.0/dialog/oauth'
FACEBOOK_TOKEN_URL = 'https://graph.facebook.com/v12.0/oauth/access_token'
FACEBOOK_USER_INFO_URL = 'https://graph.facebook.com/me'

# Database setup
db = Database()
users_collection = db.get_collection('users')

# --- Core Authentication Functions ---
def create_user(email, password=None, name=None, provider="local", profile_picture=None, auth_provider_id=None):
    """Central user creation function"""
    password_hash = generate_password_hash(password) if password else None
    user_data = {
        "username": name,
        "email": email,
        "password_hash": password_hash,
        "auth_provider": provider,
        "auth_provider_id": auth_provider_id,
        "profile_image": profile_picture,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = users_collection.insert_one(user_data)
    user_data["_id"] = result.inserted_id  # Store as ObjectId
    return User.from_dict(user_data)

def generate_token(user_id):
    """Generate JWT token with string user ID"""
    payload = {
        'user_id': str(user_id),  # Convert ObjectId to string
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def authenticate_user():
    """Retrieve user from JWT token"""
    token = get_token_from_request()
    if not token:
        return None

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user_id = ObjectId(payload['user_id'])  # Convert back to ObjectId
        user_data = users_collection.find_one({'_id': user_id})
        return User.from_dict(user_data) if user_data else None
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
        return None

# --- OAuth Common Functions ---
def handle_oauth_callback(provider, user_info_func):
    """Generic OAuth callback handler"""
    try:
        # State validation for CSRF protection
        request_state = request.args.get('state')
        session_state = session.get('oauth_state')
        if not session_state or request_state != session_state:
            return jsonify({"error": "Invalid state parameter"}), 403

        # Get user info from provider
        user_info = user_info_func()
        
        # Find or create user
        existing_user = users_collection.find_one({
            "auth_provider": provider,
            "auth_provider_id": user_info['id']
        })
        
        if existing_user:
            user = User.from_dict(existing_user)
        else:
            user = create_user(
                email=user_info['email'],
                name=user_info.get('name'),
                provider=provider,
                profile_picture=user_info.get('picture'),
                auth_provider_id=user_info['id']
            )
        
        return jsonify({
            "user": user.safe_dict(),
            "token": generate_token(user._id)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- Google OAuth Implementation ---
def google_login():
    """Initiate Google OAuth flow"""
    redirect_uri = f"{SERVICE_BASE_URL}/api/auth/google/callback"
    google = OAuth2Session(
        GOOGLE_CLIENT_ID,
        redirect_uri=redirect_uri,
        scope=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
    )
    authorization_url, state = google.authorization_url(GOOGLE_AUTH_BASE_URL, access_type="offline")
    session['oauth_state'] = state
    return jsonify({"redirect_url": authorization_url})

def google_callback():
    """Handle Google OAuth callback"""
    def fetch_user_info():
        google = OAuth2Session(GOOGLE_CLIENT_ID, state=session['oauth_state'])
        token = google.fetch_token(
            GOOGLE_TOKEN_URL,
            client_secret=GOOGLE_CLIENT_SECRET,
            authorization_response=request.url
        )
        resp = google.get(GOOGLE_USER_INFO_URL)
        user_info = resp.json()
        return {
            'id': user_info['sub'],
            'email': user_info['email'],
            'name': user_info.get('name'),
            'picture': user_info.get('picture')
        }
    
    return handle_oauth_callback('google', fetch_user_info)

# --- Facebook OAuth Implementation ---
def facebook_login():
    """Initiate Facebook OAuth flow"""
    redirect_uri = f"{SERVICE_BASE_URL}/api/auth/facebook/callback"
    facebook = OAuth2Session(
        FACEBOOK_CLIENT_ID,
        redirect_uri=redirect_uri,
        scope=["email", "public_profile"]
    )
    authorization_url, state = facebook.authorization_url(FACEBOOK_AUTH_BASE_URL)
    session['oauth_state'] = state
    return jsonify({"redirect_url": authorization_url})

def facebook_callback():
    """Handle Facebook OAuth callback"""
    def fetch_user_info():
        facebook = OAuth2Session(FACEBOOK_CLIENT_ID, state=session['oauth_state'])
        token = facebook.fetch_token(
            FACEBOOK_TOKEN_URL,
            client_secret=FACEBOOK_CLIENT_SECRET,
            authorization_response=request.url
        )
        resp = facebook.get(FACEBOOK_USER_INFO_URL, params={'fields': 'id,name,email,picture'})
        user_info = resp.json()
        return {
            'id': user_info['id'],
            'email': user_info.get('email'),
            'name': user_info.get('name'),
            'picture': user_info.get('picture', {}).get('data', {}).get('url')
        }
    
    return handle_oauth_callback('facebook', fetch_user_info)

# --- Password Utilities ---
def verify_password(plain_password, hashed_password):
    return check_password_hash(hashed_password, plain_password)

def get_token_from_request():
    auth_header = request.headers.get('Authorization')
    return auth_header.split(' ')[1] if auth_header and auth_header.startswith('Bearer ') else None

# --- Decorators ---
def require_auth(f):
    def decorated(*args, **kwargs):
        user = authenticate_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        request.current_user = user
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated