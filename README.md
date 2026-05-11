Workflow for classes 2, 3 and 4. 

## Important links
[UV reference](https://docs.astral.sh/uv/guides/projects/#creating-a-new-project)

### Data
[Open NRW](https://open.nrw/dataset/geokoordinaten-der-stadtbezirke-munster-ms)
[Open data Münster](https://opendata.stadt-muenster.de/user/1115/field_resources%253Afield_format/kml-129/field_resources%253Afield_format/geojson-130)
-> [Link Github with stadtteile Münster](https://github.com/benblankenstein/namiko-dashboard/blob/main/stadtteile-statistische-bezirke-muenster.geojson)
-> [Social and more indexes Münster](https://www.stadt-muenster.de/statistik-stadtforschung/)



## Workflow
### Class 2

1. Install and configure UV
2. New project
```bash
mkdir swm-explorer
cd swm-explorer
uv venv
uv init
```
3. Folder structure
```shell
swm-explorer/
├── pyproject.toml
├── README.md
├── data/                    # GeoJSON should go here
│   └── .gitkeep
└── src/
    └── swm/
        ├── __init__.py
        ├── io.py            # load and validate GeoJSON
        ├── weights/
        │   ├── __init__.py
        │   ├── contiguity.py    # rook, queen via libpysal
        │   ├── distance.py      # distance band, knn geographic
        │   ├── socioeconomic.py # the SWM custom module
        ├── diagnostics.py   # print matrix stats, compare W's
        ├── viz.py           # map and matrix visualization
        └── main.py          # entry point, argument parsing
```

4. Adjust project.toml, don't delete anything, just add to the end of the file, so we can run it with UV as an independent module
```toml
[project.scripts]
swm = "swm.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/swm"]

```
then we build the module with the code editing:
```bash
 uv pip install -e .
```
After this, we can run the project with:
```bash
uv run swm
```

Obs:
> From now on, no need to edit the project.toml by hand. 
> Install dependencies (libraries) with *uv add dependency*, and just run it with *uv run swm*

5. Add logging, and configure it on main.py
```python

# on main.py
# 1. SETUP CONFIGURATION
import sys
import logging
logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",

    handlers=[logging.StreamHandler(sys.stdout)]

)
```
5. Load and adjust Geojson projection

```python
# on io.py

import geopandas as gpd
import logging
# attention to logger:
logger = logging.getLogger(__name__)

def load_database(filename="data.geojson"):

    logger.info("---- loading {} ----".format(filename))

    polygons = gpd.read_file("data/"+filename)

    logger.info("---- adjusting projection ----")
	# Projection should be adjusted to proper calculate distance in meters
	# Question: Is this the best place for it?
    polygons = polygons.to_crs(epsg=25832)

    return polygons

# on main.py

from swm.io import load_database

logger = logging.getLogger(__name__)

def main():
	
	logger.info("SWM Explorer. Starting Execution")

	polygons = load_database()
	print(polygons.head())
```

6. Create contiguity spatial weight matrices module
	1. Rook and Queen
7. Create distance spatial weight matrices module
	1. Distance band, invert distance band, KNN

8. Create a socioeconomic weighting module
> Follow socioeconomic_w.md for reference

9. Create a Moran's I module
```python
# on src/swm/analisys.py
def compute_global_morans():
```

10. Create a reports table module

Exemple of table report. 

W type                  | Moran's I | p-value | z-score
------------------------|-----------|---------|--------
Rook                    |   0.41    |  0.001  |  3.8
Queen                   |   0.43    |  0.001  |  3.9
Distance 1km            |   0.38    |  0.002  |  3.2
Socio-Similarity (Rook) |   0.61    |  0.001  |  5.1
Socio-Gradient (Rook)   |   0.12    |  0.08   |  1.7


11. Update main.py for new usage
```python
import logging
import sys
from pathlib import Path
from swm.io import load_database
from swm.weights import create_rook_swm, create_queen_swm
from swm.weights import create_knn_swm, create_distance_swm
from swm.weights import create_socio_swm
from swm.viz import plot_swm_weighted, plot_lisa
from swm.analysis import compute_local_morans, build_morans_table
from swm.report import print_morans_table, save_morans_table

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

ANALYSIS_VARIABLE = "pct_children_migration_background"
SOCIO_INDEX = "pct_welfare_15_64"


def main():
    logger.info("SWM Explorer. Starting Execution")
    Path("reports").mkdir(exist_ok=True)

    polygons = load_database()

    # --- Build all W matrices ---
    rook_w        = create_rook_swm(polygons)
    queen_w       = create_queen_swm(polygons)
    knn_w         = create_knn_swm(polygons)
    distance_w    = create_distance_swm(polygons, threshold=5000)
    socio_w       = create_socio_swm(polygons, knn_w, index_col=SOCIO_INDEX)

    # --- Visualize W structures ---
    for w, name in [
        (rook_w,     "rook"),
        (queen_w,    "queen"),
        (distance_w, "distance"),
        (socio_w,    "socioeconomic"),
    ]:
        fig = plot_swm_weighted(polygons, w, title=f"{name.capitalize()} W")
        fig.savefig(f"reports/swm_{name}.png", dpi=150, bbox_inches="tight")

    # --- Global Moran's I comparison table ---
    weights_dict = {
        "Rook":                    rook_w,
        "Queen":                   queen_w,
        "KNN (k=4)":               knn_w,
        "Distance Band (5km)":     distance_w,
        "Socio-Similarity (KNN)":  socio_w,
    }

    table = build_morans_table(polygons, weights_dict, variable=ANALYSIS_VARIABLE)
    print_morans_table(table, variable=ANALYSIS_VARIABLE)
    save_morans_table(table, variable=ANALYSIS_VARIABLE)

    # --- LISA maps per W ---
    for name, w in weights_dict.items():
        lisa = compute_local_morans(polygons, w, variable=ANALYSIS_VARIABLE)
        fig  = plot_lisa(polygons, lisa, title=f"LISA — {name}")
        fig.savefig(f"reports/lisa_{name.replace(' ', '_').lower()}.png", dpi=150, bbox_inches="tight")

    logger.info("---- End of Execution ----")


if __name__ == "__main__":
    main()


```


#### Future Implementations:

1. Run the code using CLI.
2. Docstring on all methods
3. Local Moran's I: Analysis and Mapping
4. Extend Analysis: Only calculate Local Moran's I when the Global makes sense:
```python

# on main.py
MORANS_MIN_MAGNITUDE = 0.15

for name, w in weights_dict.items():
    mi = compute_global_morans(polygons, w, variable=ANALYSIS_VARIABLE)
    significant = mi.p_sim < 0.05
    meaningful  = abs(mi.I) >= MORANS_MIN_MAGNITUDE

    if significant and meaningful:
        lisa = compute_local_morans(polygons, w, variable=ANALYSIS_VARIABLE)
        fig  = plot_lisa(polygons, lisa, title=f"LISA — {name}")
        fig.savefig(f"reports/lisa_{name.replace(' ', '_').lower()}.png", dpi=150, bbox_inches="tight")
    else:
        reason = []
        if not significant: reason.append(f"not significant (p={mi.p_sim:.3f})")
        if not meaningful:  reason.append(f"magnitude too low (I={mi.I:.4f})")
        logger.info(f"Skipping LISA for {name} — {' and '.join(reason)}")
```