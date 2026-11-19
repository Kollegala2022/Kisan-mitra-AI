import React from 'react';

export const KANNADA_DISTRICT_MAP = {
  'Bagalkot': 'ಬಾಗಲಕೋಟೆ',
  'Ballari': 'ಬಳ್ಳಾರಿ',
  'Bellary': 'ಬಳ್ಳಾರಿ',
  'Belagavi': 'ಬೆಳಗಾವಿ',
  'Belgaum': 'ಬೆಳಗಾವಿ',
  'Bengaluru': 'ಬೆಂಗಳೂರು',
  'Bangalore': 'ಬೆಂಗಳೂರು',
  'Bengaluru Urban': 'ಬೆಂಗಳೂರು ನಗರ',
  'Bengaluru Rural': 'ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ',
  'Bidar': 'ಬೀದರ್',
  'Bijapur': 'ವಿಜಯಪುರ',
  'Vijayapura': 'ವಿಜಯಪುರ',
  'Chamarajanagara': 'ಚಾಮರಾಜನಗರ',
  'Chamarajanagar': 'ಚಾಮರಾಜನಗರ',
  'Chikballapur': 'ಚಿಕ್ಕಬಳ್ಳಾಪುರ',
  'Chikkaballapur': 'ಚಿಕ್ಕಬಳ್ಳಾಪುರ',
  'Chikkamagaluru': 'ಚಿಕ್ಕಮಗಳೂರು',
  'Chitradurga': 'ಚಿತ್ರದುರ್ಗ',
  'Dakshina Kannada': 'ದಕ್ಷಿಣ ಕನ್ನಡ',
  'Davanagere': 'ದಾವಣಗೆರೆ',
  'Dharwad': 'ಧಾರವಾಡ',
  'Gadag': 'ಗದಗ',
  'Hassan': 'ಹಾಸನ',
  'Haveri': 'ಹಾವೇರಿ',
  'Kalaburagi': 'ಕಲಬುರಗಿ',
  'Gulbarga': 'ಕಲಬುರಗಿ',
  'Kodagu': 'ಕೊಡಗು',
  'Coorg': 'ಕೊಡಗು',
  'Kolar': 'ಕೋಲಾರ',
  'Koppal': 'ಕೊಪ್ಪಳ',
  'Mandya': 'ಮಂಡ್ಯ',
  'Mysuru': 'ಮೈಸೂರು',
  'Mysore': 'ಮೈಸೂರು',
  'Raichur': 'ರಾಯಚೂರು',
  'Ramanagara': 'ರಾಮನಗರ',
  'Shivamogga': 'ಶಿವಮೊಗ್ಗ',
  'Shimoga': 'ಶಿವಮೊಗ್ಗ',
  'Tumakuru': 'ತುಮಕೂರು',
  'Tumkur': 'ತುಮಕೂರು',
  'Udupi': 'ಉಡುಪಿ',
  'Uttara Kannada': 'ಉತ್ತರ ಕನ್ನಡ',
  'Vijayanagara': 'ವಿಜಯನಗರ',
  'Yadgir': 'ಯಾದಗಿರಿ'
};

export const getDistrictDisplayName = (districtName, language = 'en') => {
  if (!districtName) return '';
  if (language === 'kn') {
    const knName = KANNADA_DISTRICT_MAP[districtName];
    return knName ? `${knName} (${districtName})` : districtName;
  }
  return districtName;
};

function DistrictSelector({ districts, selectedDistrict, onDistrictChange, language }) {
  // Normalize districts into objects with name and kannada
  const normalizedList = React.useMemo(() => {
    if (!districts || !Array.isArray(districts)) return [];
    
    return districts.map((item) => {
      if (typeof item === 'string') {
        return {
          name: item,
          kannada: KANNADA_DISTRICT_MAP[item] || item
        };
      }
      return {
        name: item.name,
        kannada: item.kannada || KANNADA_DISTRICT_MAP[item.name] || item.name
      };
    });
  }, [districts]);

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
        {normalizedList.map((district) => {
          const displayLabel = language === 'kn'
            ? `${district.kannada} (${district.name})`
            : district.name;

          return (
            <option key={district.name} value={district.name}>
              📍 {displayLabel}
            </option>
          );
        })}
      </select>
    </div>
  );
}

export default DistrictSelector;
