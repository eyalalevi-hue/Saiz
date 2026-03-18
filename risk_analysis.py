import requests
from datetime import datetime

def get_cardinal_direction(degrees):
    """Translates wind degrees to cardinal direction (N, S, E, W)."""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = int((degrees + 22.5) % 360 // 45)
    return directions[idx]

def check_risk(wind_speed, wind_gusts, weather_code, rain_sum):
    """
    Calculates the sailing risk score (0-100) and assesses each parameter.
    """
    weather_map = {
        0: ("Clear sky", 0), 1: ("Mainly clear", 0), 2: ("Partly cloudy", 10), 3: ("Overcast", 20),
        45: ("Fog", 60), 48: ("Fog", 60), 51: ("Light Drizzle", 40), 53: ("Moderate Drizzle", 50),
        55: ("Dense Drizzle", 60), 61: ("Slight Rain", 70), 63: ("Moderate Rain", 85), 65: ("Heavy Rain", 100),
        80: ("Slight Rain Showers", 85), 81: ("Moderate Rain Showers", 95), 82: ("Violent Rain Showers", 100),
        95: ("Thunderstorm", 100), 96: ("Thunderstorm with hail", 100), 99: ("Heavy Thunderstorm", 100)
    }
    
    weather_desc, n_weather = weather_map.get(weather_code, ("Severe Weather", 100))

    n_wind = min((wind_speed / 25) * 100, 100)
    n_gust = min((wind_gusts / 35) * 100, 100)
    n_rain = min((rain_sum / 10) * 100, 100)

    total_score = (n_wind * 0.30) + (n_gust * 0.35) + (n_weather * 0.20) + (n_rain * 0.15)

    def get_level(val, low, high):
        if val < low: return "Low Risk"
        if val < high: return "Moderate Risk"
        return "High Risk"

    return {
        "score": round(total_score, 1),
        "summary": get_level(total_score, 40, 71),
        "weather_desc": weather_desc,
        "wind_speed_risk": get_level(wind_speed, 13, 21),
        "wind_gusts_risk": get_level(wind_gusts, 16, 26),
        "rain_risk": get_level(rain_sum, 2, 6)
    }

def fetch_and_check_risk(lat, lon):
    url = (f"https://seasonal-api.open-meteo.com/v1/seasonal?"
           f"latitude={lat}&longitude={lon}&"
           f"daily=weather_code,wind_speed_10m_max,wind_gusts_10m_max,rain_sum,wind_direction_10m_dominant&"
           f"forecast_days=7")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        daily = data["daily"]
        
        full_report = []

        for i in range(len(daily["time"])):
            # המרת תאריך למבנה DD-MM-YYYY (סעיף 1)
            raw_date = daily["time"][i]
            formatted_date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%d-%m-%Y")

            # נתונים גולמיים והמרה לקשר
            w_speed_kn = round(daily["wind_speed_10m_max"][i] * 0.54, 1)
            w_gusts_kn = round(daily["wind_gusts_10m_max"][i] * 0.54, 1)
            w_code = daily["weather_code"][i]
            r_sum = daily["rain_sum"][i]
            w_dir_deg = daily["wind_direction_10m_dominant"][i]

            # ניתוח סיכונים (סעיף 2)
            risk = check_risk(w_speed_kn, w_gusts_kn, w_code, r_sum)

            # בניית האובייקט המזוקק
            day_data = {
                "run_index": i + 1,
                "date": formatted_date,
                "coordinates": {"lat": lat, "lon": lon},
                "risk_assessment": {
                    "total_score": risk["score"],
                    "summary": risk["summary"]
                },
                "raw_metrics": {
                    "wind_speed": {"val": w_speed_kn, "status": risk["wind_speed_risk"]},
                    "wind_gusts": {"val": w_gusts_kn, "status": risk["wind_gusts_risk"]},
                    "wind_direction": get_cardinal_direction(w_dir_deg), # שדה אחד מקוצר (סעיף 3)
                    "weather_description": risk["weather_desc"], # תיאור בלבד (סעיף 3)
                    "rain": {"sum_mm": r_sum, "status": risk["rain_risk"]}
                }
            }
            full_report.append(day_data)

        return full_report

    except Exception as e:
        return {"error": f"Failed: {str(e)}"}

# דוגמה להרצה
all_days = fetch_and_check_risk(52.52, 13.41)
print(all_days[0]) # הדפסת היום הראשון כדוגמה