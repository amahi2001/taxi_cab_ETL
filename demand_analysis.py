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

    # Loading data into a polars dataframe
    df = pl.DataFrame(data)

    # Convert datetime columns to datetime type
    df = df.with_columns(
        [
            pl.col("tpep_pickup_datetime")
            .str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S%.f")
            .alias("pickup_datetime"),
            pl.col("tpep_dropoff_datetime")
            .str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S%.f")
            .alias("dropoff_datetime"),
        ]
    )

    # Extract day of week and hour from pickup datetime
    df = df.with_columns(
        [
            pl.col("pickup_datetime").dt.hour().alias("pickup_hour"),
            pl.col("pickup_datetime").dt.weekday().alias("pickup_weekday"),
        ]
    )

    # Aggregate data by pickup hour
    hourly_aggregation = df.group_by("pickup_hour").agg([pl.len().alias("trip_count")])

    # Aggregate data by day of the week
    day_of_week_aggregation = df.group_by("pickup_weekday").agg(
        [pl.len().alias("trip_count")]
    )

    # load both aggregations to csv
    hourly_aggregation.write_csv("outputs/hourly_aggregation.csv")
    day_of_week_aggregation.write_csv("outputs/day_of_week_aggregation.csv")
