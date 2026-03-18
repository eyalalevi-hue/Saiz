import requests

API_KEY = "91a0ba76dbf81c8d4a4778ebff5cd5fb"

def get_coordinates_by_city(city: str):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if not data:
        print(f"City '{city}' not found")
        return None

    lat = data[0]["lat"]
    lon = data[0]["lon"]
    return lat, lon


#### Testing ####
# city = "Tel Aviv"
# result = get_coordinates_by_city(city)

    #if result:
    #lat, lon = result
   
   
  ###Testing the function by printing the coordinates of the city. 
   # print(f"City: {city}")
   # print(f"Latitude: {lat}")
   # print(f"Longitude: {lon}") 
   # print(f"City: {city}")
   # print(f"Latitude: {lat}")
   # print(f"Longitude: {lon}")
# ```

# **פלט:**
# ```
# City: Tel Aviv
# Latitude: 32.0853
# Longitude: 34.7818




## - Testing - API working fine.
# API_KEY = "91a0ba76dbf81c8d4a4778ebff5cd5fb"
# lat = 32.3
# lon = 34.8
# url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
# response = requests.get(url)
# data = response.json()
# print(data) 