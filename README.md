# Taxi Trip Efficiency Analysis Project

## Introduction
This project is designed to analyze the operational efficiency and demand patterns of New York City taxi trips. Utilizing data from the NYC OpenData portal, the project comprises two primary ETL pipelines. These pipelines aim to derive insights into taxi trip durations, speeds, cost efficiency, and demand patterns that can help taxi companies, taxi drivers, and city planners in optimizing taxi operations mobility.

## Installation Instructions

### Recommended: Using Poetry
- Ensure GNU Make (gmake 3.82 or higher) is installed on your system.
- To initialize the project with Poetry, execute: `make init-poetry`.
- Alternatively, run `poetry install` directly to install dependencies.

### Alternative: Using virtualenv
- Install GNU Make (gmake 3.82 or higher) if not already installed.
- Install virtualenv: `pip install virtualenv`.
- Create a virtual environment: `virtualenv -p python3.12 env`.
- Activate the virtual environment: `source env/bin/activate`.
- Install dependencies: `pip install -r requirements.txt`.

## Why Polars?
The project uses the Polars library for data processing due to its high performance (it's a LOT faster than pandas and spark). It's API is nearly identical to Pandas (I have a lot of experience with Pandas), and frankly I just wanted to try something new.

## ETL Pipeline Descriptions

### ETL 1: Analyzing Trip Efficiency [efficiency.py](efficiency.py)

#### Overview
The first pipeline evaluates the efficiency of taxi trips by analyzing trip durations, speeds, and fare efficiencies. Insights derived from this analysis can help improve taxi service quality and operational strategies.

#### Insights
- Identifying efficient routes and times can optimize taxi operations.
- Fare efficiency analysis offers insights into pricing strategies.
- Trends in trip data can guide improvements in service and pricing.

#### Pipeline Steps
1. **Extract**: Fetch Yellow Taxi Trip data from the NYC OpenData portal or a local JSON fallback.
2. **Transform**:
   - Convert pickup and dropoff times to datetime.
   - Calculate trip durations and speeds.
   - Normalize numerical fields for consistency.
   - Compute fare efficiency metrics.
3. **Load**: Save the transformed data into `efficiency_taxi_data.csv` for further analysis.

#### Execution
Run the pipeline with:
- `poetry run python efficiency.py`
- For virtualenv setups: `python efficiency.py`

### ETL 2: Demand Pattern Analysis [demand_analysis.py](demand_analysis.py)

#### Overview
This pipeline focuses on uncovering taxi demand patterns across different times and locations, providing insights into peak demand hours and the influence of weekdays on taxi usage.

#### Insights
- Peak demand hours identification helps in fleet optimization.
- Analysis of weekday effects informs operational planning.
- Insights support urban planning and taxi driver strategies.

#### Pipeline Steps
1. **Extract**: Retrieve Yellow Taxi Trip Data in JSON format.
2. **Transform**:
   - Convert datetime fields.
   - Extract hour and weekday information.
   - Aggregate data by hour and weekday.
3. **Load**: Store aggregated data in `day_of_week_aggregation.csv` and `hourly_aggregation.csv`.

#### Execution
Run the pipeline with:
- `poetry run python demand_analysis.py`
- For virtualenv setups: `python demand_analysis.py`

## Output Files
- all files are stored in the `output` directory and are named as follows:
  - `efficiency_taxi_data.csv`
  - `day_of_week_aggregation.csv`
  - `hourly_aggregation.csv`
