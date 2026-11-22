import React from 'react';
import './WeatherCard.css';
import { KANNADA_DISTRICT_MAP } from './DistrictSelector';

function WeatherCard({ weatherData, district, language = 'en', compact = false, isLoading = false }) {
  if (!district && !weatherData) {
    return (
      <div className="weather-card-empty">
        <span className="weather-empty-icon">🌤️</span>
        <p>
          {language === 'kn'
            ? 'ಲೈವ್ ಹವಾಮಾನ ಮತ್ತು ಕೃಷಿ ಸಲಹೆ ಪಡೆಯಲು ಜಿಲ್ಲೆ ಆಯ್ಕೆಮಾಡಿ.'
            : 'Select a district above to view live weather & farming advisory.'}
        </p>
      </div>
    );
  }

  if (isLoading && !weatherData) {
    return (
      <div className="weather-card-loading">
        <div className="weather-skeleton-spinner"></div>
        <span>
          {language === 'kn' ? 'ಹವಾಮಾನ ಮಾಹಿತಿ ಲೋಡ್ ಆಗುತ್ತಿದೆ...' : 'Fetching live district weather...'}
        </span>
      </div>
    );
  }

  if (!weatherData || !weatherData.weather) {
    return null;
  }

  const { weather, farming_advice } = weatherData;
  const districtName = weather.district || district;
  const kannadaDistrict = KANNADA_DISTRICT_MAP[districtName];
  const displayDistrict = language === 'kn' && kannadaDistrict
    ? `${kannadaDistrict} (${districtName})`
    : districtName;

  // Weather condition icons
  const getWeatherIcon = (cond = '') => {
    const c = cond.toLowerCase();
    if (c.includes('rain') || c.includes('drizzle')) return '🌧️';
    if (c.includes('thunder')) return '⛈️';
    if (c.includes('cloud') || c.includes('overcast')) return '⛅';
    if (c.includes('fog')) return '🌫️';
    return '☀️';
  };

  if (compact) {
    return (
      <div className="weather-card-compact">
        <div className="compact-header">
          <span className="compact-icon">{getWeatherIcon(weather.weather)}</span>
          <span className="compact-district">📍 {displayDistrict}</span>
          <span className="compact-temp">{weather.temperature_celsius}°C</span>
          <span className="compact-cond">{weather.weather}</span>
        </div>
        <div className="compact-meta">
          <span>💧 {weather.humidity}% {language === 'kn' ? 'ತೇವಾಂಶ' : 'Humidity'}</span>
          <span>💨 {weather.wind_speed_kmh} km/h {language === 'kn' ? 'ಗಾಳಿ' : 'Wind'}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="weather-card-sidebar">
      <div className="weather-card-top">
        <div className="weather-status-badge">
          <span className="weather-pulse-dot"></span>
          <span>{language === 'kn' ? 'ನೇರ ಹವಾಮಾನ' : 'LIVE WEATHER'}</span>
        </div>
        <div className="weather-district-name">
          📍 {displayDistrict}
        </div>
      </div>

      <div className="weather-hero-row">
        <span className="weather-big-icon">{getWeatherIcon(weather.weather)}</span>
        <div className="weather-temp-block">
          <div className="weather-temp-value">{weather.temperature_celsius}°C</div>
          <div className="weather-cond-text">{weather.weather}</div>
        </div>
      </div>

      <div className="weather-metrics-grid">
        <div className="metric-box">
          <span className="metric-icon">💧</span>
          <div className="metric-content">
            <span className="metric-label">{language === 'kn' ? 'ತೇವಾಂಶ' : 'Humidity'}</span>
            <span className="metric-value">{weather.humidity}%</span>
          </div>
        </div>
        <div className="metric-box">
          <span className="metric-icon">💨</span>
          <div className="metric-content">
            <span className="metric-label">{language === 'kn' ? 'ಗಾಳಿಯ ವೇಗ' : 'Wind Speed'}</span>
            <span className="metric-value">{weather.wind_speed_kmh} km/h</span>
          </div>
        </div>
      </div>

      {farming_advice && (
        <div className="weather-farming-advice">
          <div className="advice-header">
            <span>💡</span>
            <strong>{language === 'kn' ? 'ಕೃಷಿ ಸಲಹೆ' : 'Farming Advisory'}</strong>
          </div>
          <p className="advice-text">
            {farming_advice.split('\n')[0]}
          </p>
        </div>
      )}
    </div>
  );
}

export default WeatherCard;
