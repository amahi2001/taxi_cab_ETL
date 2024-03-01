import json

import polars as pl
import requests
from requests.exceptions import ReadTimeout

if __name__ == "__main__":
    #! Extract the data from API or local file
    URL = "https://data.cityofnewyork.us/resource/t29m-gskq.json"
    try:
        response = requests.get(URL, timeout=30)
        data = response.json()
    except ReadTimeout:
        with open("taxi.json", "r", encoding="utf-8") as file:
            data = json.load(file)

    #! Loading data into a polars dataframe
    df = pl.DataFrame(data)

    #! Transforming data
    # Convert datetime strings to datetime objects and calculate trip duration in hours
    df = df.with_columns(
        [
            # Converting pickup time
            pl.col("tpep_pickup_datetime")
            .str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S%.f")
            .alias("pickup_datetime"),
            # converting dropoff time
            pl.col("tpep_dropoff_datetime")
            .str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S%.f")
            .alias("dropoff_datetime"),
        ]
    )

    # Calculate trip duration in hours
    df = df.with_columns(
        (
            (pl.col("dropoff_datetime") - pl.col("pickup_datetime")).dt.total_seconds()
            / 3600
        ).alias("trip_duration_hours")
    )

    # Calculate speed in miles per hour
    df = df.with_columns(
        (pl.col("trip_distance").cast(float) / pl.col("trip_duration_hours")).alias(
            "speed_mph"
        )
    )

    # Ensure fare_amount is a float for calculations
    df = df.with_columns(pl.col("fare_amount").cast(float))

    # Calculate cost efficiency (fare per mile)
    df = df.with_columns(
        (pl.col("fare_amount") / pl.col("trip_distance").cast(float)).alias(
            "cost_per_mile"
        )
    )

    #! Load data to csv
    df.write_csv("outputs/efficiency_taxi_data.csv")
