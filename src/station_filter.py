import csv
from collections import defaultdict

INPUT_PATH = "input_data/stations.txt"
CITIES_PATH = "input_data/cities.csv"
OUTPUT_PATH = "output_data/stations.csv"

# txt metadata
ID_PREFIXES = ["CA", "US"]
COLUMN_LENS = [11, 8, 9, 6, 2, 30]

# create dict of cities in each state/province
city_lookup = defaultdict(list)
with open(CITIES_PATH, "r", newline='', encoding="utf-8") as cities_csv:
    reader = csv.reader(cities_csv)
    for row in reader:
        if not row:
            continue

        city = row[0].strip()
        state = row[1].strip()
        city_lookup[state].append(city)

# convert txt to filtered and cleaned csv
output_data = []
with open(INPUT_PATH, "r", newline='', encoding="utf-8") as input_txt:
    for line in input_txt:
        # filter out unused country IDs
        prefix = line[:2]
        if prefix not in ID_PREFIXES:
            continue

        station_id = line[:COLUMN_LENS[0]]
        
        # skip lat/lon data
        skip_index = sum(COLUMN_LENS[:4]) + 4 # include space delimiters
        line = line[skip_index:]

        state = line[:2]
        city_raw = line[3:(2 + COLUMN_LENS[5])].strip()

        # filter and clean city names
        city = None
        city_candidates = city_lookup.get(state, [])
        for candidate in city_candidates:
            if candidate.lower() in city_raw.lower():
                city = candidate
                break

        if city:
            output_data.append([station_id, city])

# write (station id, city) rows to csv
with open(OUTPUT_PATH, "w", newline='', encoding="utf-8") as output_csv:
    writer = csv.writer(output_csv)
    writer.writerows(output_data)
