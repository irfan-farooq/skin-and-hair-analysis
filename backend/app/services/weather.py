import requests
from app.config import Config

def get_weather_advice(lat: float, lon: float) -> dict:
    api_key = Config.WEATHER_API_KEY

    if not api_key:
        return {"error": "Weather API key not configured"}

    try:
        # UV and general weather
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        weather_resp = requests.get(weather_url, timeout=5)
        weather_data = weather_resp.json()

        # Air pollution
        pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        pollution_resp = requests.get(pollution_url, timeout=5)
        pollution_data = pollution_resp.json()

        humidity = weather_data["main"]["humidity"]
        weather_desc = weather_data["weather"][0]["description"]

        aqi = pollution_data["list"][0]["main"]["aqi"]
        # AQI: 1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor
        aqi_labels = {1: "good", 2: "fair", 3: "moderate", 4: "poor", 5: "very poor"}

        advice = []

        if humidity < 30:
            advice.append("Air is very dry — use a heavy moisturizer today")
        elif humidity > 70:
            advice.append("High humidity — stick to lightweight, non-comedogenic products")

        if aqi >= 4:
            advice.append("High pollution today — double cleanse at night, use antioxidant serum")
        elif aqi == 3:
            advice.append("Moderate pollution — don't skip your evening cleanse")

        return {
            "humidity": humidity,
            "weather": weather_desc,
            "aqi": aqi_labels.get(aqi, "unknown"),
            "advice": advice
        }

    except Exception as e:
        print(f"Weather API error: {str(e)}")
        return {"error": "Could not fetch weather data"}