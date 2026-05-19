import logging
import sys
from pathlib import Path
from swm.io import load_database
from swm.weights import create_rook_swm, create_queen_swm
from swm.weights import create_knn_swm, create_distance_swm
from swm.weights import create_socio_swm
from swm.viz import plot_swm_weighted
from swm.analysis import build_morans_table
from swm.report import print_morans_table, save_morans_table

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

ANALYSIS_VARIABLE = "pct_children_migration_background"
SOCIO_INDEX = "pct_welfare_15_64"
DISTANCE_THRESHOLD = 5000


def main():
    logger.info("SWM Explorer. Starting Execution")
    Path("reports").mkdir(exist_ok=True)

    polygons = load_database()

    # --- Build all W matrices ---
    rook_w = create_rook_swm(polygons)
    queen_w = create_queen_swm(polygons)
    knn_w = create_knn_swm(polygons)
    distance_w = create_distance_swm(polygons, threshold=DISTANCE_THRESHOLD)
    socio_w = create_socio_swm(polygons, knn_w, index_col=SOCIO_INDEX)

    # --- Visualize W structures ---
    for w, name in [
        (rook_w, "rook"),
        (queen_w, "queen"),
        (distance_w, "distance"),
        (socio_w, "socioeconomic"),
    ]:
        fig = plot_swm_weighted(polygons, w, title=f"{name.capitalize()} W")
        fig.savefig(f"reports/swm_{name}.png", dpi=150, bbox_inches="tight")

    # --- Global Moran's I comparison table ---
    weights_dict = {
        "Rook": rook_w,
        "Queen": queen_w,
        "KNN (k=4)": knn_w,
        f"Distance Band ({DISTANCE_THRESHOLD})": distance_w,
        "Socio-Similarity (KNN)": socio_w,
    }

    table = build_morans_table(polygons, weights_dict, variable=ANALYSIS_VARIABLE)
    print_morans_table(table, variable=ANALYSIS_VARIABLE)
    save_morans_table(table, variable=ANALYSIS_VARIABLE)


if __name__ == "__main__":
    main()
