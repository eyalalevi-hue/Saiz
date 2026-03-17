#SailZ

from turtle import distance

import requests
import tkinter as TK
from get_coordinates_by_city import get_coordinates_by_city
from get_path import get_path
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

origin = (32.08, 34.7)
#destination = (32.0, 34.7) # for testing the case when the distance is '0'
destination = (38.7, -9.13)
#get_path(origin, destination)
#distances, 
dist, num_points = get_path(origin, destination)
#print(dist, num_points)
print(f"Distance: {dist}")
print(f"Points: {num_points}")

#now, we have the distance and the number of points in the path, we can use this information to get the coordinates of the points along the path.
#this is second option. waiting for searoutes.com to assistance respond. 

# import os
# import sys

# # בדיקה אם הקובץ קיים בתיקייה
# if os.path.exists("get_path.py"):
#     print("V - הקובץ get_path.py נמצא!")
# else:
#     print("X - הקובץ לא נמצא בתיקייה הנוכחית. רשימת קבצים:", os.listdir())

# try:
#     from get_path import get_path
#     print("V - הייבוא הצליח!")
# except ImportError as e:
#     print(f"X - שגיאת ייבוא: {e}")



# import sys
# import os

# # הוספת התיקייה הנוכחית לנתיב החיפוש של פייתון (קריטי ב-GitHub)
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# try:
#     from get_path import get_path
# except ImportError:
#     # ניסיון ייבוא נוסף למקרה של מבנה תיקיות שונה
#     import get_path as gp
#     get_path = gp.get_path

# origin = (32.08, 34.7)
# destination = (38.7, -9.13)

# # קריאה לפונקציה
# dist, num_points = get_path(origin, destination)

# print(f"Distance: {dist}")
# print(f"Points: {num_points}")



# import sys
# import os

# # הוספת הנתיב הנוכחי לרשימת החיפוש של פייתון
# current_path = os.path.dirname(os.path.abspath(__file__))
# if current_path not in sys.path:
#     sys.path.append(current_path)

# # ייבוא הפונקציה (כולל טיפול במקרה שהקובץ נקרא אחרת ב-GitHub)
# try:
#     from get_path import get_path
# except ImportError as e:
#     print(f"Error: Could not find get_path.py in {current_path}")
#     print(f"Available files: {os.listdir(current_path)}")
#     sys.exit(1)

# # נתונים להרצה
# origin = (32.08, 34.7)
# destination = (38.7, -9.13)

# # קריאה לפונקציה
# # שינוי קטן: אם הפונקציה עכשיו מחזירה רשימת נקודות, כדאי לקרוא למשתנה path_points
# dist, path_points = get_path(origin, destination)

# # הדפסה
# print(f"Distance: {dist}")
# print(f"Path Points: {path_points}")