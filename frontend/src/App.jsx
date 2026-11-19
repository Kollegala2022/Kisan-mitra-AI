import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import ChatWindow from './components/ChatWindow';
import LanguageSelector from './components/LanguageSelector';
import DistrictSelector, { KANNADA_DISTRICT_MAP } from './components/DistrictSelector';
import CropSelector from './components/CropSelector';
import QuickActions from './components/QuickActions';
import AuthModal from './components/AuthModal';
import ConversationHistory from './components/ConversationHistory';
import { chatAPI, authAPI, getToken } from './services/api';

function App() {
  const [language, setLanguage] = useState('kn'); // Default to Kannada as requested by user
  const [district, setDistrict] = useState(null);
  const [crop, setCrop] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [districts, setDistricts] = useState([]);
  const [crops, setCrops] = useState([]);
  const [weatherData, setWeatherData] = useState(null);

  // Authentication & Conversation History states
  const [currentUser, setCurrentUser] = useState(null);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [conversations, setConversations] = useState([]);

  // Fetch conversations for logged in user
  const loadConversations = useCallback(async () => {
    try {
      const data = await chatAPI.getConversations();
      setConversations(Array.isArray(data) ? data : []);
    } catch (err) {
      console.warn('Could not load conversations:', err);
    }
  }, []);

  // Check auth session on startup
  useEffect(() => {
    if (getToken()) {
      authAPI
        .getMe()
        .then((user) => {
          setCurrentUser(user);
          if (user.district) setDistrict(user.district);
          if (user.language) setLanguage(user.language);
          loadConversations();
        })
        .catch(() => {
          setCurrentUser(null);
        });
    }
  }, [loadConversations]);

  // Load initial reference data
  useEffect(() => {
    const loadData = async () => {
      try {
        const [districtsData, cropsData] = await Promise.all([
          chatAPI.getDistricts(),
          chatAPI.getCrops(),
        ]);
        setDistricts(districtsData.districts || []);
        setCrops(cropsData.crops || []);
      } catch (err) {
        console.error('Error loading initial data:', err);
      }
    };
    loadData();
  }, []);

  // Fetch weather data when district changes
  useEffect(() => {
    if (district) {
      chatAPI
        .getWeather(district)
        .then((data) => {
          setWeatherData(data);
        })
        .catch((err) => {
          console.warn('Could not fetch weather for district:', err);
          setWeatherData(null);
        });
    } else {
      setWeatherData(null);
    }
  }, [district]);

  const handleSendMessage = async (message, actionTopic = null) => {
    if (!message || !message.trim()) return;

    setIsLoading(true);
    setError(null);

    const userMsgId = Date.now();
    const assistantMsgId = userMsgId + 1;

    // Optimistically append user message
    setMessages((prev) => [
      ...prev,
      { id: userMsgId, role: 'user', content: message }
    ]);

    try {
      const response = await chatAPI.sendMessage(
        message,
        language,
        district,
        crop,
        conversationId
      );

      setConversationId(response.conversation_id);
      setMessages((prev) => [
        ...prev,
        {
          id: assistantMsgId,
          role: 'assistant',
          content: response.answer,
          sources: response.sources,
          topic: response.topic,
          needs_expert: response.needs_expert,
        },
      ]);

      // Refresh conversations list if user is logged in
      if (currentUser) {
        loadConversations();
      }
    } catch (err) {
      console.error('Error sending message:', err);
      setError(
        err.response?.data?.detail ||
        (language === 'kn'
          ? 'ಕಿಸಾನ್‌ಮಿತ್ರ AI ಪ್ರತಿಕ್ರಿಯೆ ಪಡೆಯಲು ವಿಫಲವಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.'
          : 'Failed to get response from KisanMitra AI. Please try again.')
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setConversationId(null);
    setError(null);
  };

  const handleSelectConversation = async (id) => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await chatAPI.getConversationMessages(id);
      setConversationId(data.id);
      setMessages(
        (data.messages || []).map((m) => {
          let parsedSources = null;
          if (m.sources) {
            try {
              parsedSources = typeof m.sources === 'string' ? JSON.parse(m.sources.replace(/'/g, '"')) : m.sources;
            } catch {
              parsedSources = m.sources;
            }
          }
          return {
            id: m.id,
            role: m.role,
            content: m.content,
            created_at: m.created_at,
            sources: parsedSources,
          };
        })
      );
    } catch (err) {
      console.error('Failed to load conversation:', err);
      setError(
        language === 'kn'
          ? 'ಸಂಭಾಷಣೆಯನ್ನು ಲೋಡ್ ಮಾಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ'
          : 'Failed to load conversation'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteConversation = async (id) => {
    try {
      await chatAPI.deleteConversation(id);
      if (conversationId === id) {
        handleClearChat();
      }
      loadConversations();
    } catch (err) {
      console.error('Failed to delete conversation:', err);
    }
  };

  const handleAuthSuccess = (user) => {
    setCurrentUser(user);
    if (user.district) setDistrict(user.district);
    if (user.language) setLanguage(user.language);
    loadConversations();
  };

  const handleLogout = async () => {
    await authAPI.logout();
    setCurrentUser(null);
    setConversations([]);
    handleClearChat();
  };

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
    if (currentUser) {
      authAPI.updateProfile({ language: newLanguage }).catch(() => {});
    }
  };

  const handleQuickAction = (action) => {
    const prompts = {
      'crop-advice': language === 'en'
        ? `What are the best crop management and variety recommendations for ${district || 'Karnataka'}?`
        : `${district || 'ಕರ್ನಾಟಕ'}ದಲ್ಲಿ ಬೆಳೆ ಬೆಳೆಯಲು ಉತ್ತಮ ತಳಿಗಳು ಮತ್ತು ನಿರ್ವಹಣೆ ಯಾವುವು?`,
      'irrigation': language === 'en'
        ? `How often and in what quantities should I irrigate ${crop || 'crops'} during this stage?`
        : `${crop || 'ಬೆಳೆಗೆ'} ಈ ಹಂತದಲ್ಲಿ ಎಷ್ಟು ಬಾರಿ ನೀರಾವರಿ ಮಾಡಬೇಕು?`,
      'pest-disease': language === 'en'
        ? `What are common pests and diseases affecting ${crop || 'crops in my region'} and their management?`
        : `${crop || 'ಬೆಳೆಗಳಿಗೆ'} ಬರುವ ರೋಗಗಳು ಮತ್ತು ಕೀಟಗಳ ನಿಯಂತ್ರಣ ಕ್ರಮಗಳು ಯಾವುವು?`,
      'weather': language === 'en'
        ? `What is the current weather forecast and agricultural field advice for ${district || 'my district'}?`
        : `${district || 'ನನ್ನ ಜಿಲ್ಲೆಯ'} ಪ್ರಸ್ತುತ ಹವಾಮಾನ ಮತ್ತು ಕೃಷಿ ಸಲಹೆ ಏನು?`,
      'schemes': language === 'en'
        ? 'What government agricultural subsidies, solar schemes, and insurance programs are available in Karnataka?'
        : 'ಕರ್ನಾಟಕದಲ್ಲಿ ರೈತರಿಗೆ ಲಭ್ಯವಿರುವ ಸರ್ಕಾರಿ ಸಬ್ಸಿಡಿಗಳು, ಸೌರ ಪಂಪ್ ಯೋಜನೆಗಳು ಮತ್ತು ಬೆಳೆ ವಿಮೆ ವಿವರಗಳು ಯಾವುವು?',
    };

    const prompt = prompts[action] || '';
    if (prompt) {
      handleSendMessage(prompt, action);
    }
  };

  // Localized district pill text
  const districtPillText = district
    ? language === 'kn' && KANNADA_DISTRICT_MAP[district]
      ? `📍 ${KANNADA_DISTRICT_MAP[district]} (${district})`
      : `📍 ${district}`
    : `📍 ${language === 'en' ? 'All Karnataka' : 'ಸಮಗ್ರ ಕರ್ನಾಟಕ'}`;

  return (
    <div className="app">
      {/* Top Navigation Bar */}
      <header className="app-header">
        <div className="header-left">
          <div className="brand-logo" onClick={handleClearChat} role="button" title="Back to Home">
            <span className="logo-icon">🌾</span>
            <div>
              <h1 className="logo-text">KisanMitra <span className="logo-badge">AI</span></h1>
              <span className="logo-subtext">
                {language === 'en' ? 'Smart Agricultural Assistant • Karnataka' : 'ಕರ್ನಾಟಕ ರೈತ ಮಿತ್ರ ಕೃಷಿ AI ಸಹಾಯಕ'}
              </span>
            </div>
          </div>
        </div>

        <div className="header-center">
          <div className="active-context-pills">
            <span className={`context-pill ${district ? 'district-pill' : 'hint-pill'}`}>
              {districtPillText}
            </span>

            {crop && (
              <span className="context-pill crop-pill">
                🌱 {crop}
              </span>
            )}

            {weatherData && weatherData.weather && (
              <span className="context-pill weather-pill">
                ☀️ {weatherData.weather.temperature_celsius}°C {weatherData.weather.weather}
              </span>
            )}
          </div>
        </div>

        <div className="header-right">
          {messages.length > 0 && (
            <button className="btn-home-nav" onClick={handleClearChat}>
              <span>🏠</span> {language === 'en' ? 'Home / New Chat' : 'ಮುಖಪುಟ / ಹೊಸ ಚಾಟ್'}
            </button>
          )}

          {/* User Auth Section */}
          {currentUser ? (
            <div className="user-profile-badge">
              <span className="user-avatar-icon">👤</span>
              <span className="user-display-name">
                {currentUser.name || currentUser.username}
              </span>
              <button
                className="btn-user-logout"
                onClick={handleLogout}
                title={language === 'kn' ? 'ಖಾತೆಯಿಂದ ನಿರ್ಗಮಿಸಿ' : 'Logout'}
              >
                🚪 {language === 'kn' ? 'ನಿರ್ಗಮಿಸಿ' : 'Logout'}
              </button>
            </div>
          ) : (
            <button
              className="btn-user-login-trigger"
              onClick={() => setIsAuthModalOpen(true)}
            >
              <span>👤</span> {language === 'kn' ? 'ಲಾಗಿನ್ / ಸೈನ್ ಅಪ್' : 'Sign In'}
            </button>
          )}

          <LanguageSelector language={language} onLanguageChange={handleLanguageChange} />
        </div>
      </header>

      {/* Main Body */}
      <div className="app-body">
        {/* Sidebar Controls */}
        <aside className="sidebar">
          {/* Karnataka Agriculture Banner Card */}
          <div className="sidebar-banner-card">
            <img
              src="/images/karnataka_agriculture.jpg"
              alt="Karnataka Agriculture"
              className="sidebar-banner-img"
            />
            <div className="sidebar-banner-overlay">
              <h4>{language === 'en' ? 'Farmer Control Panel' : 'ರೈತ ಕಂಟ್ರೋಲ್ ಪ್ಯಾನೆಲ್'}</h4>
              <p>{language === 'en' ? 'Personalize AI guidance' : 'ನಿಮ್ಮ ಕೃಷಿ ವಿವರ ಹೊಂದಿಸಿ'}</p>
            </div>
          </div>

          <div className="sidebar-section">
            <h3 className="section-heading">
              <span>📍</span> {language === 'en' ? 'Your Location' : 'ನಿಮ್ಮ ಜಿಲ್ಲೆ'}
            </h3>
            <DistrictSelector
              districts={districts}
              selectedDistrict={district}
              onDistrictChange={setDistrict}
              language={language}
            />
          </div>

          <div className="sidebar-section">
            <h3 className="section-heading">
              <span>🌱</span> {language === 'en' ? 'Primary Crop' : 'ಮುಖ್ಯ ಬೆಳೆ'}
            </h3>
            <CropSelector
              crops={crops}
              selectedCrop={crop}
              onCropChange={setCrop}
              language={language}
            />
          </div>

          <div className="sidebar-section">
            <h3 className="section-heading">
              <span>⚡</span> {language === 'en' ? 'Quick Actions' : 'ತ್ವರಿತ ಕ್ರಿಯೆಗಳು'}
            </h3>
            <QuickActions onActionClick={handleQuickAction} language={language} />
          </div>

          {/* Conversation History Section */}
          <div className="sidebar-section">
            <ConversationHistory
              conversations={conversations}
              currentConversationId={conversationId}
              onSelectConversation={handleSelectConversation}
              onNewChat={handleClearChat}
              onDeleteConversation={handleDeleteConversation}
              currentUser={currentUser}
              onOpenAuth={() => setIsAuthModalOpen(true)}
              language={language}
            />
          </div>

          {/* Quick Help Card */}
          <div className="sidebar-help-card">
            <div className="help-icon">💡</div>
            <div className="help-text">
              <strong>{language === 'en' ? 'Farmer Helpline' : 'ರೈತ ಸಹಾಯವಾಣಿ'}</strong>
              <p>{language === 'en' ? 'Toll Free: 1800-180-1551 (Kisan Call Center)' : 'ಉಚಿತ ಕರೆ: 1800-180-1551 (ಕಿಸಾನ್ ಕಾಲ್ ಸೆಂಟರ್)'}</p>
            </div>
          </div>
        </aside>

        {/* Chat / Home Dashboard View */}
        <main className="main-content">
          <ChatWindow
            messages={messages}
            isLoading={isLoading}
            onSendMessage={handleSendMessage}
            language={language}
            district={district}
            crop={crop}
            weatherData={weatherData}
            error={error}
          />
        </main>
      </div>

      {/* Footer */}
      <footer className="app-footer">
        <p className="disclaimer">
          {language === 'en'
            ? '⚠️ Disclaimer: KisanMitra AI provides informational assistance based on published agricultural literature. For severe disease outbreaks or legal scheme claims, verify with official government portals and local Krishi Vigyan Kendras (KVK).'
            : '⚠️ ಸೂಚನೆ: ಕಿಸನ್‌ಮಿತ್ರ AI ಅಧಿಕೃತ ಕೃಷಿ ದಾಖಲೆಗಳ ಆಧಾರದ ಮೇಲೆ ಮಾಹಿತಿ ನೀಡುತ್ತದೆ. ಗಂಭೀರ ರೋಗ ಅಥವಾ ಯೋಜನೆ ಅರ್ಹತೆಗೆ ಅಧಿಕೃತ ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್ ಹಾಗೂ ಸ್ಥಳೀಯ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರ (KVK) ಸಂಪರ್ಕಿಸಿ.'}
        </p>
      </footer>

      {/* Auth Modal (Sign Up & Login) */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onSuccess={handleAuthSuccess}
        language={language}
        districts={districts}
      />
    </div>
  );
}

export default App;
