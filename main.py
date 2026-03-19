#SailZ
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#from get_path import get_path # type: ignore
#from time import time
#from turtle import distance

#import requests
#import tkinter as TK
from get_coordinates_by_city import get_coordinates_by_city
#from get_path import get_path
 # type: ignore
#import json
import pandas as pd

from sea_routing import SeaRouter
#from sea_map import create_interactive_sea_map
from risk_analysis import  fetch_and_check_risk
from df_table import results_to_dataframe
from sea_mapp import create_route_map


### User will provide the origin and destination cities, then we need to get their coordinates.
origin_city = "Haifa"
origin_coordinates = get_coordinates_by_city(origin_city)
#print(origin_coordinates) 

destination_city = "Larnaka" #not Lisbon
destination_coordinates = get_coordinates_by_city(destination_city)
#print(destination_coordinates)


###Old version 
#while we got the cities cordinations we need to send them and get back the distance between them, and the number of points in path. every 20 nautical miles we will add one point to the path.
#we will use the get_path function for that.

# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# from get_path import get_path # type: ignore

#####get_path function doesnt work correctly.######

# origin = origin_coordinates #(32.08, 34.7)
# #destination = (32.0, 34.7) # for testing the case when the distance is '0'
# destination = destination_coordinates #(38.7, -9.13)
# #get_path(origin, destination)
# #distances, 
# dist, num_points = get_path(origin, destination)

# print(f"Distance: {dist}")
# print(f"Points: {num_points}")
##########


#now, we have the distance and the number of points in the path, we can use this information to get the coordinates of the points along the path.
#this is second option. waiting for searoutes.com to assistance respond. 

#Distance: 2663.61
#Points: 92




##haifa_port = (32.824, 35.003)
##limassol_port = (34.674, 33.042)


### creating the sea router and getting the path between the origin and destination coordinates
router = SeaRouter(resolution = 0.25) # Resolution in degrees (0.25° ~ 27.8 nautical miles at the equator)
dist, path = router.get_sea_path(origin_coordinates, destination_coordinates)

if dist:
    print(f"✅ Route Found!")
    print(f"From: {origin_city} {origin_coordinates}")
    print(f"To: {destination_city} {destination_coordinates}")
    print(f"Total Distance: {dist} Nautical Miles")
    print(f"\nWaypoints (Total {len(path)} points):")
    for i, pt in enumerate(path):
        print(f"Point {i+1}: {pt}")
else:
    print(f"❌ Error: {path}")

#print(path )





### Now we have the path coordinates, we can use them to get the weather information for each point along the path and analyze the risk for sailing on those days.
def analyze_route_risk(coordinate_list):
    route_analysis = []
    print(f"Analyzing {len(coordinate_list)} waypoints. Please wait...")

    for i, (lat, lon) in enumerate(coordinate_list):
        # call API for each point and get the risk assessment
        point_data = fetch_and_check_risk(lat, lon)
        
        if isinstance(point_data, list):
            route_analysis.append({
                "waypoint_id": i + 1,
                "location": {"lat": lat, "lon": lon},
                "forecast": point_data
            })
            print(f"✔ Processed Waypoint {i+1}/{len(coordinate_list)}")
        else:
            print(f"✘ Error at Waypoint {i+1}: {point_data.get('error')}")

        time.sleep(1) 

    return route_analysis


#coords = [(35.25, 32.75), (35.5, 33.0), (35.5, 33.25)]#, (35.5, 33.5), (35.5, 33.75), (35.25, 34.0), (35.0, 34.25), (34.75, 34.5), (34.5, 34.75), (34.25, 35.0), (34.0, 35.0), (33.75, 35.0), (33.5, 35.0)]
#path  = coords
final_results = analyze_route_risk(path)

## store the results in a DataFrame
df = results_to_dataframe(final_results)
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y') #Fformating
df = df.sort_values(by=['date', 'waypoint_id'], ascending=[True, True]) #Sorting
df['date'] = df['date'].dt.strftime('%d-%m-%Y') #Re-formatting back to string for better display
print(df)


sailing_map = create_route_map(df)

### to create the map with the path and the points we got from the get_path function
sailing_map.save("sailing_route_final.html")
print("Map saved to sailing_route_final.html - Open this file in your browser.")


### to create the map with the path and the points we got from the get_path function
#create_interactive_sea_map(path, origin_coordinates, destination_coordinates)
#create_route_map(df, filename="sea_route_points.html")
# sailing_map = create_route_map(df)





'''
Next steps:
1. use path points to provide weather information for each point along the path. waiting 
2. Integrate the get_path function with the SeaRouter to get the actual path coordinates. 
3. Add error handling for cases where no path is found or when the API fails. negetive cordinate.get_coordinates_by_city - Lisbon, Portugal.listed as (38.7, -9.13) instead of (38.7, -9.13)
'''










'''
import numpy as np

def get_equally_distributed_points(data, num_points=10):
    """
    מחזירה מספר מוגדר של נקודות מתוך רשימה בהתפלגות שווה על פני האינדקסים.
    """
    if len(data) <= num_points:
        return data  # אם הסדרה קצרה מדי, מחזירים את כולה
    
    # יצירת אינדקסים במרווחים שווים (כולל הקצוות)
    indices = np.linspace(0, len(data) - 1, num_points).astype(int)
    
    # שליפת הערכים לפי האינדקסים שחושבו
    return [data[i] for i in indices]

# דוגמה לשימוש:
my_data = list(range(100, 1000, 5)) # סדרה של 180 ערכים
result = get_equally_distributed_points(my_data, 10)

print(f"נבחרו {len(result)} נקודות:")
print(result)
'''