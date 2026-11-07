# Property Footprint Intelligence

**DSC 180A Capstone | Cotality**
Team: Aarshia Gupta, Clayton Tan, Dhruv Sehgal, Dylan Louie

Mentor: Lawrence Vulis (Cotality)

## Overview
The property industry needs an accurate record of where every building in
the US is, what it's made of, and whether it has been demolished, merged,
or destroyed. Building footprints are increasingly extracted from satellite
imagery, but extraction tools have changed significantly between 2021 and
2025, which makes footprints inconsistent across time and sources. It is
often unclear whether a change in the data reflects a real change on the
ground or an artifact of how the footprint was extracted.

*AI Usage: We used Claude and Copilot to help explain documentation, with additional context on the readings, to help edit parts of this report, and to help plan our repository structure. AI assistance was used for DuckDB code, but all code validation was done manually. All prompts and further details are covered in* `AI_USE.md` *in the repository.*

## Project Phases
**Quarter 1 (Fall): building footprint extraction and analysis**
We are building a foundation in GIS and building data (spatial SQL with
DuckDB, OpenStreetMap, and Overture Maps) and focusing on how building
footprints are extracted and built. Using footprints from OpenStreetMap
(and possibly Microsoft Building Footprints), we develop and test methods
to manipulate footprints and detect geometric anomalies, such as concave
corners and other irregular shapes.

**Quarter 2 (Winter): automated error detection**
Our end goal is a system that automatically extracts building footprints
from satellite imagery and detects errors in them for the property
industry, such as buildings incorrectly marked as demolished or merged.
We may also integrate National Structure Inventory (NSI) data to connect
footprints with property attributes.

## Footprint Analysis
Before applying anomaly detection at scale, we practice our methods on
OpenStreetMap building footprints from four San Diego zip codes (92103,
92104, 92037, and 92105). In each area, we profile the footprints
(building counts, vertex counts, and areas) and test the techniques our
anomaly detection will rely on: shifting footprints to simulate location
errors, buffering to find overlapping or touching buildings, shrinking
footprints to flag slivers and very small shapes, and checking where
centroids fall outside irregular footprints. These zip codes serve as
test areas for developing and validating the methods we will use in Q2.

## Data Sources
| Source | What it provides | Status |
|---|---|---|
| OpenStreetMap | Building footprints, downloaded via the OSM API | In use |
| Census ZCTA boundaries | Zip code boundary polygons used to fetch footprints | In use |
| Microsoft Building Footprints | ML-extracted footprints | Under consideration |
| Overture Maps | Combined global building footprints | Used for exploration |
| National Structure Inventory | Structure-level property attributes | Possible for Q2 |

Data files are not stored in this repo. Running the fetch script `src/data/fetch_osm.py` downloads
them into `data/raw/`. All footprints are reprojected to EPSG:32611
(UTM zone 11N, in meters) so that distances, buffers, and areas are
measured in meters.

## Repository Structure
    building-footprint-quality/
    ├── README.md
    ├── requirements.txt
    ├── .gitignore
    │
    ├── data/                          # not tracked in git
    │   ├── raw/
    │   └── processed/
    │
    ├── src/
    │   ├── data/
    │   │   └── fetch_osm.py           # zip code → OSM footprints → saved file
    │   └── footprints/
    │       ├── metrics.py             # building counts, vertices, areas
    │       ├── manipulate.py          # shifting, buffering, intersections
    │       └── checks.py              # negative buffers, centroid checks
    │
    ├── notebooks/
    │   ├── exploration/               # GIS and spatial SQL fundamentals
    │   │   ├── duckdb_basics.ipynb
    │   │   ├── duckdb_spatial.ipynb
    │   │   └── overture_buildings.ipynb
    │   └── footprint_analysis/        # one notebook per test area
    │       ├── 92103_hillcrest.ipynb
    │       ├── 92104_north_park.ipynb
    │       ├── 92037_la_jolla.ipynb
    │       └── 92105_city_heights.ipynb
    │
    └── docs/
        ├── literature/                # notes on papers and foundation models
        └── osm_contributions.md       # our OpenStreetMap edits

## Setup
    pip install -r requirements.txt

## Usage
Fetch building footprints for a zip code:

    python src/data/fetch_osm.py --zip 92103

Then open the matching notebook in `notebooks/footprint_analysis/`.

## Status
- [x] GIS and spatial SQL fundamentals (DuckDB, Overture, OSM)
- [x] Manual OSM mapping
- [ ] OSM footprint fetching by zip code
- [ ] Footprint profiling and manipulation in four test areas
- [ ] Footprint anomaly detection (concave corners, irregular shapes)
- [ ] Automated extraction and error detection (Q2)
