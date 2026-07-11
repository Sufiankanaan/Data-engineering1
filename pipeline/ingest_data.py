"""
Ingest NYC yellow taxi trip data into a PostgreSQL database.

Reads a compressed CSV in chunks and loads it into a Postgres table.
Database credentials are read from environment variables.

Usage:
    python ingest_data.py
"""

import os
import logging

import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# --- Configuration ---
DATA_URL = (
    "https://github.com/DataTalksClub/nyc-tlc-data/releases/"
    "download/yellow/yellow_tripdata_2021-01.csv.gz"
)
TABLE_NAME = "yellow_taxi_data"
CHUNK_SIZE = 100_000

DTYPES = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
}
PARSE_DATES = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]


def get_engine():
    """Build a SQLAlchemy engine from environment variables."""
    user = os.getenv("POSTGRES_USER", "root")
    password = os.getenv("POSTGRES_PASSWORD", "root")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "ny_taxi")
    url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)


def ingest(engine) -> None:
    """Read the CSV in chunks and write each chunk to Postgres."""
    df_iter = pd.read_csv(
        DATA_URL,
        dtype=DTYPES,
        parse_dates=PARSE_DATES,
        iterator=True,
        chunksize=CHUNK_SIZE,
    )

    total_rows = 0
    for i, chunk in enumerate(df_iter):
        if_exists = "replace" if i == 0 else "append"
        chunk.to_sql(name=TABLE_NAME, con=engine, if_exists=if_exists, index=False)
        total_rows += len(chunk)
        logger.info("Inserted chunk %s (%s rows so far)", i + 1, total_rows)

    logger.info("Done. Loaded %s rows into '%s'.", total_rows, TABLE_NAME)


def main() -> None:
    logger.info("Connecting to database...")
    engine = get_engine()
    logger.info("Starting ingestion from %s", DATA_URL)
    ingest(engine)


if __name__ == "__main__":
    main()