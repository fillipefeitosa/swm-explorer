import logging
import sys
import matplotlib.pyplot as plt
from swm.io import load_database
from swm.weights import create_rook_swm, create_queen_swm
from swm.weights import create_knn_swm, create_distance_swm
from swm.weights import create_socio_swm
from swm.viz import plot_lisa, plot_swm_weighted


# 1. SETUP CONFIGURATION
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

def main():
    logger.info("SWM Explorer. Starting Execution")
    polygons = load_database()
    print(polygons.head())
    
    rook_w = create_rook_swm(polygons)
    queen_w = create_queen_swm(polygons)
    knn_w = create_knn_swm(polygons)
    distance_band_w = create_distance_swm(polygons, threshold=1000)
    
    
    
    # print(distance_band_w.weights)

    logger.info("---- Starting Socioeconomic Analisys ----")
    socioeconomic_w = create_socio_swm(polygons, knn_w, index_col="pct_welfare_15_64")
    # print(socioeconomic_w.weights)
    
    # Some Viz
    # Class 2: show the structure of each W
    fig = plot_swm_weighted(polygons, rook_w, title="Rook W")
    fig.savefig("reports/swm_rook.png", dpi=150, bbox_inches="tight")

    fig = plot_swm_weighted(polygons, distance_band_w, title="Distance W")
    fig.savefig("reports/swm_distance.png", dpi=150, bbox_inches="tight")

    fig = plot_swm_weighted(polygons, socioeconomic_w, title="Socioeconomic W — Similarity")
    fig.savefig("reports/swm_socio.png", dpi=150, bbox_inches="tight")

    logger.info("---- End of Execution ----")

if __name__ == "__main__":
    main()
