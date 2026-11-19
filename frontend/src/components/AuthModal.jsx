import React, { useState } from 'react';
import './AuthModal.css';
import { authAPI } from '../services/api';
import { KANNADA_DISTRICT_MAP } from './DistrictSelector';

function AuthModal({
  isOpen,
  onClose,
  onSuccess,
  language,
  districts,
  initialTab = 'signup',
  mandatory = false,
  onLanguageChange
}) {
  // Modes: 'signup' | 'login' | 'forgot' | 'verify_otp' | 'reset_password'
  const [mode, setMode] = useState(initialTab);
  
  // Registration & Login fields
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [district, setDistrict] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  
  // Forgot Password / OTP fields
  const [forgotChannel, setForgotChannel] = useState('mobile'); // 'mobile' | 'email'
  const [forgotIdentifier, setForgotIdentifier] = useState('');
  const [otpCode, setOtpCode] = useState('');
  const [resetToken, setResetToken] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  // Status states
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [demoOtpNotice, setDemoOtpNotice] = useState(null);

  if (!isOpen) return null;

  const resetAllFields = () => {
    setUsername('');
    setPassword('');
    setName('');
    setDistrict('');
    setPhone('');
    setEmail('');
    setForgotIdentifier('');
    setOtpCode('');
    setResetToken('');
    setNewPassword('');
    setConfirmPassword('');
    setError(null);
    setSuccessMessage(null);
    setDemoOtpNotice(null);
  };

  const handleClose = () => {
    if (mandatory) return; // Cannot close if initial auth is mandatory
    resetAllFields();
    onClose();
  };

  // 1. Submit Registration or Login
  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (mode === 'signup') {
      if (!username.trim() || !password.trim()) {
        setError(
          language === 'kn'
            ? 'ದಯವಿಟ್ಟು ಬಳಕೆದಾರ ಹೆಸರು ಮತ್ತು ಪಾಸ್‌ವರ್ಡ್ ನಮೂದಿಸಿ'
            : 'Please enter username and password'
        );
        return;
      }

      setLoading(true);
      try {
        const response = await authAPI.signup({
          username: username.trim(),
          password: password.trim(),
          name: name.trim() || username.trim(),
          phone: phone.trim() || null,
          email: email.trim() || null,
          district: district || null,
          language: language,
        });
        resetAllFields();
        onSuccess(response.user);
        if (!mandatory) onClose();
      } catch (err) {
        console.error('Signup error:', err);
        setError(
          err.response?.data?.detail ||
          (language === 'kn'
            ? 'ಖಾತೆ ರಚಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.'
            : 'Failed to create account. Please check details.')
        );
      } finally {
        setLoading(false);
      }
    } else if (mode === 'login') {
      if (!username.trim() || !password.trim()) {
        setError(
          language === 'kn'
            ? 'ದಯವಿಟ್ಟು ಬಳಕೆದಾರ ಹೆಸರು/ಮೊಬೈಲ್ ಮತ್ತು ಪಾಸ್‌ವರ್ಡ್ ನಮೂದಿಸಿ'
            : 'Please enter username/mobile and password'
        );
        return;
      }

      setLoading(true);
      try {
        const response = await authAPI.login({
          username: username.trim(),
          password: password.trim(),
        });
        resetAllFields();
        onSuccess(response.user);
        if (!mandatory) onClose();
      } catch (err) {
        console.error('Login error:', err);
        setError(
          err.response?.data?.detail ||
          (language === 'kn'
            ? 'ತಪ್ಪು ಬಳಕೆದಾರ ಹೆಸರು ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್. ದಯವಿಟ್ಟು ಪರಿಶೀಲಿಸಿ.'
            : 'Invalid username/mobile or password.')
        );
      } finally {
        setLoading(false);
      }
    }
  };

  // 2. Request OTP / Reset code
  const handleRequestOtp = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);
    setDemoOtpNotice(null);

    if (!forgotIdentifier.trim()) {
      setError(
        language === 'kn'
          ? forgotChannel === 'mobile'
            ? 'ದಯವಿಟ್ಟು ನಿಮ್ಮ ನೋಂದಾಯಿತ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ'
            : 'ದಯವಿಟ್ಟು ನಿಮ್ಮ ನೋಂದಾಯಿತ ಇಮೇಲ್ ನಮೂದಿಸಿ'
          : forgotChannel === 'mobile'
          ? 'Please enter your registered mobile number'
          : 'Please enter your registered email'
      );
      return;
    }

    setLoading(true);
    try {
      const res = await authAPI.forgotPassword(forgotChannel, forgotIdentifier.trim());
      setSuccessMessage(
        language === 'kn'
          ? forgotChannel === 'mobile'
            ? `ನಿಮ್ಮ ಮೊಬೈಲ್‌ಗೆ OTP ಕಳುಹಿಸಲಾಗಿದೆ: ${forgotIdentifier}`
            : `ನಿಮ್ಮ ಇಮೇಲ್‌ಗೆ ರಿಸೆಟ್ ಕೋಡ್ ಕಳುಹಿಸಲಾಗಿದೆ: ${forgotIdentifier}`
          : res.message
      );
      
      // If server returned demo OTP for instant visual confirmation
      if (res.otp_code) {
        setDemoOtpNotice(res.otp_code);
        setOtpCode(res.otp_code); // Pre-fill for quick test convenience
      }
      
      setMode('verify_otp');
    } catch (err) {
      console.error('Forgot password error:', err);
      setError(
        err.response?.data?.detail ||
        (language === 'kn'
          ? 'ಖಾತೆ ಹುಡುಕಲು ವಿಫಲವಾಗಿದೆ. ದಯವಿಟ್ಟು ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ಅಥವಾ ಇಮೇಲ್ ಪರಿಶೀಲಿಸಿ.'
          : 'Account not found. Please verify mobile or email.')
      );
    } finally {
      setLoading(false);
    }
  };

  // 3. Verify OTP Code
  const handleVerifyOtp = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (!otpCode.trim() || otpCode.trim().length < 4) {
      setError(
        language === 'kn'
          ? 'ದಯವಿಟ್ಟು 6-ಅಂಕಿಯ ಸರಿಯಾದ OTP ನಮೂದಿಸಿ'
          : 'Please enter valid 6-digit OTP'
      );
      return;
    }

    setLoading(true);
    try {
      const res = await authAPI.verifyOtp(forgotIdentifier.trim(), otpCode.trim());
      setResetToken(res.reset_token);
      setSuccessMessage(
        language === 'kn'
          ? 'OTP ಯಶಸ್ವಿಯಾಗಿ ದೃಢೀಕರಿಸಲಾಗಿದೆ. ಹೊಸ ಗುಪ್ತಪದ ರಚಿಸಿ.'
          : 'OTP verified successfully. Create your new password.'
      );
      setDemoOtpNotice(null);
      setMode('reset_password');
    } catch (err) {
      console.error('Verify OTP error:', err);
      setError(
        err.response?.data?.detail ||
        (language === 'kn'
          ? 'ತಪ್ಪು ಅಥವಾ ಮುಕ್ತಾಯಗೊಂಡ OTP. ದಯವಿಟ್ಟು ಪರಿಶೀಲಿಸಿ.'
          : 'Invalid or expired OTP.')
      );
    } finally {
      setLoading(false);
    }
  };

  // 4. Set New Password
  const handleResetPassword = async (e) => {
    e.preventDefault();
    setError(null);

    if (!newPassword.trim() || newPassword.length < 4) {
      setError(
        language === 'kn'
          ? 'ಗುಪ್ತಪದ ಕನಿಷ್ಠ 4 ಅಕ್ಷರಗಳಾಗಿರಬೇಕು'
          : 'Password must be at least 4 characters'
      );
      return;
    }

    if (newPassword !== confirmPassword) {
      setError(
        language === 'kn'
          ? 'ಗುಪ್ತಪದಗಳು ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ'
          : 'Passwords do not match'
      );
      return;
    }

    setLoading(true);
    try {
      await authAPI.resetPassword(resetToken, newPassword.trim());
      setSuccessMessage(
        language === 'kn'
          ? 'ನಿಮ್ಮ ಗುಪ್ತಪದವನ್ನು ಯಶಸ್ವಿಯಾಗಿ ನವೀಕರಿಸಲಾಗಿದೆ! ಈಗ ಲಾಗಿನ್ ಮಾಡಿ.'
          : 'Password updated successfully! Please login with your new password.'
      );
      // Switch back to login
      setMode('login');
      setUsername(forgotIdentifier);
      setPassword('');
    } catch (err) {
      console.error('Reset password error:', err);
      setError(
        err.response?.data?.detail ||
        (language === 'kn'
          ? 'ಗುಪ್ತಪದ ನವೀಕರಿಸಲು ವಿಫಲವಾಗಿದೆ. ದಯವಿಟ್ಟು ಹೊಸ OTP ಪಡೆದುಕೊಳ್ಳಿ.'
          : 'Failed to reset password. Please request a new OTP.')
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`auth-modal-backdrop ${mandatory ? 'mandatory-backdrop' : ''}`} onClick={handleClose}>
      <div className="auth-modal-content" onClick={(e) => e.stopPropagation()}>
        {!mandatory && (
          <button className="auth-modal-close" onClick={handleClose} title="Close">
            ✕
          </button>
        )}

        {/* Language switch header */}
        {onLanguageChange && (
          <div className="auth-modal-lang-toggle">
            <span className="auth-lang-label">
              {language === 'kn' ? 'ಭಾಷೆ / Language:' : 'Language:'}
            </span>
            <button
              type="button"
              className={`btn-lang-pill ${language === 'en' ? 'active' : ''}`}
              onClick={() => onLanguageChange('en')}
            >
              English
            </button>
            <button
              type="button"
              className={`btn-lang-pill ${language === 'kn' ? 'active' : ''}`}
              onClick={() => onLanguageChange('kn')}
            >
              ಕನ್ನಡ
            </button>
          </div>
        )}

        <div className="auth-modal-header">
          <div className="auth-modal-icon">🌾</div>
          <h2 className="auth-modal-title">
            {mode === 'signup'
              ? language === 'kn' ? 'ಕಿಸಾನ್‌ಮಿತ್ರಕ್ಕೆ ಸ್ವಾಗತ • ಹೊಸ ಖಾತೆ' : 'Welcome to KisanMitra • Register'
              : mode === 'login'
              ? language === 'kn' ? 'ಕಿಸಾನ್‌ಮಿತ್ರ ರೈತ ಲಾಗಿನ್' : 'Farmer Login'
              : mode === 'forgot'
              ? language === 'kn' ? 'ಗುಪ್ತಪದ ಮರುಹೊಂದಿಸಿ (OTP)' : 'Reset Password (OTP)'
              : mode === 'verify_otp'
              ? language === 'kn' ? 'OTP ಪರಿಶೀಲಿಸಿ' : 'Verify 6-Digit OTP'
              : language === 'kn' ? 'ಹೊಸ ಗುಪ್ತಪದ ರಚಿಸಿ' : 'Create New Password'}
          </h2>
          <p className="auth-modal-subtitle">
            {mode === 'signup'
              ? language === 'kn'
                ? 'ಕರ್ನಾಟಕದ ರೈತರಿಗೆ ಮೀಸಲಾದ AI ಕೃಷಿ ಸಲಹೆಗಾರ. ಮುಂದುವರಿಯಲು ಖಾತೆ ರಚಿಸಿ.'
                : 'AI-powered farming advisory for Karnataka. Create an account to begin.'
              : mode === 'login'
              ? language === 'kn'
                ? 'ನಿಮ್ಮ ಕೃಷಿ ಪ್ರಶ್ನೆಗಳು, ಹವಾಮಾನ ಮತ್ತು ಹಿಂದಿನ ಸಂಭಾಷಣೆಗಳನ್ನು ಪ್ರವೇಶಿಸಲು ಲಾಗಿನ್ ಮಾಡಿ.'
                : 'Sign in to access your crop advisory, weather, and conversation history.'
              : mode === 'forgot'
              ? language === 'kn'
                ? 'ನಿಮ್ಮ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ OTP ಮೂಲಕ ಗುಪ್ತಪದ ಮರುಹೊಂದಿಸಿ.'
                : 'Enter your mobile number or email to receive a password reset OTP.'
              : mode === 'verify_otp'
              ? language === 'kn'
                ? 'ನಿಮ್ಮ ಮೊಬೈಲ್‌ಗೆ ಕಳುಹಿಸಲಾದ 6-ಅಂಕಿಯ OTP ಕೋಡ್ ನಮೂದಿಸಿ.'
                : 'Enter the 6-digit verification code sent to your device.'
              : language === 'kn'
              ? 'ನಿಮ್ಮ ಖಾತೆಗೆ ಸುರಕ್ಷಿತ ಹೊಸ ಗುಪ್ತಪದ ನಮೂದಿಸಿ.'
              : 'Enter a secure new password for your account.'}
          </p>
        </div>

        {/* Tab switcher for Sign Up & Login */}
        {(mode === 'signup' || mode === 'login') && (
          <div className="auth-tab-buttons">
            <button
              type="button"
              className={`auth-tab-btn ${mode === 'signup' ? 'active' : ''}`}
              onClick={() => {
                setMode('signup');
                setError(null);
                setSuccessMessage(null);
              }}
            >
              {language === 'kn' ? 'ಖಾತೆ ರಚಿಸಿ (Sign Up)' : 'Sign Up'}
            </button>
            <button
              type="button"
              className={`auth-tab-btn ${mode === 'login' ? 'active' : ''}`}
              onClick={() => {
                setMode('login');
                setError(null);
                setSuccessMessage(null);
              }}
            >
              {language === 'kn' ? 'ಲಾಗಿನ್ (Login)' : 'Sign In'}
            </button>
          </div>
        )}

        {/* Alerts */}
        {error && <div className="auth-error-alert">{error}</div>}
        {successMessage && <div className="auth-success-alert">{successMessage}</div>}
        {demoOtpNotice && (
          <div className="auth-otp-badge-notice">
            <span>📲 {language === 'kn' ? 'ಪರೀಕ್ಷಾರ್ಥ OTP ಕೋಡ್:' : 'Verification OTP Code:'}</span>{' '}
            <strong>{demoOtpNotice}</strong>
          </div>
        )}

        {/* ================= MODE 1: SIGN UP ================= */}
        {mode === 'signup' && (
          <form onSubmit={handleAuthSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="auth-name">
                {language === 'kn' ? 'ಪೂರ್ಣ ಹೆಸರು (Full Name)' : 'Full Name'} *
              </label>
              <input
                id="auth-name"
                type="text"
                required
                placeholder={language === 'kn' ? 'ಉದಾ: ಬಸವರಾಜ / Basavaraj' : 'e.g. Basavaraj'}
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="form-row-2">
              <div className="form-group">
                <label htmlFor="auth-username">
                  {language === 'kn' ? 'ಬಳಕೆದಾರ ಹೆಸರು (Username)' : 'Username'} *
                </label>
                <input
                  id="auth-username"
                  type="text"
                  required
                  placeholder={language === 'kn' ? 'ಉದಾ: farmer_raju' : 'e.g. farmer_raju'}
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label htmlFor="auth-phone">
                  {language === 'kn' ? 'ಮೊಬೈಲ್ ಸಂಖ್ಯೆ (Mobile)' : 'Mobile Number'} *
                </label>
                <input
                  id="auth-phone"
                  type="tel"
                  required
                  placeholder="9876543210"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="auth-email">
                {language === 'kn' ? 'ಇಮೇಲ್ ವಿಳಾಸ (Email - ಐಚ್ಛಿಕ)' : 'Email Address (Optional)'}
              </label>
              <input
                id="auth-email"
                type="email"
                placeholder="farmer@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label htmlFor="auth-district">
                {language === 'kn' ? 'ನಿಮ್ಮ ಜಿಲ್ಲೆ (District)' : 'District'} *
              </label>
              <select
                id="auth-district"
                required
                value={district}
                onChange={(e) => setDistrict(e.target.value)}
              >
                <option value="">
                  {language === 'kn' ? '-- ಕರ್ನಾಟಕದ ಜಿಲ್ಲೆ ಆರಿಸಿ --' : '-- Select District --'}
                </option>
                {districts &&
                  districts.map((d) => {
                    const dName = typeof d === 'string' ? d : d.name;
                    const knName = typeof d === 'object' && d.kannada ? d.kannada : (KANNADA_DISTRICT_MAP[dName] || dName);
                    const label = language === 'kn' ? `${knName} (${dName})` : dName;
                    return (
                      <option key={dName} value={dName}>
                        📍 {label}
                      </option>
                    );
                  })}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="auth-password">
                {language === 'kn' ? 'ಗುಪ್ತಪದ (Password)' : 'Password'} *
              </label>
              <input
                id="auth-password"
                type="password"
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <button type="submit" className="auth-submit-btn" disabled={loading}>
              {loading ? (
                <span>⏳ {language === 'kn' ? 'ಖಾತೆ ರಚಿಸಲಾಗುತ್ತಿದೆ...' : 'Creating account...'}</span>
              ) : (
                <span>✨ {language === 'kn' ? 'ಖಾತೆ ರಚಿಸಿ ಪ್ರಾರಂಭಿಸಿ' : 'Create Account & Enter'}</span>
              )}
            </button>
          </form>
        )}

        {/* ================= MODE 2: LOGIN ================= */}
        {mode === 'login' && (
          <form onSubmit={handleAuthSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="login-username">
                {language === 'kn'
                  ? 'ಬಳಕೆದಾರ ಹೆಸರು / ಮೊಬೈಲ್ ಸಂಖ್ಯೆ / ಇಮೇಲ್'
                  : 'Username, Mobile Number, or Email'} *
              </label>
              <input
                id="login-username"
                type="text"
                required
                placeholder={language === 'kn' ? 'ಬಳಕೆದಾರ ಹೆಸರು ಅಥವಾ 10-ಅಂಕಿಯ ಮೊಬೈಲ್' : 'Enter username, phone, or email'}
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>

            <div className="form-group">
              <div className="label-with-action">
                <label htmlFor="login-password">
                  {language === 'kn' ? 'ಗುಪ್ತಪದ (Password)' : 'Password'} *
                </label>
                <button
                  type="button"
                  className="auth-inline-link"
                  onClick={() => {
                    setMode('forgot');
                    setError(null);
                    setSuccessMessage(null);
                    setForgotIdentifier(username);
                  }}
                >
                  🔑 {language === 'kn' ? 'ಗುಪ್ತಪದ ಮರೆತಿರಾ?' : 'Forgot Password?'}
                </button>
              </div>
              <input
                id="login-password"
                type="password"
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <button type="submit" className="auth-submit-btn" disabled={loading}>
              {loading ? (
                <span>⏳ {language === 'kn' ? 'ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...' : 'Signing in...'}</span>
              ) : (
                <span>🔓 {language === 'kn' ? 'ಲಾಗಿನ್ ಮಾಡಿ' : 'Sign In'}</span>
              )}
            </button>
          </form>
        )}

        {/* ================= MODE 3: FORGOT PASSWORD (REQUEST OTP) ================= */}
        {mode === 'forgot' && (
          <form onSubmit={handleRequestOtp} className="auth-form">
            <div className="auth-channel-selector">
              <button
                type="button"
                className={`channel-btn ${forgotChannel === 'mobile' ? 'active' : ''}`}
                onClick={() => setForgotChannel('mobile')}
              >
                📱 {language === 'kn' ? 'ಮೊಬೈಲ್ OTP' : 'Mobile OTP'}
              </button>
              <button
                type="button"
                className={`channel-btn ${forgotChannel === 'email' ? 'active' : ''}`}
                onClick={() => setForgotChannel('email')}
              >
                ✉️ {language === 'kn' ? 'ಇಮೇಲ್ ಲಿಂಕ್' : 'Email Link'}
              </button>
            </div>

            <div className="form-group">
              <label htmlFor="forgot-identifier">
                {forgotChannel === 'mobile'
                  ? language === 'kn' ? 'ನೋಂದಾಯಿತ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ (Registered Mobile)' : 'Registered Mobile Number'
                  : language === 'kn' ? 'ನೋಂದಾಯಿತ ಇಮೇಲ್ ವಿಳಾಸ (Registered Email)' : 'Registered Email Address'} *
              </label>
              <input
                id="forgot-identifier"
                type={forgotChannel === 'mobile' ? 'tel' : 'email'}
                required
                placeholder={forgotChannel === 'mobile' ? '9876543210' : 'farmer@example.com'}
                value={forgotIdentifier}
                onChange={(e) => setForgotIdentifier(e.target.value)}
              />
            </div>

            <button type="submit" className="auth-submit-btn" disabled={loading}>
              {loading ? (
                <span>⏳ {language === 'kn' ? 'OTP ಕಳುಹಿಸಲಾಗುತ್ತಿದೆ...' : 'Sending OTP...'}</span>
              ) : (
                <span>📲 {language === 'kn' ? 'OTP ಕೋಡ್ ಕಳುಹಿಸಿ' : 'Send Verification OTP'}</span>
              )}
            </button>

            <button
              type="button"
              className="auth-secondary-btn"
              onClick={() => {
                setMode('login');
                setError(null);
                setSuccessMessage(null);
              }}
            >
              ⬅️ {language === 'kn' ? 'ಲಾಗಿನ್‌ಗೆ ಹಿಂತಿರುಗಿ' : 'Back to Login'}
            </button>
          </form>
        )}

        {/* ================= MODE 4: VERIFY OTP ================= */}
        {mode === 'verify_otp' && (
          <form onSubmit={handleVerifyOtp} className="auth-form">
            <div className="form-group">
              <label htmlFor="otp-input">
                {language === 'kn' ? '6-ಅಂಕಿಯ OTP ಕೋಡ್ (6-Digit OTP Code)' : '6-Digit OTP Code'} *
              </label>
              <input
                id="otp-input"
                type="text"
                required
                maxLength={6}
                placeholder="123456"
                className="otp-number-input"
                value={otpCode}
                onChange={(e) => setOtpCode(e.target.value)}
              />
            </div>

            <button type="submit" className="auth-submit-btn" disabled={loading}>
              {loading ? (
                <span>⏳ {language === 'kn' ? 'ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...' : 'Verifying...'}</span>
              ) : (
                <span>✅ {language === 'kn' ? 'OTP ದೃಢೀಕರಿಸಿ' : 'Verify OTP'}</span>
              )}
            </button>

            <div className="auth-sub-actions">
              <button
                type="button"
                className="auth-link-btn"
                onClick={handleRequestOtp}
                disabled={loading}
              >
                🔄 {language === 'kn' ? 'ಮತ್ತೆ OTP ಕಳುಹಿಸಿ' : 'Resend OTP'}
              </button>
              <button
                type="button"
                className="auth-link-btn"
                onClick={() => {
                  setMode('forgot');
                  setError(null);
                }}
              >
                ✏️ {language === 'kn' ? 'ಸಂಖ್ಯೆ ಬದಲಿಸಿ' : 'Change Number'}
              </button>
            </div>
          </form>
        )}

        {/* ================= MODE 5: SET NEW PASSWORD ================= */}
        {mode === 'reset_password' && (
          <form onSubmit={handleResetPassword} className="auth-form">
            <div className="form-group">
              <label htmlFor="reset-new-password">
                {language === 'kn' ? 'ಹೊಸ ಗುಪ್ತಪದ (New Password)' : 'New Password'} *
              </label>
              <input
                id="reset-new-password"
                type="password"
                required
                placeholder="••••••••"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label htmlFor="reset-confirm-password">
                {language === 'kn' ? 'ಗುಪ್ತಪದ ಖಚಿತಪಡಿಸಿ (Confirm Password)' : 'Confirm Password'} *
              </label>
              <input
                id="reset-confirm-password"
                type="password"
                required
                placeholder="••••••••"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>

            <button type="submit" className="auth-submit-btn" disabled={loading}>
              {loading ? (
                <span>⏳ {language === 'kn' ? 'ನವೀಕರಿಸಲಾಗುತ್ತಿದೆ...' : 'Updating password...'}</span>
              ) : (
                <span>🔒 {language === 'kn' ? 'ಹೊಸ ಗುಪ್ತಪದ ಉಳಿಸಿ' : 'Save New Password'}</span>
              )}
            </button>
          </form>
        )}

        {/* Footer switchers */}
        <div className="auth-modal-footer">
          {mode === 'signup' && (
            <p>
              {language === 'kn' ? 'ಈಗಾಗಲೇ ಖಾತೆ ಹೊಂದಿದ್ದೀರಾ?' : 'Already have an account?'}{' '}
              <button
                type="button"
                className="auth-link-btn"
                onClick={() => {
                  setMode('login');
                  setError(null);
                  setSuccessMessage(null);
                }}
              >
                {language === 'kn' ? 'ಇಲ್ಲಿ ಲಾಗಿನ್ ಮಾಡಿ' : 'Sign in here'}
              </button>
            </p>
          )}

          {mode === 'login' && (
            <p>
              {language === 'kn' ? 'ಹೊಸ ರೈತರೇ?' : 'New to KisanMitra?'}{' '}
              <button
                type="button"
                className="auth-link-btn"
                onClick={() => {
                  setMode('signup');
                  setError(null);
                  setSuccessMessage(null);
                }}
              >
                {language === 'kn' ? 'ಹೊಸ ಖಾತೆ ರಚಿಸಿ' : 'Create an account'}
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default AuthModal;
