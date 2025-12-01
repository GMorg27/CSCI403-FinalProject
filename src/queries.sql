-- table creation
CREATE TABLE IF NOT EXISTS stations (
    id CHAR(11) PRIMARY KEY NOT NULL,
    city TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS weather (
    station_id CHAR(11) REFERENCES stations(id),
    date DATE NOT NULL,
    temp_max NUMERIC(4, 1),
    temp_min NUMERIC(4, 1),
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
    city TEXT
);
CREATE TABLE IF NOT EXISTS hitting (
    at_bats INT NOT NULL,
    hits INT NOT NULL,
    walks INT NOT NULL,
    strikeouts INT NOT NULL,
    game_id INT NOT NULL,
    team VARCHAR(3) NOT NULL,
    PRIMARY KEY (game_id, team)
);

-- bulk loading
\COPY stations FROM 'output_data/stations.csv' WITH (FORMAT CSV, HEADER);
\COPY weather FROM 'output_data/weather.csv' WITH (FORMAT CSV, HEADER);
\COPY games FROM 'output_data/games.csv' WITH (FORMAT CSV, HEADER);
\COPY hitting FROM 'output_data/hitting.csv' WITH (FORMAT CSV, HEADER);

-- indexing
-- TODO

-- join
SELECT w.date, s.city, w.temp_min, w.temp_max, w.precip, w.elevation, g.away_score, g.home_score, h.at_bats, h.hits
FROM STATIONS AS s
JOIN weather AS w ON w.station_id = s.id
JOIN games AS g ON g.city = s.city AND g.date = w.date
JOIN hitting AS h ON h.game_id = g.id
WHERE w.temp_min IS NOT NULL AND w.temp_max IS NOT NULL;
