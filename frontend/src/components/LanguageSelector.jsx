import React from 'react';
import './LanguageSelector.css';

function LanguageSelector({ language, onLanguageChange }) {
  return (
    <div className="language-selector">
      <button
        className={`lang-btn ${language === 'en' ? 'active' : ''}`}
        onClick={() => onLanguageChange('en')}
      >
        🇬🇧 English
      </button>
      <button
        className={`lang-btn ${language === 'kn' ? 'active' : ''}`}
        onClick={() => onLanguageChange('kn')}
      >
        🇮🇳 ಕನ್ನಡ
      </button>
    </div>
  );
}

export default LanguageSelector;
