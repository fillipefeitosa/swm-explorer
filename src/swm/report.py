import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)


def print_morans_table(df: pd.DataFrame, variable: str) -> None:
    """
    Prints the Moran's I comparison table to stdout in a readable format.

    Args:
        df:       DataFrame returned by build_morans_table.
        variable: Variable name analyzed, used in the header.
    """
    print()
    print("=" * 60)
    print(f"  Global Moran's I Comparison — {variable}")
    print("=" * 60)
    print(df.to_string(index=False))
    print("=" * 60)
    print()


def save_morans_table(
    df: pd.DataFrame, variable: str, output_dir: str = "reports"
) -> None:
    """
    Saves the Moran's I comparison table as a CSV file.

    Args:
        df:         DataFrame returned by build_morans_table.
        variable:   Variable name analyzed, used in the filename.
        output_dir: Directory to save the CSV. Created if it doesn't exist.
    """
    Path(output_dir).mkdir(exist_ok=True)
    filename = f"{output_dir}/morans_table_{variable}.csv"
    df.to_csv(filename, index=False)
    logger.info("Moran's I table saved to %s", filename)
