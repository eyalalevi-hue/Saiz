import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


# ייבוא המרחק - הגנה מפני קריסה
# try:
#     from main import dist
# except Exception:
#     dist = "N/A"


## זמני לטובת בדיקות שימוש רק במרחק מתוך משתנה קבוע
### להחליף בהרצה 
dist =  356.98  # מרחק קבוע לדוגמה (120 מייל ימי)

# --- 1. הגדרות דף ---
st.set_page_config(layout="wide", page_title="Sailing Risk Advisor")

# --- 2. CSS לעברית ---
st.markdown("""
    <style>
    .rtl-text {
        direction: rtl;
        text-align: right;
    }
    .stMetric, .stAlert {
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. מאגר נמלים מקומי ---
LOCAL_PORTS = {
    "Tel Aviv": [32.0853, 34.7818],
    "Antalya": [36.8872942, 30.7074549],
    "Haifa": [32.8192, 34.9992],
    "Limassol": [34.6750, 33.0440],
    "Larnaca": [34.9173, 33.6427],
    "Rhodes": [36.4452, 28.2277]
}

# --- 4. טעינת נתונים ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('sailing_route_forecast.csv')
        df.columns = df.columns.str.strip()
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
        df['date'] = df['date'].astype(str).str.strip()
        return df.dropna(subset=['lat', 'lon'])
    except Exception as e:
        st.error(f"שגיאה בקריאת הקובץ: {e}")
        return pd.DataFrame()

df_raw = load_data()

# --- 5. לוגיקת בחירה (Sidebar) ---
if df_raw.empty:
    st.error("לא נמצאו נתונים בקובץ CSV.")
    st.stop()

# רשימת תאריכים ייחודיים (רק אלו עם מידע אמיתי)
available_dates = sorted([d for d in df_raw['date'].unique() if d not in ['N/A', 'nan', 'None']])

with st.sidebar:
    st.header("📍 תכנון מסלול")
    origin_city = st.selectbox("נמל מוצא:", list(LOCAL_PORTS.keys()), index=0)
    dest_city = st.selectbox("נמל יעד:", list(LOCAL_PORTS.keys()), index=1)
    
    st.write("---")
    st.write("**בחר תאריך לתחזית:**")
    if available_dates:
        selected_date = st.radio("תאריכים זמינים:", options=available_dates, label_visibility="collapsed")
    else:
        st.warning("אין תאריכים זמינים.")
        st.stop()

# --- 6. עיבוד הנתונים ---
# לוקחים את כל הנקודות לצורך ציור המסלול המלא (17 נקודות)
all_waypoints = df_raw.copy().sort_values('waypoint_id')

# מסננים רק את הנקודות של היום הנבחר לטבלה ולפופאפים (5 נקודות)
info_points = df_raw[df_raw['date'] == selected_date].copy().sort_values('waypoint_id')

# --- 7. פונקציית יצירת המפה ---
def create_map(full_path, date_str, start_city, end_city):
    # מרכוז המפה
    m = folium.Map(location=[full_path['lat'].mean(), full_path['lon'].mean()], 
                   zoom_start=7, tiles="CartoDB positron")
    
    # 1. ציור קו הנתיב המלא (כל הנקודות מחוברות)
    path_coords = full_path[['lat', 'lon']].values.tolist()
    folium.PolyLine(path_coords, color="#3498db", weight=2, opacity=0.5, dash_array='5').add_to(m)
    
    # 2. הוספת נקודות (Waypoints)
    for _, row in full_path.iterrows():
        is_current_forecast = (row['date'] == date_str)
        
        if is_current_forecast:
            # נקודה עם מידע - גדולה וצבעונית
            radius = 8
            risk = str(row['risk_summary']).lower()
            if "high" in risk: color = "#e74c3c"
            elif "moderate" in risk: color = "#f39c12"
            elif "low" in risk: color = "#2ecc71"
            else: color = "#3498db"
            
            html = f"""
            <div style="direction: rtl; text-align: right; font-family: sans-serif; font-size: 12px;">
                <b style="color:{color};">נקודה {int(row['waypoint_id'])}</b><br>
                <b>תחזית:</b> {row['risk_summary']}<br>
                <b>רוח:</b> {row['wind_speed_kn']} קשר<br>
                <b>מזג אוויר:</b> {row['weather']}
            </div>
            """
            popup = folium.Popup(folium.Html(html, script=True), max_width=200)
            opacity = 0.9
        else:
            # נקודת מסלול רגילה - קטנה וכחולה/אפורה
            radius = 2
            color = "#3498db"
            popup = None
            opacity = 0.4

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=radius,
            color=color,
            fill=True,
            fill_opacity=opacity,
            popup=popup
        ).add_to(m)
        
# 3. סמלי מוצא ויעד (מעודכן: רק סיכה למוצא)
    if start_city in LOCAL_PORTS:
        folium.Marker(
            location=LOCAL_PORTS[start_city], 
            icon=folium.Icon(color='blue', icon='ship', prefix='fa'),
            #icon=folium.Icon(color='blue', icon='info-sign'), # סיכה (pin) כחולה
            popup=f"מוצא: {start_city}"
        ).add_to(m)
    
    # הערה: הסרנו את הלולאה שמוסיפה את ה-Marker של היעד לבקשתך
    # # 3. סמלי מוצא ויעד
    # for p_name, p_color in [(start_city, 'blue'), (end_city, 'black')]:
    #     if p_name in LOCAL_PORTS:
    #         folium.Marker(
    #             location=LOCAL_PORTS[p_name], 
    #             icon=folium.Icon(color=p_color, icon='anchor', prefix='fa'),
    #             popup=p_name
    #         ).add_to(m)

    return m

# --- 8. תצוגה ראשית ---
st.markdown(f'<div class="rtl-text"><h2>נתיב הפלגה: {selected_date}</h2></div>', unsafe_allow_html=True)

col_map, col_info = st.columns([4, 1])

with col_map:
    # Key דינמי לרענון המפה
    st_folium(create_map(all_waypoints, selected_date, origin_city, dest_city), 
              width="stretch", height=600, key=f"map_{selected_date}_{origin_city}_{dest_city}")
    st.info(f"📏 מרחק כולל במסלול: {round(dist)} מייל ימי. משך הפלגה עשוי להימשך כ- {round(dist / 8)} שעות")

with col_info:
    st.markdown('<div class="rtl-text"><b>נתוני הפלגה</b></div>', unsafe_allow_html=True)
    st.metric("מנמל", origin_city)
    st.metric("ליעד", dest_city)
    st.write("---")
    st.markdown("""
    <div class="rtl-text">
    <b>מקרא:</b><br>
    🔴 סיכון גבוה<br>
    🟠 סיכון בינוני<br>
    🟢 סיכון נמוך<br>
    🔵 נקודת מסלול
    </div>
    """, unsafe_allow_html=True)

# טבלה תחתונה - משתמשת ב-info_points
st.write("---")
st.subheader("📊 פירוט תחזית לנקודות הדרך")
if not info_points.empty:
    disp_cols = ['waypoint_id', 'risk_summary', 'wind_speed_kn', 'wind_direction', 'weather', 'rain_mm']
    st.dataframe(info_points[disp_cols], width="stretch", hide_index=True)
else:
    st.info("בחר תאריך כדי להציג את פירוט התחזית.")