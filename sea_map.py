import folium
import pandas as pd
from folium.plugins import TimestampedGeoJson


def create_route_map(df):
    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=7, tiles="CartoDB positron")
    
    for _, row in df.iterrows():
        # --- תיקון השגיאה כאן ---
        raw_date = str(row.get('date', 'N/A'))
        
        # בודק אם התאריך נראה כמו DD-MM-YYYY (מכיל שני מקפים לפחות)
        if '-' in raw_date and len(raw_date.split('-')) == 3:
            date_parts = raw_date.split('-')
            iso_date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
        else:
            iso_date = "No Date" # או פשוט להשאיר את raw_date
        # ------------------------

        def get_risk_color(summary_text):
            # בדיקה אם הערך הוא NaN או None
            if pd.isna(summary_text) or summary_text is None:
                return "blue"
            
            val = str(summary_text).lower().strip()
            if "high" in val: return "red"
            elif "moderate" in val: return "orange"
            elif "low" in val: return "green"
            return "blue"

        m_color = get_risk_color(row['risk_summary'])
        
        # בתוך ה-Popup נציג את התאריך רק אם הוא קיים
        date_display = f"<b>תאריך:</b> {iso_date}<br>" if iso_date != "No Date" else ""
        
        popup_html = f"""
        <div style="direction: rtl; text-align: right; font-family: sans-serif; min-width: 180px;">
            <b style="color: #1565c0;">נקודה: {row['waypoint_id']}</b><br>
            <hr style="margin: 5px 0;">
            {date_display}
            <b>סיכון:</b> {row['risk_summary']}<br>
            <b>רוח:</b> {row['wind_speed_kn']} קשר<br>
        </div>
        """
        
        # בונוס: בוא נעשה את הנקודות הריקות קטנות יותר
        is_forecast = row['risk_summary'] != "N/A" and row['risk_summary'] != "No Forecast"
        radius_size = 12 if is_forecast else 4
        fill_op = 0.8 if is_forecast else 0.4
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=radius_size,
            color=m_color,
            fill=True,
            fill_color=m_color,
            fill_opacity=fill_op,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(m)
        
    # חיבור הנתיב
    points = df[['lat', 'lon']].values.tolist()
    folium.PolyLine(points, color="blue", weight=1, opacity=0.3).add_to(m)
    
    return m




'''
def create_route_map(df):
    """
    מייצר מפה אינטראקטיבית עם סרגל זמן (Slider) המציג את שינויי הסיכון לאורך 7 ימים.
    """
    # 1. הכנת המפה הבסיסית
    m = folium.Map(
        location=[df['lat'].mean(), df['lon'].mean()],
        zoom_start=7,
        tiles="CartoDB positron"
    )

    # 2. פונקציית עזר לצבעים
    def get_color(summary):
        if "Low" in summary: return "green"
        if "Moderate" in summary: return "orange"
        return "red"

    # 3. בניית רשימת ה"פיצ'רים" עבור ה-GeoJSON
    features = []
    
    for _, row in df.iterrows():
        # המרת התאריך לפורמט ISO שסרגל הזמן מבין (YYYY-MM-DD)
        # מכיוון שהתאריך ב-DF הוא DD-MM-YYYY, נהפוך אותו:
        date_parts = row['date'].split('-')
        iso_date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
        
        color = get_color(row['risk_summary'])
        
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [row['lon'], row['lat']], # ב-GeoJSON זה קודם LON ואז LAT
            },
            'properties': {
                'time': iso_date,
                'style': {'color': color, 'fillColor': color},
                'icon': 'circle',
                'iconstyle': {
                    'fillColor': color,
                    'fillOpacity': 0.8,
                    'stroke': 'true',
                    'radius': 8
                },
                'popup': f"""
                    <b>Waypoint {int(row['waypoint_id'])}</b><br>
                    Date: {row['date']}<br>
                    Risk: {row['risk_summary']} ({row['risk_score']})<br>
                    Wind: {row['wind_speed_kn']} kn {row['wind_direction']}
                """
            }
        }
        features.append(feature)

    # 4. הוספת רכיב הזמן למפה
    TimestampedGeoJson(
        {'type': 'FeatureCollection', 'features': features},
        period='P1D', # קפיצות של יום אחד
        add_last_point=True,
        auto_play=False,
        loop=False,
        max_speed=1,
        loop_button=True,
        date_options='YYYY-MM-DD',
        time_slider_drag_update=True
    ).add_to(m)

    # 5. הוספת קו הנתיב הכללי (שיישאר קבוע ברקע)
    # נחלץ את הנקודות הייחודיות של הנתיב (לפי waypoint_id)
    unique_path = df[df['date'] == df['date'].iloc[0]][['lat', 'lon']].values.tolist()
    folium.PolyLine(unique_path, color="blue", weight=1, opacity=0.3).add_to(m)

    return m


'''


# --- הרצה ---
# וודא שהשתמשת ב-df_sorted מהשלב הקודם
# animated_map = create_animated_route_map(df_sorted)

# # שמירה
# animated_map.save("sailing_forecast_animated.html")
# print("Animated map ready! Open 'sailing_forecast_animated.html' in your browser.")
# --- הרצה ---
# וודא ש-df_sorted הוא ה-DataFrame הממוין שלך
# sailing_map = create_route_map(df_sorted)

# # שמירה וצפייה
# sailing_map.save("sailing_route_final.html")
# print("Map saved to sailing_route_final.html - Open this file in your browser.")