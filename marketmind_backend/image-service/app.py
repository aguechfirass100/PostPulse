import os
import json
import jwt
from flask import Flask, request, jsonify
from flask_cors import CORS
from image_generator import ImageGenerator

app = Flask(__name__)
# CORS(app)
# CORS(app, supports_credentials=True)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)


# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'your_jwt_secret_key_here')

def get_token_from_request():
    """Extract token from Authorization header"""
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1]
    return None

def verify_token(token):
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator to ensure user is authenticated"""
    def decorated(*args, **kwargs):
        token = get_token_from_request()
        if not token:
            return jsonify({"error": "Authentication required"}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        request.user_id = payload.get('user_id')
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Image generation service is operational"})

@app.route('/generate', methods=['POST'])
@require_auth
def generate_image():
    """Generate an image based on the provided prompt"""
    data = request.json
    
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400
    
    prompt = data['prompt']
    width = data.get('width', 512)
    height = data.get('height', 512)
    
    # Validate parameters
    if not isinstance(prompt, str) or not prompt.strip():
        return jsonify({"error": "Invalid prompt"}), 400
    
    try:
        width = int(width)
        height = int(height)
        
        # Limit dimensions to reasonable values
        width = max(64, min(width, 1024))
        height = max(64, min(height, 1024))
    except:
        return jsonify({"error": "Invalid dimensions"}), 400
    
    # Generate the image
    try:
        image_data = ImageGenerator.generate_image(prompt, width, height)
        
        # Return the base64 encoded image data
        return jsonify({
            "image": image_data,
            "prompt": prompt,
            "width": width,
            "height": height
        })
    except Exception as e:
        return jsonify({"error": f"Image generation failed: {str(e)}"}), 500

@app.route('/status', methods=['GET'])
@require_auth
def get_service_status():
    """Get service status and capabilities"""
    return jsonify({
        "status": "operational",
        "service": "image-generation",
        "capabilities": {
            "max_width": 1024,
            "max_height": 1024,
            "formats": ["png"],
            "models": ["mock-generator"]  # In a real app, this would list the available ML models
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)