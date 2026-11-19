import React from 'react';

function DistrictSelector({ districts, selectedDistrict, onDistrictChange, language }) {
  return (
    <div>
      <label htmlFor="district-select">
        {language === 'en' ? 'Select Karnataka District' : 'ಕರ್ನಾಟಕದ ಜಿಲ್ಲೆ ಆರಿಸಿ'}
      </label>
      <select
        id="district-select"
        value={selectedDistrict || ''}
        onChange={(e) => onDistrictChange(e.target.value || null)}
      >
        <option value="">
          {language === 'en' ? '-- Select District (Live Weather) --' : '-- ಜಿಲ್ಲೆ ಆಯ್ಕೆಮಾಡಿ (ಹವಾಮಾನ) --'}
        </option>
        {districts.map((district) => (
          <option key={district} value={district}>
            📍 {district}
          </option>
        ))}
      </select>
    </div>
  );
}

export default DistrictSelector;
