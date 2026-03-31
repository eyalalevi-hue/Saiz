### Sea Routing Module. map creation and path finding between two points in the sea.


import networkx as nx
import math
from global_land_mask import globe

class SeaRouter:
    def __init__(self, resolution=0.5):
        self.resolution = resolution
        self.G = nx.Graph()
        self._build_sea_graph()

    def _build_sea_graph(self):
        # יצירת רשת נקודות בים באזור הים התיכון (לביצועים מהירים)
        lat_range = range(30, 40) 
        lon_range = range(30, 40)
        
        for lat in [x * self.resolution for x in range(int(30/self.resolution), int(40/self.resolution))]:
            for lon in [x * self.resolution for x in range(int(30/self.resolution), int(40/self.resolution))]:
                if not globe.is_land(lat, lon):
                    self.G.add_node((round(lat, 3), round(lon, 3)))

        for node in self.G.nodes():
            lat, lon = node
            for d_lat in [-self.resolution, 0, self.resolution]:
                for d_lon in [-self.resolution, 0, self.resolution]:
                    if d_lat == 0 and d_lon == 0: continue
                    neighbor = (round(lat + d_lat, 3), round(lon + d_lon, 3))
                    if self.G.has_node(neighbor):
                        dist = self._haversine(lat, lon, neighbor[0], neighbor[1])
                        self.G.add_edge(node, neighbor, weight=dist)

    def _haversine(self, lat1, lon1, lat2, lon2):
        R = 3440.065
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return R * 2 * math.asin(math.sqrt(a))

    def get_sea_path(self, origin, destination):
        start_node = min(self.G.nodes(), key=lambda n: self._haversine(origin[0], origin[1], n[0], n[1]))
        end_node = min(self.G.nodes(), key=lambda n: self._haversine(destination[0], destination[1], n[0], n[1]))
        
        try:
            path = nx.astar_path(self.G, start_node, end_node, weight='weight')
            total_dist = sum(self.G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))
            return round(total_dist, 3), path
        except nx.NetworkXNoPath:
            return None, "No path found"


'''

# --- TESTING ---

# קואורדינטות מדויקות
haifa_port = (32.824, 35.003)
limassol_port = (34.674, 33.042)

router = SeaRouter(resolution=0.25) # רזולוציה גבוהה לדיוק מירבי
dist, path = router.get_sea_path(haifa_port, limassol_port)

if dist:
    print(f"✅ Route Found!")
    print(f"From: Haifa {haifa_port}")
    print(f"To: Limassol {limassol_port}")
    print(f"Total Distance: {dist} Nautical Miles")
    print(f"\nWaypoints (Total {len(path)} points):")
    for i, pt in enumerate(path):
        print(f"Point {i+1}: {pt}")
else:
    print(f"❌ Error: {path}")
    '''