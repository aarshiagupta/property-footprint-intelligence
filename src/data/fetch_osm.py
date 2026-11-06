"""Fetch OpenStreetMap building footprints for a US zip code.

OSM does not store US zip code boundaries as polygons, so we can't use
`ox.features_from_place("92103")` like the pygis tutorial does with city
names. Instead we:
  1. Get the zip's boundary polygon from the Census Bureau (ZCTA = ZIP Code
     Tabulation Area, the Census's polygon approximation of a zip code).
  2. Ask OSM for every feature tagged `building=*` inside that polygon
     (`ox.features_from_polygon`, the polygon version of the tutorial's call).
  3. Keep only polygon footprints and reproject to UTM 11N (meters).

Usage:
    python src/data/fetch_osm.py --zip 92103
"""

import argparse
from pathlib import Path

import geopandas as gpd
import osmnx as ox
import requests

# Census TIGERweb service, layer 7 = "2020 Census ZIP Code Tabulation Areas"
ZCTA_URL = (
    "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
    "PUMA_TAD_TAZ_UGA_ZCTA/MapServer/7/query"
)
UTM_CRS = "EPSG:32611"  # UTM zone 11N, units = meters (covers San Diego)
RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def fetch_zcta_boundary(zip_code: str) -> gpd.GeoDataFrame:
    """Return the Census ZCTA polygon for a zip code (in lat/lon, EPSG:4326)."""
    params = {
        "where": f"ZCTA5='{zip_code}'",
        "outFields": "ZCTA5,AREALAND,AREAWATER",
        "outSR": 4326,  # return lat/lon so it matches what OSM expects
        "f": "geojson",
    }
    resp = requests.get(ZCTA_URL, params=params, timeout=60)
    resp.raise_for_status()
    boundary = gpd.GeoDataFrame.from_features(resp.json()["features"], crs="EPSG:4326")
    if boundary.empty:
        raise ValueError(f"No ZCTA found for zip code {zip_code}")
    return boundary


def fetch_buildings(boundary: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Download OSM building footprints inside the boundary polygon."""
    polygon = boundary.geometry.union_all()
    gdf = ox.features_from_polygon(polygon, tags={"building": True})

    # OSM returns a (element type, osmid) index, e.g. ("way", 12345).
    # Some "buildings" are mapped as points or lines; footprints must be areas.
    gdf = gdf.reset_index()
    gdf = gdf[gdf.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]

    # Keep a small set of useful columns (OSM returns hundreds of tag columns).
    keep = ["element", "id", "building", "name", "addr:housenumber",
            "addr:street", "building:levels", "geometry"]
    gdf = gdf[[c for c in keep if c in gdf.columns]]

    # Degrees -> meters so later buffers/shifts/areas are in real units.
    return gdf.to_crs(UTM_CRS)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--zip", required=True, help="5-digit zip code, e.g. 92103")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Fetching ZCTA boundary for {args.zip} from Census TIGERweb...")
    boundary = fetch_zcta_boundary(args.zip)
    boundary_path = RAW_DIR / f"zcta_{args.zip}.parquet"
    boundary.to_crs(UTM_CRS).to_parquet(boundary_path)
    print(f"  saved boundary -> {boundary_path}")

    print("Fetching OSM buildings inside the boundary (may take a minute)...")
    buildings = fetch_buildings(boundary)
    buildings_path = RAW_DIR / f"osm_buildings_{args.zip}.parquet"
    buildings.to_parquet(buildings_path)
    print(f"  saved {len(buildings):,} building footprints -> {buildings_path}")
    print(f"  geometry types: {buildings.geometry.geom_type.value_counts().to_dict()}")


if __name__ == "__main__":
    main()
