// src/services/auth.service.ts

interface User {
  _id: string;
  username: string;
  email: string;
  profile_image?: string;
  auth_provider: string;
  created_at: string;
  updated_at: string;
}

interface AuthResponse {
  user: User;
  token: string;
}

class AuthService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = 'http://localhost:8000/api/auth';
  }

  // Email/Password Authentication
  async signup(email: string, password: string, username: string): Promise<AuthResponse> {
    const response = await fetch(`${this.baseUrl}/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password, name: username }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Registration failed. Please try again.');
    }

    const data = await response.json();
    this.storeAuthData(data);
    return data;
  }

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await fetch(`${this.baseUrl}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Invalid credentials. Please try again.');
    }

    const data = await response.json();
    this.storeAuthData(data);
    return data;
  }

  // OAuth Authentication
  async initiateOAuth(provider: 'google' | 'facebook'): Promise<{ redirectUrl: string }> {
    const response = await fetch(`${this.baseUrl}/${provider}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || `Could not connect to ${provider}. Please try again.`);
    }

    return response.json();
  }

  async handleOAuthCallback(provider: 'google' | 'facebook', code: string): Promise<AuthResponse> {
    const response = await fetch(`${this.baseUrl}/${provider}/callback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || `Authentication with ${provider} failed. Please try again.`);
    }

    const data = await response.json();
    this.storeAuthData(data);
    return data;
  }

  // User Management
  async getCurrentUser(): Promise<User> {
    const token = this.getToken();
    if (!token) throw new Error('No authentication token found');

    const response = await fetch(`${this.baseUrl}/users/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to fetch user data');
    }

    return response.json();
  }

  async updateProfile(updateData: { username?: string; profile_image?: string }): Promise<User> {
    const token = this.getToken();
    if (!token) throw new Error('No authentication token found');

    const response = await fetch(`${this.baseUrl}/users/me`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(updateData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to update profile');
    }

    const updatedUser = await response.json();
    this.storeUserData(updatedUser);
    return updatedUser;
  }

  // Session Management
  private storeAuthData(data: AuthResponse): void {
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
  }

  private storeUserData(user: User): void {
    localStorage.setItem('user', JSON.stringify(user));
  }

  getToken(): string | null {
    return localStorage.getItem('authToken');
  }

  getUser(): User | null {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  logout(): void {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  }
}

export const authService = new AuthService();









// // API service for authentication-related requests

// interface User {
//     _id: string;
//     username: string;
//     email: string;
//     profile_image?: string;
//     auth_provider: string;
//     created_at: string;
//     updated_at: string;
//   }
  
//   interface AuthResponse {
//     user: User;
//     token: string;
//   }
  
//   class AuthService {
//     private baseUrl: string;
  
//     constructor() {
//       this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
//     }
  
//     /**
//      * Get the current user's profile
//      */
//     async getCurrentUser(): Promise<User> {
//       const token = localStorage.getItem('authToken');
      
//       if (!token) {
//         throw new Error('Not authenticated');
//       }
  
//       const response = await fetch(`${this.baseUrl}/users/me`, {
//         method: 'GET',
//         headers: {
//           'Content-Type': 'application/json',
//           'Authorization': `Bearer ${token}`
//         },
//       });
  
//       if (!response.ok) {
//         const error = await response.json();
//         throw new Error(error.error || 'Failed to get user profile');
//       }
  
//       return response.json();
//     }
  
//     /**
//      * Start OAuth flow for a provider
//      */
//     async initiateOAuth(provider: 'google' | 'facebook'): Promise<{ redirect_url: string }> {
//       const response = await fetch(`${this.baseUrl}/auth/${provider}/login`, {
//         method: 'GET',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//       });
  
//       if (!response.ok) {
//         const error = await response.json();
//         throw new Error(error.error || `Failed to initiate ${provider} login`);
//       }
  
//       return response.json();
//     }
  
//     /**
//      * Process OAuth callback
//      */
//     async processOAuthCallback(
//       provider: 'google' | 'facebook', 
//       callbackUrl: string
//     ): Promise<AuthResponse> {
//       // Extract just the path and query parameters
//       const urlObj = new URL(callbackUrl);
//       const query = urlObj.search;
      
//       const response = await fetch(`${this.baseUrl}/auth/${provider}/callback${query}`, {
//         method: 'GET',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//       });
  
//       if (!response.ok) {
//         const error = await response.json();
//         throw new Error(error.error || 'Authentication failed');
//       }
  
//       return response.json();
//     }
  
//     /**
//      * Update user profile
//      */
//     async updateUserProfile(data: { username?: string; profile_image?: string }): Promise<User> {
//       const token = localStorage.getItem('authToken');
      
//       if (!token) {
//         throw new Error('Not authenticated');
//       }
  
//       const response = await fetch(`${this.baseUrl}/users/update`, {
//         method: 'PUT',
//         headers: {
//           'Content-Type': 'application/json',
//           'Authorization': `Bearer ${token}`
//         },
//         body: JSON.stringify(data),
//       });
  
//       if (!response.ok) {
//         const error = await response.json();
//         throw new Error(error.error || 'Failed to update profile');
//       }
  
//       const updatedUser = await response.json();
      
//       // Update stored user
//       localStorage.setItem('user', JSON.stringify(updatedUser));
      
//       return updatedUser;
//     }
  
//     /**
//      * Log the user out
//      */
//     logout(): void {
//       localStorage.removeItem('authToken');
//       localStorage.removeItem('user');
//     }
//   }
  
//   export const authService = new AuthService();
