-- table creation
CREATE TABLE IF NOT EXISTS stations (
    id CHAR(11) PRIMARY KEY NOT NULL,
    city TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS weather (
    station_id CHAR(11) REFERENCES stations(id),
    date DATE NOT NULL,
    temp_min NUMERIC(4, 1),
    temp_max NUMERIC(4, 1),
    precip NUMERIC(5, 1),
    elevation NUMERIC(5, 1),
    PRIMARY KEY (station_id, date)
);

CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    away TEXT NOT NULL,
    home TEXT NOT NULL,
    date DATE NOT NULL,
    away_score INT,
    home_score INT,
    location TEXT
);

-- bulk loading
\COPY stations FROM 'output_data/stations.csv' WITH (FORMAT CSV, HEADER);
\COPY weather FROM 'output_data/weather.csv' WITH (FORMAT CSV, HEADER);
\COPY games FROM 'output_data/games.csv' WITH (FORMAT CSV, HEADER);
