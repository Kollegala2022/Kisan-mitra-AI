import React from 'react';
import './QuickActions.css';

function QuickActions({ onActionClick, language }) {
  const actions = [
    {
      id: 'crop-advice',
      label: language === 'en' ? '🌱 Crop Advice' : '🌱 ಬೆಳೆ ಸಲಹೆ',
    },
    {
      id: 'irrigation',
      label: language === 'en' ? '💧 Irrigation' : '💧 ನೀರಾವರಿ',
    },
    {
      id: 'pest-disease',
      label: language === 'en' ? '🐛 Pest/Disease' : '🐛 ಕೀಟ/ರೋಗ',
    },
    {
      id: 'weather',
      label: language === 'en' ? '🌦️ Weather' : '🌦️ ಹವಾಮಾನ',
    },
    {
      id: 'schemes',
      label: language === 'en' ? '🏛️ Schemes' : '🏛️ ಯೋಜನೆಗಳು',
    },
  ];

  return (
    <div className="quick-actions">
      {actions.map((action) => (
        <button
          key={action.id}
          className="quick-action-btn"
          onClick={() => onActionClick(action.id)}
        >
          {action.label}
        </button>
      ))}
    </div>
  );
}

export default QuickActions;
