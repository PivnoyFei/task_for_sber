import json
from pathlib import Path

import folium
import folium.plugins

path: Path = Path("interesting_places.json")
""" можно было сделать и через pydantic но по моему оверхед.
example json code:
[
    {
        "location": [56.3284, 44.0025],
        "tooltip": "Нижегородский Кремль",
        "popup": "Нижегородский Кремль",
        "icon": {"icon": "flag"}
    },
]
"""
datas: list[dict] = json.loads(path.read_text(encoding="utf-8"))

# Примерные координаты границ Нижнего Новгорода
NINO_POLYGON = [
    (56.3930, 43.7388),
    (56.3301, 44.0723),
    (56.2860, 44.1122),
    (56.2385, 44.1281),
    (56.1903, 43.7519),
]


class CustomMap:
    def __init__(self, location: list[float], zoom_start: int) -> None:
        self.polygons: dict = {}
        self.map = folium.Map(location=location, zoom_start=zoom_start)

    def create_polygon(self, name: str, show=False) -> folium.FeatureGroup:
        if not self.polygons.get(name):
            self.polygons[name] = folium.FeatureGroup(name=name, show=show).add_to(self.map)
        return self.polygons[name]

    def add_marker(self, data: dict, polygon: folium.FeatureGroup) -> None:
        if icon := data.get("icon"):
            data["icon"] = folium.Icon(**icon)
        folium.Marker(**data).add_to(polygon)

    def add_polygon(
        self,
        locations: list,
        polygon: folium.FeatureGroup,
        color: str = "blue",
        fill_color: str = "blue",
    ) -> None:
        folium.Polygon(locations=locations, color=color, fill_color=fill_color).add_to(polygon)
 
    def add_controls(self) -> None:
        folium.LatLngPopup().add_to(self.map)
        folium.LayerControl().add_to(self.map)
        folium.plugins.MiniMap().add_to(self.map)
        folium.plugins.Fullscreen(position="topright").add_to(self.map)

    def show_map(self) -> folium.Map:
        return self.map


if __name__ == "__main__":
    nizhny_map = CustomMap(location=[56.2996, 43.9419], zoom_start=12)

    marker_layer = nizhny_map.create_polygon("Маркеры интересных мест", True)
    polygon_layer = nizhny_map.create_polygon("Граница Нижнего Новгорода", False)

    for data in datas:
        nizhny_map.add_marker(data, marker_layer)

    nizhny_map.add_polygon(NINO_POLYGON, polygon_layer)
    nizhny_map.add_controls()
    nizhny_map.show_map().save("index.html")

    # Открываем ссылку в браузере. Если не нужно, закомментируйте.
    import os
    import webbrowser
    webbrowser.open('file://' + os.path.realpath('index.html'))
