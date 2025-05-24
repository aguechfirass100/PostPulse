from flask import Flask, request, jsonify
from flask_cors import CORS
from models import User
from database import db
from auth import (
    create_user,
    facebook_callback,
    facebook_login,
    google_callback,
    google_login,
    verify_password,
    generate_token,
    verify_token
)
import os
from datetime import datetime

app = Flask(__name__)
# CORS(app)
# CORS(app, supports_credentials=True)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)


users_collection = db.get_collection('users')  # Add this line


# Configure MongoDB
# app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://mongo:27017/user_service")
# db.init_app(app)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "user-service"})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    try:
        # Validate required fields
        required_fields = ["email", "password", "name"]
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing required field: {field}"}), 400

        # Check if user exists using PyMongo
        existing_user = users_collection.find_one({"email": data["email"]})
        if existing_user:
            return jsonify({"message": "Email already registered"}), 409

        # Create user
        user = create_user(
            email=data["email"],
            password=data["password"],
            name=data["name"],
            provider="local"
        )

        return jsonify({
            "id": user["_id"],
            "email": user["email"],
            "name": user["username"],
            "provider": user["auth_provider"],
            "createdAt": user["created_at"],
            "updatedAt": user["updated_at"]
        }), 201
    except Exception as e:
        return jsonify({"message": f"Error creating user: {str(e)}"}), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    if "email" not in data or "password" not in data:
        return jsonify({"message": "Email and password are required"}), 400
    
    try:
        # Find user by email using PyMongo
        user_data = users_collection.find_one({"email": data["email"]})
        
        if not user_data:
            return jsonify({"message": "Invalid email or password"}), 401
        
        # Convert MongoDB ObjectId to string
        user_data["_id"] = str(user_data["_id"])
        
        # Create User object from raw data
        user = User.from_dict(user_data)
        
        # Verify password
        if not verify_password(data["password"], user.password_hash):
            return jsonify({"message": "Invalid email or password"}), 401
        
        # Generate token with user ID
        token = generate_token(user._id)
        
        return jsonify({
            "token": token,
            "user": {
                "id": user._id,
                "email": user.email,
                "name": user.username,
                "profilePicture": user.profile_image,
                "provider": user.auth_provider,
                "createdAt": user.created_at,
                "updatedAt": user.updated_at
            }
        })
        
    except Exception as e:
        return jsonify({"message": f"Login error: {str(e)}"}), 500
    
    

@app.route("/me", methods=["GET"])
def get_current_user():
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Authorization header required"}), 401
    
    token = auth_header.split(" ")[1]
    user_id = verify_token(token)
    
    if not user_id:
        return jsonify({"message": "Invalid or expired token"}), 401
    
    user = User.objects(id=user_id).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        "id": str(user.id),
        "email": user.email,
        "name": user.username,
        "profilePicture": user.profile_picture,
        "provider": user.provider,
        "createdAt": user.created_at.isoformat(),
        "updatedAt": user.updated_at.isoformat()
    })

@app.route("/logout", methods=["POST"])
def logout():
    # In a more complex implementation, you might want to invalidate the token
    # For now, we'll just return a success response as token management is handled client-side
    return jsonify({"message": "Logged out successfully"})



# OAuth Routes
@app.route("/auth/google/login", methods=["GET"])
def handle_google_login():
    return google_login()

@app.route("/auth/google/callback", methods=["GET"])
def handle_google_callback():
    return google_callback()

@app.route("/auth/facebook/login", methods=["GET"])
def handle_facebook_login():
    return facebook_login()

@app.route("/auth/facebook/callback", methods=["GET"])
def handle_facebook_callback():
    return facebook_callback()



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)