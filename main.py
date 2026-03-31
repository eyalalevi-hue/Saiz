#SailZ
#import sys
#import os
import time
import pandas as pd
import numpy as np

#from turtle import st
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#from app import create_streamlit_map
from get_coordinates_by_city import get_coordinates_by_city
from sea_routing import SeaRouter
from risk_analysis import  fetch_and_check_risk
from df_table import results_to_dataframe
from sea_map import create_route_map
#from streamlit_folium import st_folium


### User will provide the origin and destination cities, then we need to get their coordinates.
origin_city = "Tel Aviv" # "Haifa" #not Lisbon
origin_coordinates = get_coordinates_by_city(origin_city)
#print(origin_coordinates) 

destination_city = "Antalya"  #"Larnaka"# "Larnaka" #not Lisbon
destination_coordinates = get_coordinates_by_city(destination_city)
#print(destination_coordinates)


### creating the sea router and getting the path between the origin and destination coordinates
router = SeaRouter(resolution = 0.05) # Resolution in degrees (0.25° ~ 27.8 nautical miles at the equator)
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


### Reduce the number of points to a manageable number for weather analysis (e.g., 5 points)
def get_equally_distributed_points(path, num_points=5):

    if len(path) <= num_points:
        return path  
    
    # יצירת אינדקסים במרווחים שווים (כולל הקצוות)
    indices = np.linspace(0, len(path) - 1, num_points).astype(int)
    
    # שליפת הערכים לפי האינדקסים שחושבו
    return [path[i] for i in indices]

# fot testing.
#my_data = [(35.25, 32.75), (35.5, 33.0), (35.5, 33.25), (35.5, 33.5), (35.5, 33.75), (35.25, 34.0), (35.0, 34.25), (34.75, 34.5), (34.5, 34.75), (34.25, 35.0), (34.0, 35.0), (33.75, 35.0), (33.5, 35.0)]

reduce_path = get_equally_distributed_points(path, 5)
#print ('reduce_path: ',reduce_path)
#print ('Path: ', path)

#reduce oath without the points we will use for the weather analysis
reduce_set = set(reduce_path)
remaining_path = [point for point in path if point not in reduce_set]



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
final_results = analyze_route_risk(reduce_path)

## store the results in a DataFrame
df = results_to_dataframe(final_results)
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y') #Fformating
df = df.sort_values(by=['date', 'waypoint_id'], ascending=[True, True]) #Sorting
df['date'] = df['date'].dt.strftime('%d-%m-%Y') #Re-formatting back to string for better display
print(df)


#Combine the original path with the reduced path to create a complete DataFrame for all waypoints, including those without forecasts.
# 1. יצירת הבסיס מהנתיב המלא (31 נקודות)
df_final = pd.DataFrame(path, columns=['lat', 'lon'])
df_final = pd.merge(df_final, df, on=['lat', 'lon'], how='left')
df_final['waypoint_id'] = range(1, len(df_final) + 1)
text_cols = ['risk_summary', 'wind_direction', 'weather', 'date']
for col in text_cols:
    if col in df_final.columns:
        df_final[col] = df_final[col].fillna("N/A")
num_cols = ['risk_score', 'wind_speed_kn', 'wind_speed_risk', 'wind_gusts_kn', 'wind_gusts_risk', 'rain_mm', 'rain_risk']
for col in num_cols:
    if col in df_final.columns:
        df_final[col] = df_final[col].fillna(0)

if 'run_index' in df_final.columns:
    df_final['run_index'] = df_final['run_index'].ffill().bfill()

#print(df_final.head())



########### create html
sailing_map = create_route_map(df_final)

###########

#Create CSV file for practice.
#Saving the results to a CSV file for further analysis or sharing.
df_final.to_csv('sailing_route_forecast.csv', index=False, encoding='utf-8')
print("✅ 'sailing_route_forecast.csv' saved successfully!")
print("    Go to streamlit_map")

#Create CSV file for practice.
### to create the map with the path and the points we got from the get_path function
sailing_map.save("sailing_route_final.html")
print("Map saved to sailing_route_final.html - Open this file in your browser.")

