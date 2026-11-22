import React from 'react';
import './HomeHero.css';
import { KANNADA_DISTRICT_MAP } from './DistrictSelector';

function HomeHero({ language, district, crop, onActionClick, weatherData }) {
  const cards = [
    {
      id: 'crop-advice',
      title: language === 'en' ? 'Crop & Variety Advisory' : 'ಬೆಳೆ ಮತ್ತು ತಳಿ ಸಲಹೆ',
      subtitle: language === 'en' 
        ? 'Paddy, Ragi, Maize, Sugarcane, Cotton, Coffee & Horticulture crop guides.' 
        : 'ಭತ್ತ, ರಾಗಿ, ಮೆಕ್ಕೆಜೋಳ, ಕಬ್ಬು, ಹತ್ತಿ, ಕಾಫಿ ಮತ್ತು ತೋಟಗಾರಿಕೆ ಬೆಳೆಗಳ ಮಾರ್ಗದರ್ಶಿ.',
      image: '/images/crop_growth.jpg',
      tag: language === 'en' ? 'High Yield' : 'ಹೆಚ್ಚು ಇಳುವರಿ',
      prompt: language === 'en'
        ? `What are the best crop management practices for ${crop || 'crops'} in ${district || 'Karnataka'}?`
        : `${district || 'ಕರ್ನಾಟಕ'}ದಲ್ಲಿ ${crop || 'ಬೆಳೆಗಳಿಗೆ'} ಉತ್ತಮ ನಿರ್ವಹಣೆ ಹೇಗೆ?`
    },
    {
      id: 'irrigation',
      title: language === 'en' ? 'Smart Irrigation & Water' : 'ಬುದ್ಧಿವಂತ ನೀರಾವರಿ ನಿರ್ವಹಣೆ',
      subtitle: language === 'en' 
        ? 'Precision drip irrigation, moisture retention, and seasonal watering cycles.' 
        : 'ಹನಿ ನೀರಾವರಿ, ತೇವಾಂಶ ಸಂರಕ್ಷಣೆ ಮತ್ತು ಹಂತ-ಹಂತದ ನೀರಿನ ವೇಳಾಪಟ್ಟಿ.',
      image: '/images/irrigation.jpg',
      tag: language === 'en' ? 'Water Saving' : 'ಜಲ ಸಂರಕ್ಷಣೆ',
      prompt: language === 'en'
        ? `How often and how much should I irrigate ${crop || 'my crops'} during this season?`
        : `${crop || 'ನನ್ನ ಬೆಳೆಗೆ'} ಈ ಋತುವಿನಲ್ಲಿ ಎಷ್ಟು ಬಾರಿ ನೀರುಣಿಸಬೇಕು?`
    },
    {
      id: 'pest-disease',
      title: language === 'en' ? 'Pest & Disease Shield' : 'ಕೀಟ ಮತ್ತು ರೋಗ ರಕ್ಷಣೆ',
      subtitle: language === 'en' 
        ? 'Early symptoms diagnosis, fungal blight control, and safe biological remedies.' 
        : 'ಆರಂಭಿಕ ರೋಗ ಲಕ್ಷಣ, ಶಿಲೀಂಧ್ರ ನಿಯಂತ್ರಣ ಮತ್ತು ಜೈವಿಕ ಪರಿಹಾರಗಳು.',
      image: '/images/pest_control.jpg',
      tag: language === 'en' ? 'Crop Health' : 'ಸಸ್ಯ ಆರೋಗ್ಯ',
      prompt: language === 'en'
        ? `What are common pests and diseases affecting ${crop || 'crops'} and how to prevent them?`
        : `${crop || 'ಬೆಳೆಗಳಿಗೆ'} ಬರುವ ಸಾಮಾನ್ಯ ಕೀಟ ಮತ್ತು ರೋಗಗಳ ನಿಯಂತ್ರಣ ಹೇಗೆ?`
    },
    {
      id: 'weather',
      title: language === 'en' ? 'Weather & Farm Advisory' : 'ಹವಾಮಾನ ಮತ್ತು ಕೃಷಿ ಸಲಹೆ',
      subtitle: language === 'en' 
        ? 'Real-time temperature, rainfall forecast, and ideal field operation timing.' 
        : 'ಪ್ರಸ್ತುತ ಉಷ್ಣಾಂಶ, ಮಳೆ ಮುನ್ಸೂಚನೆ ಮತ್ತು ಕೃಷಿ ಕೆಲಸಗಳ ಸರಿಯಾದ ಸಮಯ.',
      image: '/images/weather_farming.jpg',
      tag: language === 'en' ? 'Live Climate' : 'ನೇರ ಹವಾಮಾನ',
      prompt: language === 'en'
        ? `What is the current weather impact and farming advice for ${district || 'my district'}?`
        : `${district || 'ನನ್ನ ಜಿಲ್ಲೆಯ'} ಹವಾಮಾನದ ಪ್ರಕಾರ ಕೃಷಿ ಸಲಹೆ ನೀಡಿ.`
    },
    {
      id: 'schemes',
      title: language === 'en' ? 'Govt Schemes & Subsidies' : 'ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಮತ್ತು ಸಬ್ಸಿಡಿ',
      subtitle: language === 'en' 
        ? 'PM-Kisan, Raitha Siri, solar pump subsidies, crop insurance & loans.' 
        : 'ಪಿಎಂ-ಕಿಸಾನ್, ರೈತ ಸಿರಿ, ಸೌರ ಪಂಪ್ ಸಬ್ಸಿಡಿ ಮತ್ತು ಬೆಳೆ ವಿಮೆ ವಿವರಗಳು.',
      image: '/images/government_scheme.jpg',
      tag: language === 'en' ? 'Financial Aid' : 'ಆರ್ಥಿಕ ನೆರವು',
      prompt: language === 'en'
        ? 'What government agricultural subsidies and schemes are currently active for farmers in Karnataka?'
        : 'ಕರ್ನಾಟಕದ ರೈತರಿಗೆ ಪ್ರಸ್ತುತ ಯಾವ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಮತ್ತು ಸಬ್ಸಿಡಿಗಳು ಲಭ್ಯವಿವೆ?'
    },
    {
      id: 'soil-health',
      title: language === 'en' ? 'Soil Health & Fertility' : 'ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಮತ್ತು ಫಲವತ್ತತೆ',
      subtitle: language === 'en' 
        ? 'Organic composting, soil pH balancing, NPK dosage and micronutrients.' 
        : 'ಸಾವಯವ ಗೊಬ್ಬರ, ಮಣ್ಣಿನ pH ಸಮತೋಲನ, NPK ಪ್ರಮಾಣ ಮತ್ತು ಸೂಕ್ಷ್ಮ ಪೋಷಕಾಂಶಗಳು.',
      image: '/images/soil_health.jpg',
      tag: language === 'en' ? 'Fertility' : 'ಫಲವತ್ತತೆ',
      prompt: language === 'en'
        ? `How to test and improve soil fertility for ${crop || 'farming'} in ${district || 'Karnataka'}?`
        : `${district || 'ಕರ್ನಾಟಕ'}ದಲ್ಲಿ ${crop || 'ಕೃಷಿಗಾಗಿ'} ಮಣ್ಣಿನ ಫಲವತ್ತತೆ ಹೆಚ್ಚಿಸುವುದು ಹೇಗೆ?`
    },
  ];

  return (
    <div className="home-hero">
      {/* Hero Banner Section with Realistic Background */}
      <div className="hero-banner">
        <div className="hero-overlay"></div>
        <div className="hero-content">
          <div className="hero-badge">
            <span className="badge-pulse"></span>
            <span className="badge-text">
              {language === 'en' ? '🌾 AGRI-TECH AI ASSISTANT • KARNATAKA' : '🌾 ಕೃಷಿ ತಂತ್ರಜ್ಞಾನ AI ಸಹಾಯಕ • ಕರ್ನಾಟಕ'}
            </span>
          </div>

          <h1 className="hero-title">
            {language === 'en' ? (
              <>
                SMART FARMING FOR <br />
                <span className="hero-highlight">HIGHER CROP YIELDS</span>
              </>
            ) : (
              <>
                ಬುದ್ಧಿವಂತ ಕೃಷಿ, <br />
                <span className="hero-highlight">ಸಮೃದ್ಧ ಫಸಲು ಮತ್ತು ಲಾಭ</span>
              </>
            )}
          </h1>

          <p className="hero-subtitle">
            {language === 'en'
              ? 'Instant, verified agricultural advisory tailored to Karnataka’s districts, weather patterns, and crop lifecycles.'
              : 'ಕರ್ನಾಟಕದ ಜಿಲ್ಲೆಗಳು, ಹವಾಮಾನ ಮತ್ತು ಬೆಳೆಗಳಿಗಾಗಿ ತ್ವರಿತ ಹಾಗೂ ಪರಿಶೀಲಿಸಿದ ಕೃಷಿ ಮಾರ್ಗದರ್ಶನ.'}
          </p>

          <div className="hero-stats">
            <div className="stat-item">
              <span className="stat-number">22+</span>
              <span className="stat-label">{language === 'en' ? 'Crops Covered' : 'ಬೆಳೆಗಳು'}</span>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <span className="stat-number">30+</span>
              <span className="stat-label">{language === 'en' ? 'Districts' : 'ಜಿಲ್ಲೆಗಳು'}</span>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <span className="stat-number">100%</span>
              <span className="stat-label">{language === 'en' ? 'Verified RAG Knowledge' : 'ಪರಿಶೀಲಿಸಿದ ಮಾಹಿತಿ'}</span>
            </div>
          </div>
        </div>

        {weatherData && weatherData.weather ? (
          <div className="hero-weather-card">
            <div className="weather-card-header">
              <span className="weather-badge">🌦️ {language === 'en' ? 'Live Weather' : 'ಹವಾಮಾನ'}</span>
              <span className="weather-district">
                {language === 'kn' && KANNADA_DISTRICT_MAP[weatherData.weather.district]
                  ? `${KANNADA_DISTRICT_MAP[weatherData.weather.district]} (${weatherData.weather.district})`
                  : weatherData.weather.district}
              </span>
            </div>
            <div className="weather-temp-row">
              <div className="weather-temp">{weatherData.weather.temperature_celsius}°C</div>
              <div className="weather-condition">{weatherData.weather.weather}</div>
            </div>
            <div className="weather-details">
              <span>💧 {weatherData.weather.humidity}% {language === 'kn' ? 'ತೇವಾಂಶ' : 'Humidity'}</span>
              <span>💨 {weatherData.weather.wind_speed_kmh} km/h {language === 'kn' ? 'ಗಾಳಿ' : 'Wind'}</span>
            </div>
            {weatherData.farming_advice && (
              <div className="weather-advice-snippet">
                💡 {weatherData.farming_advice.split('\n')[0]}
              </div>
            )}
          </div>
        ) : (
          <div className="hero-weather-card hero-weather-card-hint">
            <div className="weather-card-header">
              <span className="weather-badge">🌦️ {language === 'en' ? 'Live Weather' : 'ಹವಾಮಾನ'}</span>
            </div>
            <p className="hero-weather-hint-text">
              {language === 'en'
                ? '👈 Select your district from the sidebar to view live temperature, humidity, wind & farming tips.'
                : '👈 ನೇರ ತಾಪಮಾನ, ತೇವಾಂಶ, ಗಾಳಿ ಮತ್ತು ಕೃಷಿ ಸಲಹೆ ವೀಕ್ಷಿಸಲು ಎಡಭಾಗದಲ್ಲಿ ನಿಮ್ಮ ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.'}
            </p>
          </div>
        )}
      </div>

      {/* Realistic Category Grid */}
      <div className="hero-grid-section">
        <div className="section-header">
          <div>
            <h2 className="section-title">
              {language === 'en' ? 'Explore Agricultural Guidance' : 'ಕೃಷಿ ಮಾರ್ಗದರ್ಶನ ಪರಿಶೀಲಿಸಿ'}
            </h2>
            <p className="section-desc">
              {language === 'en' 
                ? 'Select any topic below or ask your custom question in the chat' 
                : 'ಕೆಳಗಿನ ಯಾವುದೇ ವಿಷಯವನ್ನು ಆರಿಸಿ ಅಥವಾ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಚಾಟ್‌ನಲ್ಲಿ ಕೇಳಿ'}
            </p>
          </div>
          <div className="section-hint">
            <span>⚡ {language === 'en' ? 'Click card to ask' : 'ಕೇಳಲು ಕಾರ್ಡ್ ಕ್ಲಿಕ್ ಮಾಡಿ'}</span>
          </div>
        </div>

        <div className="cards-grid">
          {cards.map((card) => (
            <div
              key={card.id}
              className="feature-card"
              onClick={() => onActionClick(card.prompt)}
              role="button"
              tabIndex={0}
            >
              <div className="card-image-wrapper">
                <img src={card.image} alt={card.title} className="card-image" loading="lazy" />
                <span className="card-tag">{card.tag}</span>
                <div className="card-image-gradient"></div>
              </div>
              <div className="card-body">
                <h3 className="card-title">{card.title}</h3>
                <p className="card-text">{card.subtitle}</p>
                <div className="card-action">
                  <span>{language === 'en' ? 'Ask AI Guide' : 'AI ಸಲಹೆ ಪಡೆಯಿರಿ'}</span>
                  <span className="arrow-icon">→</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default HomeHero;
