### Aarshia Gupta: 92103
**Prompt submitted to Claude:** "I'm trying to get the OSM building footprints for my zip code (92103) but extracting by zip code manually isn’t working. can you help me write a script for it? then talk me through step 4, how do i shift the footprints accurately and check the results"


**Task context:** Writing the script to fetch OSM building footprints for ZIP code 92103 (Hillcrest). Part 4a required shifting all building footprints by 5 meters and plotting the original and shifted buildings for comparison. Part 4b required shifting a random 25\% of the footprints by 5 meters and comparing them the same way.


**AI assistance:** Extracting buildings directly by ZIP code from OSM wasn’t working, because OSM doesn’t store US ZIP codes as polygons. Claude suggested getting the ZIP’s Census ZCTA boundary and pulling the OSM buildings inside it, and checked with me before building the script that way. That became \texttt{fetch\_osm.py}, which is now shared with the team. For Step 4, Claude explained the options for an accurate shift. This included working in a projected CRS in meters so 5 m is a true distance, and using IoU against the original footprints to measure how much the shift changes the data. I ran each step myself and wrote the observations from the outputs.


**Validation:** I checked that the data was in EPSG:32611 (meters), that the buildings fell inside the 92103 boundary, and that they lined up with the streets on the basemap. I confirmed the building count (5,974) and checked the vertex and area outliers against the map. For 4a and 4b, I confirmed that every shifted building moved exactly 5 m, with IoU dropping to about 0.4. I also looked at the zoomed plots to check the shifts visually.


### Dhruv Sehgal: 92037
**Prompt submitted to Copilot:** “Buffer all buildings in the area by 5 meters, and calculate how many buffered buildings intersect. Do the same using ST\_DWithin.”


**Task context:** Buffering is used to check for a tolerance zone in models. The task (4c) asks to buffer buildings 5 meters as well as use ST\_DWithin (which would have a $5+5 = $10 meters distance) to check for this and see which building footprints could potentially overlap.


**AI assistance:** The AI model assisted in writing DuckDB code to load the data and write the required queries. This involved counting intersecting buildings excluding self-intersections, comparing buffered intersections with S\_DWithin using a 10-meter threshold, and plotting an example showing original footprints, buffered footprints, and their overlap. I made all the plots by hand, only using AI assistance for the last one.


**Validation:** I validated the analysis by confirming that the buffered-intersection and ST\_DWithin queries excluded self-intersections using a \texttt{building\_id <> b.building\_id}. I checked that the total counts across all intersection categories summed to 14,316, the total number of building footprints. I also compared the two methods' distributions and inspected the example plot to confirm that the original footprints, 5-meter buffers, and highlighted overlap were displayed correctly.

### Dylan Louie: 92105
**Prompt submitted to Claude:** "How do I fetch building footprints using a ZIP code like 92105 in Python, and how do I fix the connection and geocoding errors that pop up?"


**Task context:** Retrieving building footprints for San Diego ZIP code 92105 using OpenStreetMap data via OSMnx,handling API and geometry errors during retrieval, and understanding the resulting geospatial data structures.

**AI assistance:** Claude provided an OSMnx script to fetch footprints using a point buffer and address query, diagnosed a Nominatim polygon geocoding failure, and resolved an Overpass API rate-limit error by configuring custom API mirrors and user-agent settings. It also explained the structural distinction between way (standard polygons) and relation(multipolygons/complex footprints) present in the resulting GeoDataFrame index.


**Validation:** I ran the updated script with the custom Overpass endpoint, verified that the API returned valid GeoJSON data without network decode errors, and plotted the resulting footprints to visually confirm that building shapes were properly retrieved across the target area.

### Clayton Tan: 92104
**Prompt submitted to Claude:** for the code checkpoint, help me start with the code for 4a”


**Task context:** Part 4a required shifting all building footprints in ZIP code 92104 (North Park) by 5 meters and plotting the original and shifted buildings for comparison.

**AI assistance:** Claude generated the initial notebook for Part 4a, using the building footprint data previously collected through \texttt{fetch\_osm.py}. The notebook shifts every footprint 5 m east with DuckDB’s ST\_Translate(geom, 5, 0) and plots the original (blue) and shifted (red) footprints in a zoomed 250 m window. I ran the notebook on the 92104 data, checked the outputs below, and added it to the repo through a pull request.

**Validation:** I checked that the coordinate system was EPSG:32611, verified that the building footprints appeared within the correct ZIP code boundary, and confirmed that every building centroid moved exactly 5 meters. I also visually inspected the original and shifted footprints to confirm that the translation worked correctly.
### Clayton Tan: 92104 reentrant corners
**Prompt submitted to Claude (paraphrased):** pasted the reentrant-corners SQL homework and asked for help writing the code for 92104.

**Task context:** Find the reentrant (concave) corners of every building footprint in ZIP 92104 using SQL, measure how deep each one is, and summarise the results.

**AI assistance:** Claude drafted `notebooks/footprint_analysis/92104_reentrant_corners.ipynb`. The DuckDB query explodes each polygon into vertices, uses the cross product of the edges either side of each vertex (signed by the ring's orientation) to flag concave corners, gets the interior angle with atan2, and measures depth as distance to the convex hull. Claude also explained the geometry behind each step.

**Validation:** I ran the notebook on the 92104 footprints. I tested the method first on shapes with known answers: an L drawn counterclockwise and the same L drawn clockwise each gave exactly one 270° corner at (1, 1), and a square gave none, so the orientation handling works. On the real data the interior angles cluster at 270° (median 270.0°, IQR 269.8–270.1°), which fits right-angled notches. 13,856 reentrant corners across 4,815 of 10,826 buildings (44.5%); median depth 1.45 m, with 40.9% deeper than 6 ft. I also inspected the plots to confirm the flagged corners sit on visible notches.
