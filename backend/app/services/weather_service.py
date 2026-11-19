"""
Weather Service for fetching weather data
"""
import os
from typing import Optional, Dict, Any
import httpx
from datetime import datetime

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
# Using Open-Meteo as free weather API (no key needed)


class WeatherService:
    """Service for fetching weather information"""
    
    # Map of Karnataka districts to coordinates
    DISTRICT_COORDINATES = {
        "Belagavi": {"lat": 15.8497, "lon": 74.4977},  # Belgaum
        "Belgaum": {"lat": 15.8497, "lon": 74.4977},
        "Bagalkot": {"lat": 16.1690, "lon": 75.6193},
        "Bijapur": {"lat": 16.8303, "lon": 75.7197},
        "Dharwad": {"lat": 15.4589, "lon": 75.0193},
        "Gadag": {"lat": 15.4258, "lon": 75.3533},
        "Haveri": {"lat": 14.7959, "lon": 75.3794},
        "Uttara Kannada": {"lat": 14.4480, "lon": 74.5586},
        "Shikarpur": {"lat": 15.7835, "lon": 73.5849},
        
        "Ballari": {"lat": 15.1394, "lon": 76.9214},  # Bellary
        "Bellary": {"lat": 15.1394, "lon": 76.9214},
        "Kadapa": {"lat": 14.4676, "lon": 78.8239},
        "Kolar": {"lat": 13.1339, "lon": 78.1283},
        "Chikballapur": {"lat": 13.4336, "lon": 77.7333},
        "Tumkur": {"lat": 13.2162, "lon": 77.1144},
        "Chitradurga": {"lat": 14.2267, "lon": 76.3998},
        
        "Bengaluru": {"lat": 12.9716, "lon": 77.5946},
        "Bangalore": {"lat": 12.9716, "lon": 77.5946},
        "Ramanagara": {"lat": 12.7333, "lon": 77.2833},
        
        "Mandya": {"lat": 12.5347, "lon": 76.8896},
        "Mysuru": {"lat": 12.2958, "lon": 76.6394},
        "Mysore": {"lat": 12.2958, "lon": 76.6394},
        "Chamarajanagara": {"lat": 11.9273, "lon": 77.1441},
        
        "Hassan": {"lat": 13.0022, "lon": 75.9369},
        "Kodagu": {"lat": 12.3381, "lon": 75.7260},
        "Coorg": {"lat": 12.3381, "lon": 75.7260},
        
        "Dakshina Kannada": {"lat": 12.8124, "lon": 75.7139},
        "Udupi": {"lat": 13.3387, "lon": 74.7421},
        "Chitradurga": {"lat": 14.2267, "lon": 76.3998},
    }
    
    @staticmethod
    def get_weather(district: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch weather information for a district
        Using Open-Meteo (free, no API key required)
        
        Args:
            district: Karnataka district name
        
        Returns:
            Weather data dictionary
        """
        try:
            if not district:
                return {"error": "District not provided", "weather": None}
            
            # Get coordinates for district
            coords = WeatherService.DISTRICT_COORDINATES.get(district)
            if not coords:
                return {"error": f"District '{district}' not found in database", "weather": None}
            
            # Call Open-Meteo API
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,precipitation",
                "timezone": "Asia/Kolkata"
            }
            
            response = httpx.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            current = data.get("current", {})
            
            # Interpret weather code
            weather_description = WeatherService._interpret_weather_code(current.get("weather_code", 0))
            
            return {
                "error": None,
                "weather": {
                    "district": district,
                    "temperature_celsius": current.get("temperature_2m", "N/A"),
                    "humidity": current.get("relative_humidity_2m", "N/A"),
                    "weather": weather_description,
                    "wind_speed_kmh": current.get("wind_speed_10m", "N/A"),
                    "precipitation_mm": current.get("precipitation", 0),
                    "timestamp": current.get("time", ""),
                    "latitude": coords["lat"],
                    "longitude": coords["lon"]
                }
            }
        
        except httpx.HTTPError as e:
            return {"error": f"Weather service unavailable: {str(e)}", "weather": None}
        except Exception as e:
            return {"error": f"Error fetching weather: {str(e)}", "weather": None}
    
    @staticmethod
    def _interpret_weather_code(code: int) -> str:
        """Interpret WMO weather code"""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, f"Weather code {code}")
    
    @staticmethod
    def get_farming_advice_based_on_weather(weather_data: Dict[str, Any]) -> str:
        """
        Generate farming advice based on current weather
        
        Args:
            weather_data: Weather information dictionary
        
        Returns:
            Farming advice string
        """
        if not weather_data.get("weather"):
            return ""
        
        weather = weather_data["weather"]
        temp = weather.get("temperature_celsius", 0)
        humidity = weather.get("humidity", 0)
        precipitation = weather.get("precipitation_mm", 0)
        weather_desc = weather.get("weather", "")
        
        advice = []
        
        # Temperature advice
        if temp < 15:
            advice.append("• Cold weather detected. Be cautious with tender crops. Provide protection if needed.")
        elif temp > 35:
            advice.append("• High temperature. Increase irrigation frequency. Mulch to conserve soil moisture.")
        
        # Humidity advice
        if humidity > 80:
            advice.append("• High humidity. Check crops for fungal diseases. Ensure good air circulation.")
        elif humidity < 30:
            advice.append("• Low humidity. Increase irrigation. High evaporation expected.")
        
        # Rain advice
        if precipitation > 10:
            advice.append("• Significant rainfall detected. Ensure proper drainage to prevent waterlogging.")
        
        # Weather description advice
        if "rain" in weather_desc.lower():
            advice.append("• Rainy conditions. Avoid spraying pesticides/fungicides. Do field operations on dry days.")
        elif "clear" in weather_desc.lower():
            advice.append("• Clear conditions. Good for field work, spraying, and harvesting operations.")
        
        return "\n".join(advice) if advice else "Current weather conditions are normal for farming operations."
    
    @staticmethod
    def get_supported_districts() -> list:
        """Get list of supported districts"""
        return sorted(list(set(WeatherService.DISTRICT_COORDINATES.keys())))


def get_weather_service() -> WeatherService:
    """Get weather service instance"""
    return WeatherService()
