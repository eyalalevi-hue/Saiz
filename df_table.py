import pandas as pd

def results_to_dataframe(full_route_report):
    """
    Converts the nested route analysis list into a clean Pandas DataFrame.
    """
    flattened_data = []

    for waypoint in full_route_report:
        waypoint_id = waypoint['waypoint_id']
        lat = waypoint['location']['lat']
        lon = waypoint['location']['lon']
        
        for day in waypoint['forecast']:
            # יצירת שורה שטוחה המשלבת נתוני נקודה ונתוני תחזית
            row = {
                "waypoint_id": waypoint_id,
                "lat": lat,
                "lon": lon,
                "date": day['date'],
                "run_index": day['run_index'],
                "risk_score": day['risk_assessment']['total_score'],
                "risk_summary": day['risk_assessment']['summary'],
                "wind_speed_kn": day['raw_metrics']['wind_speed']['val'],
                "wind_speed_risk": day['raw_metrics']['wind_speed']['status'],
                "wind_gusts_kn": day['raw_metrics']['wind_gusts']['val'],
                "wind_gusts_risk": day['raw_metrics']['wind_gusts']['status'],
                "wind_direction": day['raw_metrics']['wind_direction'],
                "weather": day['raw_metrics']['weather_description'],
                "rain_mm": day['raw_metrics']['rain']['sum_mm'],
                "rain_risk": day['raw_metrics']['rain']['status']
            }
            flattened_data.append(row)

    return pd.DataFrame(flattened_data)