import React, { useState, useEffect, useRef } from 'react';
import './ChatWindow.css';
import Message from './Message';
import HomeHero from './HomeHero';

function ChatWindow({
  messages,
  isLoading,
  onSendMessage,
  language,
  district,
  crop,
  weatherData,
  error
}) {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendClick = () => {
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
      e.preventDefault();
      handleSendClick();
    }
  };

  const quickChips = [
    {
      label: language === 'en' ? '🌾 Paddy Guide' : '🌾 ಭತ್ತದ ಬೆಳೆ',
      prompt: language === 'en' ? 'What are the best practices for paddy cultivation in Karnataka?' : 'ಕರ್ನಾಟಕದಲ್ಲಿ ಭತ್ತ ಬೆಳೆಯಲು ಉತ್ತಮ ವಿಧಾನಗಳು ಯಾವುವು?'
    },
    {
      label: language === 'en' ? '🌱 Ragi Sowing' : '🌱 ರಾಗಿ ಬಿತ್ತನೆ',
      prompt: language === 'en' ? 'What is the recommended sowing time, seed rate, and fertilizer for Ragi?' : 'ರಾಗಿಗೆ ಶಿಫಾರಸು ಮಾಡಲಾದ ಬಿತ್ತನೆ ಸಮಯ, ಬೀಜದ ಪ್ರಮಾಣ ಮತ್ತು ಗೊಬ್ಬರ ಯಾವುದು?'
    },
    {
      label: language === 'en' ? '🐛 Pest Remedies' : '🐛 ಕೀಟ ನಿಯಂತ್ರಣ',
      prompt: language === 'en' ? 'How to identify and control stem borer and blast disease?' : 'ಕಾಂಡ ಕೊರೆಯುವ ಹುಳು ಮತ್ತು ಬ್ಲಾಸ್ಟ್ ರೋಗವನ್ನು ಗುರುತಿಸಿ ನಿಯಂತ್ರಿಸುವುದು ಹೇಗೆ?'
    },
    {
      label: language === 'en' ? '💧 Drip Irrigation' : '💧 ಹನಿ ನೀರಾವರಿ',
      prompt: language === 'en' ? 'How to set up efficient drip irrigation for horticulture crops?' : 'ತೋಟಗಾರಿಕೆ ಬೆಳೆಗಳಿಗೆ ಪರಿಣಾಮಕಾರಿ ಹನಿ ನೀರಾವರಿ ಮಾಡುವುದು ಹೇಗೆ?'
    },
    {
      label: language === 'en' ? '🏛️ Raitha Siri / Schemes' : '🏛️ ರೈತ ಸಿರಿ / ಯೋಜನೆ',
      prompt: language === 'en' ? 'What subsidies are available under Raitha Siri and PM-Kisan scheme in Karnataka?' : 'ಕರ್ನಾಟಕದಲ್ಲಿ ರೈತ ಸಿರಿ ಮತ್ತು ಪಿಎಂ-ಕಿಸಾನ್ ಯೋಜನೆಯಡಿ ಯಾವ ಸಬ್ಸಿಡಿ ಲಭ್ಯವಿದೆ?'
    }
  ];

  return (
    <div className="chat-window">
      <div className="messages-container">
        {messages.length === 0 ? (
          <HomeHero
            language={language}
            district={district}
            crop={crop}
            weatherData={weatherData}
            onActionClick={onSendMessage}
          />
        ) : (
          <div className="messages-stream">
            {messages.map((msg) => (
              <Message key={msg.id} message={msg} language={language} />
            ))}
            {isLoading && (
              <div className="message-row assistant-row">
                <div className="message-avatar">🌾</div>
                <div className="message-bubble assistant-bubble loading-bubble">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <span className="loading-text">
                    {language === 'en' ? 'KisanMitra is analyzing agricultural data...' : 'ಕಿಸನ್‌ಮಿತ್ರ ಕೃಷಿ ಮಾಹಿತಿ ಪರಿಶೀಲಿಸುತ್ತಿದೆ...'}
                  </span>
                </div>
              </div>
            )}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && <div className="error-message">⚠️ {error}</div>}

      {/* Quick Prompts Bar (when chatting) */}
      {messages.length > 0 && (
        <div className="quick-chips-bar">
          <span className="chips-label">💡 {language === 'en' ? 'Suggestions:' : 'ಸಲಹೆಗಳು:'}</span>
          <div className="chips-scroll">
            {quickChips.map((chip, idx) => (
              <button
                key={idx}
                className="chip-btn"
                onClick={() => onSendMessage(chip.prompt)}
                disabled={isLoading}
              >
                {chip.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Message Input Bar */}
      <div className="message-input-wrapper">
        <div className="input-box-container">
          <textarea
            className="message-input"
            placeholder={
              language === 'en'
                ? `Ask anything about ${crop || 'crops'}, ${district || 'weather'}, pests, soil, or schemes...`
                : `${crop || 'ಬೆಳೆಗಳು'}, ${district || 'ಹವಾಮಾನ'}, ಕೀಟ, ಮಣ್ಣು ಅಥವಾ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ಕೇಳಿ...`
            }
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            rows={1}
          />
          <button
            className="btn btn-send"
            onClick={handleSendClick}
            disabled={isLoading || !inputValue.trim()}
            title={language === 'en' ? 'Send Question' : 'ಪ್ರಶ್ನೆ ಕಳುಹಿಸಿ'}
          >
            {isLoading ? (
              <span className="spinner-dot"></span>
            ) : (
              <span className="send-icon">➔</span>
            )}
          </button>
        </div>
        <div className="input-hint">
          <span>
            {language === 'en'
              ? '🌿 AI guidance based on verified Karnataka Agriculture Department publications'
              : '🌿 ಕರ್ನಾಟಕ ಕೃಷಿ ಇಲಾಖೆಯ ಅಧಿಕೃತ ಮಾಹಿತಿಯ ಆಧಾರದ ಮೇಲೆ AI ಸಲಹೆ'}
          </span>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;
