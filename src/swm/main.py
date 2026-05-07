import logging
import sys
from swm.io import load_database
from swm.weights import create_rook_swm, create_queen_swm
from swm.weights import create_knn_swm, create_distance_swm
from swm.weights import create_socio_swm

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
    distance_band_w = create_distance_swm(polygons)
    
    
    
    print(distance_band_w.weights)

    logger.info("---- Starting Socioeconomic Analisys ----")
    socioeconomic_w = create_socio_swm(polygons, knn_w, index_col="pct_welfare_15_64")
    print(socioeconomic_w.weights)
    
    logger.info("---- End of Execution ----")

if __name__ == "__main__":
    main()
