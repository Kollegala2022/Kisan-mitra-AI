import React from 'react';
import ReactMarkdown from 'react-markdown';
import './Message.css';

function Message({ message, language }) {
  const isUser = message.role === 'user';

  const renderSources = (sourcesJson) => {
    try {
      if (!sourcesJson) return null;

      let sources = [];
      if (typeof sourcesJson === 'string') {
        sources = JSON.parse(sourcesJson);
      } else {
        sources = sourcesJson;
      }

      if (!Array.isArray(sources) || sources.length === 0) return null;

      return (
        <div className="message-sources">
          <div className="sources-header">
            <span className="sources-icon">📚</span>
            <span>{language === 'en' ? 'Verified Agricultural Sources:' : 'ಪರಿಶೀಲಿಸಿದ ಕೃಷಿ ಮೂಲಗಳು:'}</span>
          </div>
          <div className="sources-list">
            {sources.map((source, idx) => (
              <div key={idx} className="source-card">
                <div className="source-meta-row">
                  <span className="source-title">{source.title || 'Agricultural Reference Guide'}</span>
                  {source.relevance && (
                    <span className="source-relevance">{source.relevance} match</span>
                  )}
                </div>
                {source.url && (
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="source-link"
                  >
                    🔗 {source.url}
                  </a>
                )}
                {source.reviewed_date && (
                  <div className="source-date">
                    📅 {language === 'en' ? 'Reviewed:' : 'ಪರಿಶೀಲಿಸಲಾಯಿತು:'} {source.reviewed_date}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      );
    } catch (e) {
      return null;
    }
  };

  return (
    <div className={`message-row ${isUser ? 'user-row' : 'assistant-row'}`}>
      <div className="message-avatar">
        {isUser ? '👨‍🌾' : '🌾'}
      </div>

      <div className={`message-bubble ${isUser ? 'user-bubble' : 'assistant-bubble'}`}>
        <div className="message-author">
          {isUser
            ? (language === 'en' ? 'You' : 'ನೀವು')
            : (language === 'en' ? 'KisanMitra AI' : 'ಕಿಸನ್‌ಮಿತ್ರ AI')}
        </div>

        <div className="message-text markdown-body">
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown>{message.content}</ReactMarkdown>
          )}
        </div>

        {!isUser && message.sources && renderSources(message.sources)}

        {!isUser && message.needs_expert && (
          <div className="expert-tip-banner">
            <div className="tip-header">
              <span className="tip-icon">💡</span>
              <strong>{language === 'en' ? 'Expert Consultation Recommended:' : 'ಪರಿಣತರ ಸಲಹೆ ಸೂಚನೆ:'}</strong>
            </div>
            <p className="tip-text">
              {language === 'en'
                ? 'For severe crop disease, pest outbreaks, or high-value chemical dosing, please consult your local Raitha Samparka Kendra (RSK) or an agriculture university extension expert.'
                : 'ತೀವ್ರ ಬೆಳೆ ರೋಗ, ಕೀಟ ಬಾಧೆ ಅಥವಾ ಔಷಧಿ ಡೋಸೇಜ್‌ಗಾಗಿ, ದಯವಿಟ್ಟು ನಿಮ್ಮ ಹತ್ತಿರದ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರ (RSK) ಅಥವಾ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರವನ್ನು ಸಂಪರ್ಕಿಸಿ.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Message;
