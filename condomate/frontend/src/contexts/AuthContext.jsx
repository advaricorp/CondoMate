import React, { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../apiClient';

const AuthContext = createContext(null);

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        console.log('Checking auth with token:', token.substring(0, 20) + '...');
        const response = await apiClient.get('/api/v1/users/me');
        console.log('Auth check response:', response.data);
        console.log('Auth check headers:', response.headers);
        
        if (response.data && !response.data.detail) {
          setUser(response.data);
          setIsAuthenticated(true);
        } else {
          console.error('Invalid user data:', response.data);
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          setUser(null);
          setIsAuthenticated(false);
        }
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      console.log('Attempting login for:', email);
      const response = await apiClient.post('/api/v1/auth/token', {
        username: email,
        password: password
      });

      console.log('Token response received:', response.data);
      console.log('Token response headers:', response.headers);
      
      if (!response.data.access_token) {
        throw new Error('No access token received');
      }
      
      // Store the token
      localStorage.setItem('token', response.data.access_token);
      if (response.data.refresh_token) {
        localStorage.setItem('refreshToken', response.data.refresh_token);
      }
      
      // Add a small delay to ensure the token is properly stored
      await new Promise(resolve => setTimeout(resolve, 100));
      
      try {
        // The token is now handled by the API client interceptor
        const userResponse = await apiClient.get('/api/v1/users/me');
        console.log('User data response:', userResponse.data);
        console.log('User data headers:', userResponse.headers);
        
        if (userResponse.data && !userResponse.data.detail) {
          setUser(userResponse.data);
          setIsAuthenticated(true);
          return userResponse.data;
        } else {
          console.error('Invalid user data:', userResponse.data);
          // Clear tokens but don't redirect
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          setUser(null);
          setIsAuthenticated(false);
          throw new Error('Invalid credentials. Please try again.');
        }
      } catch (error) {
        console.error('Failed to get user data:', error);
        // Clear tokens but don't redirect
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        setUser(null);
        setIsAuthenticated(false);
        throw new Error('Invalid credentials. Please try again.');
      }
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    loading,
    login,
    logout,
    isAuthenticated
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export { AuthProvider, useAuth }; 