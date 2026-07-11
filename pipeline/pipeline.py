"""
Simple data pipeline: generates trip data for a given month
and saves it as a Parquet file.

Usage:
    python pipeline.py <month>
Example:
    python pipeline.py 10
"""

import sys
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("data/output")


def parse_month(args: list[str]) -> int:
    """Read and validate the month number from command-line arguments."""
    if len(args) < 2:
        logger.error("Missing argument: month number is required.")
        logger.info("Example: python pipeline.py 10")
        sys.exit(1)

    try:
        month = int(args[1])
    except ValueError:
        logger.error("Month must be a number between 1 and 12.")
        sys.exit(1)

    if not 1 <= month <= 12:
        logger.error("Month must be between 1 and 12, got: %s", month)
        sys.exit(1)

    return month


def extract() -> pd.DataFrame:
    """Extract raw trip data. (Placeholder for a real data source.)"""
    return pd.DataFrame({
        "day": [1, 2],
        "num_passengers": [3, 4],
    })


def transform(df: pd.DataFrame, month: int) -> pd.DataFrame:
    """Add the month column to the raw data."""
    df = df.copy()
    df["month"] = month
    return df


def load(df: pd.DataFrame, month: int) -> Path:
    """Save the processed data as a Parquet file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"output_{month}.parquet"
    df.to_parquet(output_path)
    return output_path


def main() -> None:
    month = parse_month(sys.argv)
    logger.info("Running pipeline for month %s", month)

    df = extract()
    df = transform(df, month)
    output_path = load(df, month)

    logger.info("Pipeline finished. Saved to %s", output_path)
    logger.info("\n%s", df.head())


if __name__ == "__main__":
    main()