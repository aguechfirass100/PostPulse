# Microservices Project with Flask and Docker

This project consists of a microservices architecture using Flask and Docker, including:

1. API Gateway
2. User Service with Google/Facebook OAuth
3. Image Generation Service

## Project Structure

```
microservices-project/
├── api-gateway/
│   ├── app.py
│   └── requirements.txt
├── user-service/
│   ├── app.py
│   ├── models.py
│   ├── auth.py
│   ├── database.py
│   └── requirements.txt
├── image-service/
│   ├── app.py
│   ├── image_generator.py
│   └── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Prerequisites

- Docker and Docker Compose
- Google and Facebook Developer accounts (for OAuth)

## Configuration

Before running the application, you need to set up your OAuth credentials:

1. **Create Google OAuth Credentials**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Navigate to APIs & Services > Credentials
   - Create OAuth client ID credentials
   - Set the authorized redirect URI to `http://localhost:8000/api/auth/google/callback`

2. **Create Facebook OAuth Credentials**:
   - Go to the [Facebook Developer Portal](https://developers.facebook.com/)
   - Create a new app
   - Add the Facebook Login product
   - Set the OAuth redirect URI to `http://localhost:8000/api/auth/facebook/callback`

3. **Update Environment Variables**:
   - Open `docker-compose.yml`
   - Update the following environment variables in the `user-service` section:

     ```yaml
     - GOOGLE_CLIENT_ID=your_google_client_id
     - GOOGLE_CLIENT_SECRET=your_google_client_secret
     - FACEBOOK_CLIENT_ID=your_facebook_client_id
     - FACEBOOK_CLIENT_SECRET=your_facebook_client_secret
     - JWT_SECRET=your_jwt_secret_key_here
     ```

## Running the Application

1. Build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```

2. The services will be available at:
   - API Gateway: `http://localhost:8000`
   - User Service (via Gateway): `http://localhost:8000/api/users`
   - Image Service (via Gateway): `http://localhost:8000/api/images`

## API Endpoints

### User Service

- **Health Check**: `GET /api/users/health`
- **Google Login**: `GET /api/auth/google/login`
- **Facebook Login**: `GET /api/auth/facebook/login`
- **Get Current User**: `GET /api/users/me` (Requires Authentication)
- **Get User by ID**: `GET /api/users/{user_id}` (Requires Authentication)
- **Search Users**: `GET /api/users/search?q={query}` (Requires Authentication)
- **Update User Profile**: `PUT /api/users/update` (Requires Authentication)

### Image Service

- **Health Check**: `GET /api/images/health`
- **Generate Image**: `POST /api/generate` (Requires Authentication)

  ```json
  {
    "prompt": "A beautiful mountain landscape",
    "width": 512,
    "height": 512
  }
  ```

- **Get Service Status**: `GET /api/images/status` (Requires Authentication)

## Authentication

The services use JWT-based authentication. After logging in with Google or Facebook, you'll receive a JWT token that should be included in the `Authorization` header for authenticated endpoints:

```
Authorization: Bearer your_jwt_token
```

## Microservices Communication

The services communicate with each other through the API Gateway, which routes requests to the appropriate service. Each service has its own database connection and is responsible for its own data.

## Development Notes

- The image generation service provides a mock implementation. In a production environment, you would integrate with a real ML model like DALL-E or Stable Diffusion.
- MongoDB is used for user data storage. Data is persisted between container restarts using a Docker volume.
- The services share a single Dockerfile with service-specific arguments to simplify the deployment.

## Security Considerations

- OAuth secrets and JWT keys should be stored securely in production, not in the Docker Compose file.
- The current implementation is for development purposes. For production, additional security measures like HTTPS, rate limiting, and more robust authentication would be necessary.
