import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
# CORS(app, supports_credentials=True)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "supports_credentials": True,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    }
})  


# Service URLs from environment variables
USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL', 'http://localhost:5001')
IMAGE_SERVICE_URL = os.environ.get('IMAGE_SERVICE_URL', 'http://localhost:5002')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API Gateway is operational"})

# User Service Routes
@app.route('/api/users/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_service_proxy(path):
    url = f"{USER_SERVICE_URL}/{path}"
    return proxy_request(url)

@app.route('/api/auth/<path:path>', methods=['GET', 'POST'])
def auth_proxy(path):
    url = f"{USER_SERVICE_URL}/{path}"  # ✅ Correct URL
    return proxy_request(url)

# Image Service Routes
@app.route('/api/images/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def image_service_proxy(path):
    url = f"{IMAGE_SERVICE_URL}/{path}"
    return proxy_request(url)

@app.route('/api/generate', methods=['POST'])
def generate_image_proxy():
    url = f"{IMAGE_SERVICE_URL}/generate"
    return proxy_request(url)

def proxy_request(url):
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers 
                     if key.lower() not in ['host', 'content-length']},
            data=request.get_data(),
            cookies=request.cookies,
            params=request.args,
            allow_redirects=False
        )

        # Forward headers excluding hop-by-hop headers
        excluded_headers = ['content-encoding', 'content-length', 'connection']
        headers = [
            (name, value) for (name, value) in response.raw.headers.items()
            if name.lower() not in excluded_headers
        ]

        content = response.content
        if not content:
            content = b''

        # Create Flask response
        proxy_response = app.response_class(
            response=content,
            status=response.status_code,
            headers=dict(headers)
        )

        return proxy_response

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Service unavailable"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)