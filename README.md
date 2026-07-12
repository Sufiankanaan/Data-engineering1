# NYC Taxi Data Pipeline

A hands-on data engineering project that ingests real NYC Yellow Taxi trip data
into a PostgreSQL database, containerized with Docker.

Built as part of **Module 1 (Containerization & Infrastructure)** of the
[Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
by DataTalksClub.

## Overview

This project reads a large compressed CSV of NYC taxi trips, processes it in
memory-efficient chunks, and loads it into a PostgreSQL database running in a
Docker container.

## Tech Stack

- **Python 3.13** — core language
- **pandas** — data processing
- **SQLAlchemy + psycopg** — database connection
- **PostgreSQL** — data storage (via Docker)
- **Docker** — containerization
- **uv** — dependency management
- **pytest** — testing

## Project Structure