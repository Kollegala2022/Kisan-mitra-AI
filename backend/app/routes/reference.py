"""
Reference data routes (crops, districts, schemes)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import SchemeLink
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/api", tags=["reference"])

# List of crops commonly grown in Karnataka
KARNATAKA_CROPS = [
    {"id": 1, "name": "Rice", "kannada": "ಅರಿಸಿ"},
    {"id": 2, "name": "Wheat", "kannada": "ಗೋಧಿ"},
    {"id": 3, "name": "Maize", "kannada": "ಕಂಬು"},
    {"id": 4, "name": "Ragi", "kannada": "ರಾಗಿ"},
    {"id": 5, "name": "Sugarcane", "kannada": "ಸೆಕ್ಕರೆ"},
    {"id": 6, "name": "Cotton", "kannada": "ಹೆಣ್ಣು"},
    {"id": 7, "name": "Groundnut", "kannada": "ಸೀಮೆ ಸೋಯಾಬೀನ್"},
    {"id": 8, "name": "Sunflower", "kannada": "ಸೂರ್ಯಕಾಂತಿ"},
    {"id": 9, "name": "Coconut", "kannada": "ತೆಂಗುಳಿ"},
    {"id": 10, "name": "Arecanut", "kannada": "ಹೂಕಾಯಿ"},
    {"id": 11, "name": "Coffee", "kannada": "ಕೋಪಿ"},
    {"id": 12, "name": "Cardamom", "kannada": "ಏಲಕ್ಕಿ"},
    {"id": 13, "name": "Pepper", "kannada": "ಕರಿಮೆನುಸುಪ್ಪು"},
    {"id": 14, "name": "Turmeric", "kannada": "ನೀರುಗುಂಡೆ"},
    {"id": 15, "name": "Tomato", "kannada": "ಟೊಮ್ಯಾಟೊ"},
    {"id": 16, "name": "Onion", "kannada": "ಈರುಳ್ಳಿ"},
    {"id": 17, "name": "Potato", "kannada": "ಅಳುಗೆ"},
    {"id": 18, "name": "Brinjal", "kannada": "ಬದನೆ"},
    {"id": 19, "name": "Okra", "kannada": "ಭೆಂಡೆ"},
    {"id": 20, "name": "Chilli", "kannada": "ಮೆಣಸೆ"},
    {"id": 21, "name": "Pulses", "kannada": "ಪರಿವಾಳೆ"},
    {"id": 22, "name": "Arhar (Pigeon Pea)", "kannada": "ಟೂರಿ"},
]

# List of districts in Karnataka with official Kannada names
KARNATAKA_DISTRICTS = [
    {"name": "Bagalkot", "kannada": "ಬಾಗಲಕೋಟೆ"},
    {"name": "Ballari", "kannada": "ಬಳ್ಳಾರಿ"},
    {"name": "Belagavi", "kannada": "ಬೆಳಗಾವಿ"},
    {"name": "Bengaluru Urban", "kannada": "ಬೆಂಗಳೂರು ನಗರ"},
    {"name": "Bengaluru Rural", "kannada": "ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ"},
    {"name": "Bidar", "kannada": "ಬೀದರ್"},
    {"name": "Chamarajanagara", "kannada": "ಚಾಮರಾಜನಗರ"},
    {"name": "Chikkaballapur", "kannada": "ಚಿಕ್ಕಬಳ್ಳಾಪುರ"},
    {"name": "Chikkamagaluru", "kannada": "ಚಿಕ್ಕಮಗಳೂರು"},
    {"name": "Chitradurga", "kannada": "ಚಿತ್ರದುರ್ಗ"},
    {"name": "Dakshina Kannada", "kannada": "ದಕ್ಷಿಣ ಕನ್ನಡ"},
    {"name": "Davanagere", "kannada": "ದಾವಣಗೆರೆ"},
    {"name": "Dharwad", "kannada": "ಧಾರವಾಡ"},
    {"name": "Gadag", "kannada": "ಗದಗ"},
    {"name": "Hassan", "kannada": "ಹಾಸನ"},
    {"name": "Haveri", "kannada": "ಹಾವೇರಿ"},
    {"name": "Kalaburagi", "kannada": "ಕಲಬುರಗಿ"},
    {"name": "Kodagu", "kannada": "ಕೊಡಗು"},
    {"name": "Kolar", "kannada": "ಕೋಲಾರ"},
    {"name": "Koppal", "kannada": "ಕೊಪ್ಪಳ"},
    {"name": "Mandya", "kannada": "ಮಂಡ್ಯ"},
    {"name": "Mysuru", "kannada": "ಮೈಸೂರು"},
    {"name": "Raichur", "kannada": "ರಾಯಚೂರು"},
    {"name": "Ramanagara", "kannada": "ರಾಮನಗರ"},
    {"name": "Shivamogga", "kannada": "ಶಿವಮೊಗ್ಗ"},
    {"name": "Tumakuru", "kannada": "ತುಮಕೂರು"},
    {"name": "Udupi", "kannada": "ಉಡುಪಿ"},
    {"name": "Uttara Kannada", "kannada": "ಉತ್ತರ ಕನ್ನಡ"},
    {"name": "Vijayapura", "kannada": "ವಿಜಯಪುರ"},
    {"name": "Vijayanagara", "kannada": "ವಿಜಯನಗರ"},
    {"name": "Yadgir", "kannada": "ಯಾದಗಿರಿ"},
]


@router.get("/crops")
async def get_crops():
    """Get list of crops commonly grown in Karnataka"""
    try:
        return {
            "status": "success",
            "count": len(KARNATAKA_CROPS),
            "crops": KARNATAKA_CROPS
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching crops: {str(e)}"
        )


@router.get("/districts")
async def get_districts():
    """Get list of districts in Karnataka"""
    try:
        return {
            "status": "success",
            "count": len(KARNATAKA_DISTRICTS),
            "districts": KARNATAKA_DISTRICTS
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching districts: {str(e)}"
        )


@router.get("/schemes")
async def get_schemes(language: str = "en", db: Session = Depends(get_db)):
    """Get government schemes information"""
    try:
        schemes = db.query(SchemeLink).filter(
            SchemeLink.language == language
        ).all()
        
        if not schemes:
            # Return empty list if no schemes in DB
            return {
                "status": "success",
                "count": 0,
                "schemes": []
            }
        
        return {
            "status": "success",
            "count": len(schemes),
            "schemes": [
                {
                    "id": scheme.id,
                    "name": scheme.scheme_name,
                    "description": scheme.description,
                    "eligibility": scheme.eligibility,
                    "official_url": scheme.official_url,
                    "reviewed_date": scheme.reviewed_date.isoformat() if scheme.reviewed_date else None
                }
                for scheme in schemes
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching schemes: {str(e)}"
        )


@router.get("/weather")
async def get_weather(district: str = None):
    """Get current weather for a district"""
    try:
        if not district:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="District parameter is required"
            )
        
        weather_service = WeatherService()
        weather_data = weather_service.get_weather(district)
        
        if weather_data.get("error"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=weather_data["error"]
            )
        
        # Add farming advice
        farming_advice = weather_service.get_farming_advice_based_on_weather(weather_data)
        
        return {
            "status": "success",
            "weather": weather_data["weather"],
            "farming_advice": farming_advice
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching weather: {str(e)}"
        )


@router.get("/supported-districts-weather")
async def get_supported_weather_districts():
    """Get list of districts with weather support"""
    try:
        weather_service = WeatherService()
        districts = weather_service.get_supported_districts()
        
        return {
            "status": "success",
            "count": len(districts),
            "districts": districts
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching supported districts: {str(e)}"
        )
