#SailZ

from turtle import distance

import requests
import tkinter as TK
from get_coordinates_by_city import get_coordinates_by_city
#from get_path import get_path
 # type: ignore
import json
import pandas as pd

## - Testing - API working fine.
# API_KEY = "91a0ba76dbf81c8d4a4778ebff5cd5fb"
# lat = 32.3
# lon = 34.8
# url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
# response = requests.get(url)
# data = response.json()
# print(data) 

# User will provide the origin and destination cities, and we will get their coordinates using the get_coordinates_by_city function.
origin_city = "Tel Aviv"
origin_coordinates = get_coordinates_by_city(origin_city)
print(origin_coordinates) 

destination_city = "Lisbon"
destination_coordinates = get_coordinates_by_city(destination_city)
print(destination_coordinates)



#while we got the cities cordinations we need to send them and get back the distance between them, and the number of points in path. every 20 nautical miles we will add one point to the path.
#we will use the get_path function for that.

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from get_path import get_path # type: ignore

origin = origin_coordinates #(32.08, 34.7)
#destination = (32.0, 34.7) # for testing the case when the distance is '0'
destination = destination_coordinates #(38.7, -9.13)
#get_path(origin, destination)
#distances, 
dist, num_points = get_path(origin, destination)

print(f"Distance: {dist}")
print(f"Points: {num_points}")

#now, we have the distance and the number of points in the path, we can use this information to get the coordinates of the points along the path.
#this is second option. waiting for searoutes.com to assistance respond. 

#Distance: 2663.61
#Points: 92



