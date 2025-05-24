'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User } from '../services/types';
import { authService } from '../services/authService';

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name: string) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Check if user is already logged in on component mount
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('auth_token');
      if (storedToken) {
        try {
          setToken(storedToken);
  
          const rawUserData = await authService.getCurrentUser();
  
          const userData: User = {
            id: rawUserData._id,
            name: rawUserData.username,
            email: rawUserData.email,
            createdAt: rawUserData.created_at,
            updatedAt: rawUserData.updated_at
          };
  
          setUser(userData);
        } catch (err) {
          localStorage.removeItem('auth_token');
          setToken(null);
        }
      }
      setLoading(false);
    };
  
    initAuth();
  }, []);
  

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      setError(null);
  
      const { user: rawLoginUser, token: authToken } = await authService.login(email, password);
      localStorage.setItem('auth_token', authToken);
      setToken(authToken);
  
      const rawUserData = await authService.getCurrentUser();
  
      const formattedUser: User = {
        id: rawUserData._id,
        name: rawUserData.username,
        email: rawUserData.email,
        createdAt: rawUserData.created_at,
        updatedAt: rawUserData.updated_at
      };
  
      setUser(formattedUser);
    } catch (err: any) {
      setError(err.message || 'Failed to login');
      throw err;
    } finally {
      setLoading(false);
    }
  };
  

  const signup = async (email: string, password: string, name: string) => {
    try {
      setLoading(true);
      setError(null);
  
      // Sign up the user
      await authService.signup(email, password, name);
  
      // After signup, automatically log them in
      const { token: authToken } = await authService.login(email, password);
      localStorage.setItem('auth_token', authToken);
      setToken(authToken);
  
      // Fetch the current user info
      const rawUserData = await authService.getCurrentUser();
  
      const formattedUser: User = {
        id: rawUserData._id,
        name: rawUserData.username,
        email: rawUserData.email,
        createdAt: rawUserData.created_at,
        updatedAt: rawUserData.updated_at
      };
  
      setUser(formattedUser);
    } catch (err: any) {
      setError(err.message || 'Failed to sign up');
      throw err;
    } finally {
      setLoading(false);
    }
  };
  

  const logout = async () => {
    try {
      setLoading(true);
      if (token) {
        await authService.logout();
      }
      localStorage.removeItem('auth_token');
      setToken(null);
      setUser(null);
    } catch (err: any) {
      setError(err.message || 'Failed to logout');
    } finally {
      setLoading(false);
    }
  };

  const clearError = () => {
    setError(null);
  };

  const value = {
    user,
    token,
    loading,
    error,
    login,
    signup,
    logout,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};