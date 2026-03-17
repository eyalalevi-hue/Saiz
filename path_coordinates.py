
### Function to get points along the path and distance between the origin and destination coordinates
#this is second option. waiting for searoutes.com to assistance respond.
#import geopandas as gpd
import os


print("geopandas loaded")

#import requests

# קריאת קובץ הנתיבים
#lanes = gpd.read_file("shipping_lanes.geojson")

# import os
# print("Current folder:", os.getcwd())
# print("Files:", os.listdir())


import json

with open("Shipping_Lanes.geojson") as f:
    data_lanes = json.load(f)
data_lanes["features"][0]["geometry"]["coordinates"][0][0]
# lanes = data_lanes["features"]


rows = []

for feature in data_lanes["features"]:

    lane_type = feature["properties"]["Type"]

    for line_id, line in enumerate(feature["geometry"]["coordinates"]):

        for point_id, (lon, lat) in enumerate(line):

            rows.append({
                "lane_type": lane_type,
                "line_id": line_id,
                "point_id": point_id,
                "longitude": lon,
                "latitude": lat
            })

df = pd.DataFrame(rows)

print(df.head())


# מספר נתיבי השיט
print("מספר נתיבים:", len(lanes))

path_coordinates = {
                    "routes":[
                    {
                        "geometry":{
                        "coordinates":[
                            [34.9,32.8],
                            [33.7,33.5],
                            [31.2,34.7],
                            [28.5,36.0],
                            [23.7,37.9],
                            [12.12,33]

                        ]
                        }
                    }
                    ]
                    }

coordinates = path_coordinates["routes"][0]["geometry"]["coordinates"]


for i, coord in enumerate(coordinates):
    lon, lat = coord
    print(f" {i+1}: longitude={lon}, latitude={lat}")