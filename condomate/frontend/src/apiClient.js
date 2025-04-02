import axios from 'axios';

// Use environment variable for API base URL, default for local dev
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://0s85lrdrl0.execute-api.us-east-1.amazonaws.com/prod/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false,  // Disable credentials since we're using API Gateway
});

// Helper function to decode JWT token
function decodeJWT(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Error decoding JWT:', error);
    return null;
  }
}

// Interceptor to add JWT token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    console.log('Current token from localStorage:', token ? 'Present' : 'Missing');
    
    // Special handling for auth token request
    if (config.url === '/api/v1/auth/token') {
      config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
      // Remove any existing Authorization header for auth requests
      delete config.headers.Authorization;
      
      // Convert data to URLSearchParams if it's not already
      if (!(config.data instanceof URLSearchParams)) {
        const formData = new URLSearchParams();
        formData.append('username', config.data.username);
        formData.append('password', config.data.password);
        config.data = formData;
      }
    } else if (token) {
      // For all other requests, add the token with Bearer prefix
      // Ensure the token doesn't already have the Bearer prefix
      const cleanToken = token.startsWith('Bearer ') ? token.slice(7) : token;
      config.headers.Authorization = `Bearer ${cleanToken}`;
      
      // Decode and log token contents
      const decodedToken = decodeJWT(cleanToken);
      console.log('Decoded token:', decodedToken);
      
      console.log('Setting Authorization header:', config.headers.Authorization);
      
      // Log the full request details for debugging
      console.log('Request details:', {
        url: `${config.baseURL}${config.url}`,
        method: config.method,
        headers: config.headers,
        token: cleanToken.substring(0, 20) + '...'
      });
    }

    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for better error handling
apiClient.interceptors.response.use(
  (response) => {
    // If this is a token response, store the token
    if (response.config.url === '/api/v1/auth/token') {
      const { access_token, refresh_token, token_type } = response.data;
      console.log('Received token response:', { 
        hasAccessToken: !!access_token,
        hasRefreshToken: !!refresh_token,
        accessTokenLength: access_token?.length,
        tokenType: token_type
      });
      
      // Decode and log the new token
      const decodedToken = decodeJWT(access_token);
      console.log('Decoded new token:', decodedToken);
      
      // Store the raw token without any prefix
      localStorage.setItem('token', access_token);
      
      if (refresh_token) {
        localStorage.setItem('refreshToken', refresh_token);
      }
      
      // Verify token was stored
      const storedToken = localStorage.getItem('token');
      console.log('Token stored in localStorage:', storedToken ? 'Success' : 'Failed');
    }

    // For /users/me endpoint, handle the response specially
    if (response.config.url === '/api/v1/users/me') {
      console.log('Users/me response details:', {
        status: response.status,
        headers: response.headers,
        authHeader: response.config.headers.Authorization,
        data: response.data,
        requestHeaders: response.config.headers,
        requestUrl: response.config.url,
        requestBaseURL: response.config.baseURL,
        requestMethod: response.config.method
      });

      // If we get a 200 but with "Not authenticated", return the response
      // but let the AuthContext handle the error
      if (response.status === 200 && response.data.detail === 'Not authenticated') {
        console.error('Received "Not authenticated" response despite valid token');
        return response;
      }
    }

    return response;
  },
  async (error) => {
    // Enhanced error logging
    console.error('Response error:', {
      status: error.response?.status,
      data: error.response?.data,
      headers: error.response?.headers,
      message: error.message,
      config: {
        url: error.config?.url,
        method: error.config?.method,
        baseURL: error.config?.baseURL,
        headers: error.config?.headers,
        token: localStorage.getItem('token') ? 'Present' : 'Missing'
      }
    });
    
    const originalRequest = error.config;

    // If the error is 401 and we haven't tried to refresh the token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        // Try to refresh the token
        const response = await apiClient.post('/api/v1/auth/refresh', {
          refresh_token: refreshToken
        });

        const { access_token } = response.data;
        localStorage.setItem('token', access_token);

        // Retry the original request
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
        // Clear tokens and throw error
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        throw new Error('Session expired. Please log in again.');
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient; 