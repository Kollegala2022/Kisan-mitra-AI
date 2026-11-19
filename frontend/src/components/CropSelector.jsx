import React from 'react';

function CropSelector({ crops, selectedCrop, onCropChange, language }) {
  return (
    <div>
      <label htmlFor="crop-select">
        {language === 'en' ? 'Select Crop (Optional)' : 'ಬೆಳೆ ಆರಿಸಿ (ಐಚ್ಛಿಕ)'}
      </label>
      <select
        id="crop-select"
        value={selectedCrop || ''}
        onChange={(e) => onCropChange(e.target.value || null)}
      >
        <option value="">
          {language === 'en' ? '-- Select a Crop --' : '-- ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ --'}
        </option>
        {crops.map((crop) => {
          const displayLabel = language === 'kn' && crop.kannada
            ? `${crop.kannada} (${crop.name})`
            : `${crop.name} ${crop.kannada ? `(${crop.kannada})` : ''}`;

          return (
            <option key={crop.id} value={crop.name}>
              🌱 {displayLabel}
            </option>
          );
        })}
      </select>
    </div>
  );
}

export default CropSelector;
