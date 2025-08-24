import { User } from '../types';

const API_BASE_URL = 'http://localhost:8000';

export class ApiError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function handleResponse(response: Response) {
  if (!response.ok) {
    const error = await response.json();
    throw new ApiError(response.status, error.detail || 'Something went wrong');
  }
  return response.json();
}

export const api = {
  auth: {
    login: async (email: string, password: string) => {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });
      return handleResponse(response);
    },

    me: async (token: string) => {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      return handleResponse(response);
    },

    refreshToken: async (refresh_token: string) => {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token }),
      });
      return handleResponse(response);
    }
  },

  users: {
    register: async (userData: { name: string; email: string; password: string; api_key?: string }) => {
      const response = await fetch(`${API_BASE_URL}/users/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });
      return handleResponse(response);
    },

    checkUsername: async (username: string) => {
      const response = await fetch(`${API_BASE_URL}/users/check-username?username=${encodeURIComponent(username)}`);
      return handleResponse(response);
    },

    sendOtp: async (email: string) => {
      const response = await fetch(`${API_BASE_URL}/users/send-otp`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });
      return handleResponse(response);
    },

    verifyOtp: async (email: string, otp: string) => {
      const response = await fetch(`${API_BASE_URL}/users/verify-otp`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, otp }),
      });
      return handleResponse(response);
    },

    updateApiKey: async (token: string, apiKey: string) => {
      const response = await fetch(`${API_BASE_URL}/users/update-api-key`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ api_key: apiKey }),
      });
      return handleResponse(response);
    },

    getApiKey: async (token: string) => {
      const response = await fetch(`${API_BASE_URL}/users/api-key`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      return handleResponse(response);
    }
  }
};
