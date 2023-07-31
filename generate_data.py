#!/usr/bin/python3

import json
import requests

# The "admin 0 scale rank" file from http://geojson.xyz
resp = requests.get("https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_0_scale_rank.geojson")
geojson = resp.json()

for feature in geojson["features"]:
    code = feature["properties"]["sr_adm0_a3"]
    name = feature["properties"]["sr_subunit"]
    del feature["properties"]
    feature["properties"] = {
        "code": code,
        "name": name,
    }

    # Turn the Polygons into MultiPolygons, so the Rust can expect one thing
    if feature["geometry"]["type"] == "Polygon":
        feature["geometry"]["type"] = "MultiPolygon"
        feature["geometry"]["coordinates"] = [feature["geometry"]["coordinates"]]

with open("data.geojson", "w") as f:
    json.dump(geojson, f)
