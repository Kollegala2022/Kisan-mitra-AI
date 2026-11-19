import React, { useState } from 'react';
import './AuthModal.css';
import { authAPI } from '../services/api';
import { KANNADA_DISTRICT_MAP } from './DistrictSelector';

function AuthModal({ isOpen, onClose, onSuccess, language, districts }) {
  const [activeTab, setActiveTab] = useState('login'); // 'login' or 'signup'
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [district, setDistrict] = useState('');
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!isOpen) return null;

  const resetForm = () => {
    setUsername('');
    setPassword('');
    setName('');
    setDistrict('');
    setPhone('');
    setError(null);
  };

  const handleClose = () => {
    resetForm();
    onClose();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

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
      if (activeTab === 'login') {
        const response = await authAPI.login({
          username: username.trim(),
          password: password.trim(),
        });
        resetForm();
        onSuccess(response.user);
        onClose();
      } else {
        const response = await authAPI.signup({
          username: username.trim(),
          password: password.trim(),
          name: name.trim() || username.trim(),
          district: district || null,
          phone: phone.trim() || null,
          language: language,
        });
        resetForm();
        onSuccess(response.user);
        onClose();
      }
    } catch (err) {
      console.error('Authentication error:', err);
      const serverMsg = err.response?.data?.detail;
      if (serverMsg) {
        setError(serverMsg);
      } else {
        setError(
          language === 'kn'
            ? 'ದೃಢೀಕರಣದಲ್ಲಿ ದೋಷ ಉಂಟಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.'
            : 'Authentication error occurred. Please try again.'
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-modal-backdrop" onClick={handleClose}>
      <div className="auth-modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="auth-modal-close" onClick={handleClose} title="Close">
          ✕
        </button>

        <div className="auth-modal-header">
          <div className="auth-modal-icon">🌾</div>
          <h2 className="auth-modal-title">
            {language === 'kn' ? 'ಕಿಸಾನ್‌ಮಿತ್ರ ರೈತ ಖಾತೆ' : 'KisanMitra Farmer Account'}
          </h2>
          <p className="auth-modal-subtitle">
            {language === 'kn'
              ? 'ನಿಮ್ಮ ಹಿಂದಿನ ಸಂಭಾಷಣೆಗಳು ಮತ್ತು ಕೃಷಿ ಸಲಹೆಗಳನ್ನು ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲು ಲಾಗಿನ್ ಮಾಡಿ'
              : 'Save and access your agricultural discussions, crop advice, and history'}
          </p>
        </div>

        {/* Tab switchers */}
        <div className="auth-tab-buttons">
          <button
            type="button"
            className={`auth-tab-btn ${activeTab === 'login' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('login');
              setError(null);
            }}
          >
            {language === 'kn' ? 'ಲಾಗಿನ್ (Login)' : 'Sign In'}
          </button>
          <button
            type="button"
            className={`auth-tab-btn ${activeTab === 'signup' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('signup');
              setError(null);
            }}
          >
            {language === 'kn' ? 'ಹೊಸ ಖಾತೆ ರಚಿಸಿ (Sign Up)' : 'Register Account'}
          </button>
        </div>

        {error && <div className="auth-error-alert">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          {activeTab === 'signup' && (
            <div className="form-group">
              <label htmlFor="auth-name">
                {language === 'kn' ? 'ಪೂರ್ಣ ಹೆಸರು (Full Name)' : 'Full Name'}
              </label>
              <input
                id="auth-name"
                type="text"
                placeholder={language === 'kn' ? 'ಉದಾ: ಬಸವರಾಜ್ / Basavaraj' : 'e.g. Basavaraj'}
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="auth-username">
              {language === 'kn'
                ? 'ಬಳಕೆದಾರ ಹೆಸರು / ಮೊಬೈಲ್ ಸಂಖ್ಯೆ (Username or Mobile)'
                : 'Username or Mobile Number'} *
            </label>
            <input
              id="auth-username"
              type="text"
              required
              placeholder={language === 'kn' ? 'ಉದಾ: farmer99 ಅಥವಾ 9876543210' : 'e.g. farmer99 or 9876543210'}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          {activeTab === 'signup' && (
            <div className="form-group">
              <label htmlFor="auth-district">
                {language === 'kn' ? 'ಜಿಲ್ಲೆ (District)' : 'District'}
              </label>
              <select
                id="auth-district"
                value={district}
                onChange={(e) => setDistrict(e.target.value)}
              >
                <option value="">
                  {language === 'kn' ? '-- ಜಿಲ್ಲೆ ಆರಿಸಿ --' : '-- Select District --'}
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
          )}

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
              <span>⏳ {language === 'kn' ? 'ಪ್ರಕ್ರಿಯೆಯಲ್ಲಿದೆ...' : 'Please wait...'}</span>
            ) : activeTab === 'login' ? (
              <span>🔓 {language === 'kn' ? 'ಲಾಗಿನ್ ಮಾಡಿ' : 'Sign In'}</span>
            ) : (
              <span>✨ {language === 'kn' ? 'ಖಾತೆ ರಚಿಸಿ' : 'Create Account'}</span>
            )}
          </button>
        </form>

        <div className="auth-modal-footer">
          {activeTab === 'login' ? (
            <p>
              {language === 'kn' ? 'ಹೊಸ ಖಾತೆ ಬೇಕೇ?' : "Don't have an account?"}{' '}
              <button
                type="button"
                className="auth-link-btn"
                onClick={() => {
                  setActiveTab('signup');
                  setError(null);
                }}
              >
                {language === 'kn' ? 'ಇಲ್ಲಿ ನೋಂದಾಯಿಸಿ' : 'Sign up now'}
              </button>
            </p>
          ) : (
            <p>
              {language === 'kn' ? 'ಈಗಾಗಲೇ ಖಾತೆ ಇದೆಯೇ?' : 'Already have an account?'}{' '}
              <button
                type="button"
                className="auth-link-btn"
                onClick={() => {
                  setActiveTab('login');
                  setError(null);
                }}
              >
                {language === 'kn' ? 'ಲಾಗಿನ್ ಮಾಡಿ' : 'Sign in'}
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default AuthModal;
