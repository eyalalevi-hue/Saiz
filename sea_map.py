import folium

def create_interactive_sea_map(path, origin, destination, filename="sea_route2.html"):
    # 1. יצירת המפה במרכז המסלול
    center_lat = (origin[0] + destination[0]) / 2
    center_lon = (origin[1] + destination[1]) / 2
    
    # שימוש ב-Tiles של OpenStreetMap (או CartoDB)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=7, tiles='CartoDB positron')

    # 2. הוספת שכבת OpenSeaMap (אופציונלי - מציג סימונים ימיים)
    folium.TileLayer(
        tiles='https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png',
        attr='Map data: &copy; OpenSeaMap contributors',
        name='OpenSeaMap',
        overlay=True,
        control=True
    ).add_to(m)

    # 3. ציור המסלול הימי (הקו)
    if path:
        folium.PolyLine(
            locations=path, 
            color="blue", 
            weight=4, 
            opacity=0.7,
            tooltip="Sea Route"
        ).add_to(m)

    # 4. הוספת סמנים (Markers) למוצא וליעד
    folium.Marker(
        location=origin,
        popup="Origin: Haifa",
        icon=folium.Icon(color="green", icon="ship", prefix="fa")
    ).add_to(m)

    folium.Marker(
        location=destination,
        popup="Destination: Limassol",
        icon=folium.Icon(color="red", icon="anchor", prefix="fa")
    ).add_to(m)

    # 5. שמירת המפה לקובץ
    m.save(filename)
    print(f"✅ המפה נוצרה בהצלחה! פתח את הקובץ '{filename}' בדפדפן שלך.")


# נשתמש בנקודות שקיבלנו מה-SeaRouter:
#haifa = (32.82, 35.00)
#limassol = (34.67, 33.04)

#dist, path = router.get_sea_path(haifa, limassol)
# הערה: 'path' הוא רשימת הנקודות שקיבלת מהפונקציה get_sea_path
#create_interactive_sea_map(path, haifa, limassol)