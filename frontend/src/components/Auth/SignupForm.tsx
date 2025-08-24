import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Eye, EyeOff, Loader2 } from 'lucide-react';
import { OtpVerificationDialog } from './OtpVerificationDialog';
import { api } from '../../service/api';

interface SignupFormProps {
  onSwitchToLogin: () => void;
}

export const SignupForm: React.FC<SignupFormProps> = ({ onSwitchToLogin }) => {
  const { signup } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    apiKey: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [isEmailVerified, setIsEmailVerified] = useState(false);
  const [showOtpDialog, setShowOtpDialog] = useState(false);
  const [verifyingName, setVerifyingName] = useState(false);
  const [isNameAvailable, setIsNameAvailable] = useState<boolean | null>(null);

  const checkUsername = async (name: string) => {
    if (!name) return;
    setVerifyingName(true);
    try {
      const { available } = await api.users.checkUsername(name);
      setIsNameAvailable(available);
    } catch (error) {
      console.error('Failed to check username:', error);
      setIsNameAvailable(null);
    } finally {
      setVerifyingName(false);
    }
  };

  const sendVerificationEmail = async () => {
    if (!formData.email) return;
    setIsVerifying(true);
    try {
      await api.users.sendOtp(formData.email);
      setShowOtpDialog(true);
    } catch (error: any) {
      console.error('Failed to send verification email:', error);
      alert(error.message || 'Failed to send verification code');
    } finally {
      setIsVerifying(false);
    }
  };

  const verifyOtp = async (otp: string) => {
    try {
      await api.users.verifyOtp(formData.email, otp);
      setIsEmailVerified(true);
    } catch (error: any) {
      throw new Error(error.message || 'Failed to verify code');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isEmailVerified) {
      alert('Please verify your email first');
      return;
    }
    
    if (!isNameAvailable) {
      alert('Username is not available');
      return;
    }
    
    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    
    setIsLoading(true);
    
    try {
      await signup(formData.name, formData.email, formData.password, {
        api: formData.apiKey
      });
    } catch (error: any) {
      console.error('Signup failed:', error);
      alert(error.message || 'Failed to create account');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white rounded-2xl shadow-xl p-8">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Create Account</h1>
          <p className="text-gray-600 mt-2">Join the AI development revolution</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Full Name
            </label>
            <div className="relative">
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => {
                  const name = e.target.value;
                  setFormData(prev => ({ ...prev, name }));
                  if (name.length > 2) {
                    checkUsername(name);
                  } else {
                    setIsNameAvailable(null);
                  }
                }}
                className={`w-full px-4 py-3 pr-12 border rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 ${
                  isNameAvailable === true ? 'border-green-500' :
                  isNameAvailable === false ? 'border-red-500' :
                  'border-gray-300'
                }`}
                placeholder="Enter your full name"
              />
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                {verifyingName ? (
                  <Loader2 className="w-5 h-5 animate-spin text-gray-400" />
                ) : isNameAvailable === true ? (
                  <div className="text-green-500">✓</div>
                ) : isNameAvailable === false ? (
                  <div className="text-red-500">✗</div>
                ) : null}
              </div>
            </div>
            {isNameAvailable === false && (
              <p className="mt-1 text-sm text-red-500">Username is already taken</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <div className="flex space-x-2">
              <div className="flex-1 relative">
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => {
                    setFormData(prev => ({ ...prev, email: e.target.value }));
                    setIsEmailVerified(false);
                  }}
                  className={`w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 ${
                    isEmailVerified ? 'border-green-500' : 'border-gray-300'
                  }`}
                  placeholder="Enter your email"
                  disabled={isEmailVerified}
                />
                {isEmailVerified && (
                  <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-green-500">
                    ✓
                  </div>
                )}
              </div>
              <button
                type="button"
                onClick={sendVerificationEmail}
                disabled={!formData.email || isVerifying || isEmailVerified}
                className="px-4 py-2 bg-green-500 text-white rounded-xl hover:bg-green-600 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
              >
                {isVerifying ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : isEmailVerified ? (
                  'Verified'
                ) : (
                  'Verify Email'
                )}
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                required
                value={formData.password}
                onChange={(e) => setFormData(prev => ({ ...prev, password: e.target.value }))}
                className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                placeholder="Create a password"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Confirm Password
            </label>
            <div className="relative">
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                required
                value={formData.confirmPassword}
                onChange={(e) => setFormData(prev => ({ ...prev, confirmPassword: e.target.value }))}
                className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                placeholder="Confirm your password"
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
              >
                {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          <div className="space-y-4">
            
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Nvidia API Key</label>
              <input
                type="password"
                value={formData.apiKey}
                onChange={(e) => setFormData(prev => ({ ...prev, apiKey: e.target.value }))}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="Enter API Key..."
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-green-500 to-blue-600 text-white py-3 px-4 rounded-xl font-medium hover:from-green-600 hover:to-blue-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Already have an account?{' '}
            <button
              onClick={onSwitchToLogin}
              className="text-green-600 hover:text-green-700 font-medium transition-colors"
            >
              Sign in
            </button>
          </p>
        </div>
      </div>

      <OtpVerificationDialog
        isOpen={showOtpDialog}
        onClose={() => setShowOtpDialog(false)}
        onVerify={verifyOtp}
        email={formData.email}
      />
    </div>
  );
};