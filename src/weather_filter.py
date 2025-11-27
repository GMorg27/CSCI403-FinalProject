import datetime

import pandas as pd

INPUT_PATH = "input_data/raw/weather.csv"
STATIONS_PATH = "output_data/stations.csv"
OUTPUT_PATH = "output_data/weather.csv"
CHUNK_SIZE = 100000

MIN_DATE = datetime.datetime(2016, 1, 1)

# store a set of all used station IDs
stations_df = pd.read_csv(STATIONS_PATH)
station_set = set(stations_df["id"])

chunk_reader = pd.read_csv(
    INPUT_PATH,
    chunksize=CHUNK_SIZE,
    usecols=["ID", "DATE", "TMAX", "TMIN", "PRCP", "Elevation"],
    parse_dates=["DATE"]
)

# filter and clean data
chunks_read = 0
first = True
for chunk in chunk_reader:
    filtered_df = chunk[chunk["DATE"] >= MIN_DATE]
    filtered_df = filtered_df[filtered_df["ID"].isin(station_set)]

    # convert from tenths of degrees to degrees celsius
    filtered_df["TMAX"] /= 10
    filtered_df["TMIN"] /= 10

    # write desired columns to csv
    filtered_df.rename(
        columns={
            "ID": "station_id",
            "DATE": "date",
            "TMAX": "temp_max",
            "TMIN": "temp_min",
            "PRCP": "precip",
            "Elevation": "elevation"
        },
        inplace=True
    )
    filtered_df.to_csv(
        OUTPUT_PATH,
        mode='w' if first else 'a',
        header=first,
        index=False
    )

    first = False
    chunks_read += CHUNK_SIZE
    print(chunks_read)
