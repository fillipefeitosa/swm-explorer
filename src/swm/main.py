import logging
import sys
from swm.io import load_database
from weights import create_rook_swm, create_queen_swm

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

    print(queen_w.weights)

    logger.info("---- End of Execution ----")

if __name__ == "__main__":
    main()
