import folium
from folium import plugins

def create_route_map(df, target_date=None):
    """
    מייצר מפה אינטראקטיבית עם נתיב הפלגה, צבעי סיכון וחצי כיוון רוח.
    """
    # 1. סינון ליום ספציפי (ברירת מחדל: היום הראשון בטבלה)
    if target_date is None:
        target_date = df['date'].iloc[0]
    
    day_df = df[df['date'] == target_date].copy()

    # 2. יצירת המפה - ריכוז לפי הממוצע של הקואורדינטות בנתיב
    m = folium.Map(
        location=[day_df['lat'].mean(), day_df['lon'].mean()], 
        zoom_start=8, 
        tiles="CartoDB positron" # מפה נקייה שקל לראות עליה צבעים
    )

    # פונקציה לבחירת צבע לפי רמת סיכון
    def get_color(summary):
        if "Low" in summary: return "green"
        if "Moderate" in summary: return "orange"
        return "red"

    # 3. ציור הנתיב והוספת נקודות
    path_coords = []
    for _, row in day_df.iterrows():
        current_loc = [row['lat'], row['lon']]
        path_coords.append(current_loc)
        
        # טקסט לחלונית המידע
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="margin-bottom:5px;">Waypoint {int(row['waypoint_id'])}</h4>
            <b>Date:</b> {row['date']}<br>
            <b>Risk Score:</b> <span style="color:{get_color(row['risk_summary'])}">{row['risk_score']}</span><br>
            <b>Wind:</b> {row['wind_speed_kn']} kn ({row['wind_direction']})<br>
            <b>Weather:</b> {row['weather']}<br>
            <b>Rain:</b> {row['rain_mm']} mm
        </div>
        """
        
        # הוספת נקודת סיכון (עיגול צבעוני)
        folium.CircleMarker(
            location=current_loc,
            radius=7,
            color=get_color(row['risk_summary']),
            fill=True,
            fill_opacity=0.8,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(m)

        # הוספת חץ כיוון רוח (נעזר באייקון של חץ שמסתובב לפי המעלות)
        # הערה: כיוון הרוח ב-API הוא "מאיפה היא באה", לכן נוסיף 180 מעלות כדי שהחץ יצביע לאן היא נושבת
        # אם יש לך את המעלות המקוריות ב-DF, השתמש בהן. אם לא, נסתפק בנקודות.
        # כאן אני מוסיף סימון ויזואלי פשוט של כיוון הרוח המקוצר כטקסט מעל הנקודה
        folium.map.Marker(
            current_loc,
            icon=folium.DivIcon(
                icon_size=(150,36),
                icon_anchor=(0,0),
                html=f'<div style="font-size: 10pt; color: blue; font-weight: bold;">{row["wind_direction"]}</div>',
            )
        ).add_to(m)

    # 4. חיבור הנקודות בקו
    folium.PolyLine(path_coords, color="blue", weight=2, opacity=0.4, dash_array='5').add_to(m)

    return m

# --- הרצה ---
# וודא ש-df_sorted הוא ה-DataFrame הממוין שלך
# sailing_map = create_route_map(df_sorted)

# # שמירה וצפייה
# sailing_map.save("sailing_route_final.html")
# print("Map saved to sailing_route_final.html - Open this file in your browser.")