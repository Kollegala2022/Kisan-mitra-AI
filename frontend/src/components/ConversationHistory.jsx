import React from 'react';
import './ConversationHistory.css';

function ConversationHistory({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  currentUser,
  onOpenAuth,
  language,
}) {
  const formatDate = (isoString) => {
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString(language === 'kn' ? 'kn-IN' : 'en-US', {
        month: 'short',
        day: 'numeric',
      });
    } catch {
      return '';
    }
  };

  return (
    <div className="history-container">
      <div className="history-header">
        <h3 className="history-title">
          <span>💬</span> {language === 'kn' ? 'ಹಿಂದಿನ ಸಂಭಾಷಣೆಗಳು' : 'Past Conversations'}
        </h3>
        <button
          className="btn-new-chat-sm"
          onClick={onNewChat}
          title={language === 'kn' ? 'ಹೊಸ ಚಾಟ್ ಆರಂಭಿಸಿ' : 'Start New Chat'}
        >
          ➕ {language === 'kn' ? 'ಹೊಸ ಚಾಟ್' : 'New Chat'}
        </button>
      </div>

      {!currentUser ? (
        <div className="history-guest-card">
          <div className="guest-icon">🔒</div>
          <div className="guest-content">
            <strong>
              {language === 'kn' ? 'ಸಂಭಾಷಣೆಗಳನ್ನು ಉಳಿಸಿಕೊಳ್ಳಿ' : 'Save Your Chats'}
            </strong>
            <p>
              {language === 'kn'
                ? 'ನಿಮ್ಮ ಹಿಂದಿನ ಕೃಷಿ ಸಲಹೆಗಳನ್ನು ನಂತರವೂ ನೋಡಲು ಲಾಗಿನ್ ಮಾಡಿ.'
                : 'Sign in to store and revisit your farming questions anytime.'}
            </p>
            <button className="btn-guest-login" onClick={onOpenAuth}>
              👤 {language === 'kn' ? 'ಲಾಗಿನ್ / ಖಾತೆ ರಚಿಸಿ' : 'Sign In / Register'}
            </button>
          </div>
        </div>
      ) : conversations.length === 0 ? (
        <div className="history-empty">
          <p>
            {language === 'kn'
              ? 'ಇನ್ನೂ ಯಾವುದೇ ಹಿಂದಿನ ಚಾಟ್‌ಗಳಿಲ್ಲ. ಕೃಷಿ ಪ್ರಶ್ನೆ ಕೇಳಿ ಆರಂಭಿಸಿ!'
              : 'No past chats yet. Ask an agricultural question to begin!'}
          </p>
        </div>
      ) : (
        <div className="history-list">
          {conversations.map((conv) => {
            const isActive = conv.id === currentConversationId;
            return (
              <div
                key={conv.id}
                className={`history-item ${isActive ? 'active' : ''}`}
                onClick={() => onSelectConversation(conv.id)}
              >
                <div className="history-item-body">
                  <div className="history-item-title" title={conv.title}>
                    {conv.title || (language === 'kn' ? 'ಕೃಷಿ ಚರ್ಚೆ' : 'Agri Chat')}
                  </div>
                  <div className="history-item-meta">
                    <span className="history-item-date">{formatDate(conv.created_at)}</span>
                    {conv.message_count > 0 && (
                      <span className="history-item-count">
                        {conv.message_count} {language === 'kn' ? 'ಸಂದೇಶ' : 'msgs'}
                      </span>
                    )}
                  </div>
                </div>
                <button
                  className="history-item-delete"
                  title={language === 'kn' ? 'ಚಾಟ್ ಅಳಿಸಿ' : 'Delete conversation'}
                  onClick={(e) => {
                    e.stopPropagation();
                    if (
                      window.confirm(
                        language === 'kn'
                          ? 'ಈ ಸಂಭಾಷಣೆಯನ್ನು ಅಳಿಸಲು ನೀವು ಖಚಿತವಾಗಿದ್ದೀರಾ?'
                          : 'Are you sure you want to delete this conversation?'
                      )
                    ) {
                      onDeleteConversation(conv.id);
                    }
                  }}
                >
                  🗑️
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default ConversationHistory;
