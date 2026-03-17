import requests

API_KEY = "91a0ba76dbf81c8d4a4778ebff5cd5fb"

def get_coordinates_by_city(city: str):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if not data:
        print(f"העיר '{city}' לא נמצאה")
        return None

    lat = data[0]["lat"]
    lon = data[0]["lon"]
    return lat, lon


# דוגמת שימוש
city = "Tel Aviv"
result = get_coordinates_by_city(city)

if result:
    lat, lon = result
    print(f"City: {city}")
    print(f"Latitude: {lat}")
    print(f"Longitude: {lon}")
# ```

# **פלט:**
# ```
# City: Tel Aviv
# Latitude: 32.0853
# Longitude: 34.7818