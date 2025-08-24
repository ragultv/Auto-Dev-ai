import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { api } from '../service/api';

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string, apiKeys?: User['apiKeys']) => Promise<void>;
  signup: (name: string, email: string, password: string, apiKeys?: User['apiKeys']) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored user data
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string, apiKeys?: User['apiKeys']) => {
    try {
      const { access_token, refresh_token } = await api.auth.login(email, password);
      const userData = await api.auth.me(access_token);

      // Get API key if available
      try {
        await api.users.getApiKey(access_token);
      } catch (error) {
        console.warn('Failed to fetch API key:', error);
      }

      const user: User = {
        id: userData.id,
        name: userData.name,
        email: userData.email,
        apiKeys: {
          ...apiKeys,
          api: apiKeys?.api
        },
        access_token,
        refresh_token,
      };

      setUser(user);
      localStorage.setItem('user', JSON.stringify(user));
      
      // Trigger a page reload to ensure fresh state
      window.location.href = '/workspace';
    } catch (error: any) {
      throw new Error(error.message || 'Login failed');
    }
  };

  const signup = async (name: string, email: string, password: string, apiKeys?: User['apiKeys']) => {
    try {
      await api.users.register({
        name,
        email,
        password,
        api_key: apiKeys?.api
      });

      // After successful registration, login the user
      await login(email, password, apiKeys);
    } catch (error: any) {
      throw new Error(error.message || 'Registration failed');
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};