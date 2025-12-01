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

-- join query
SELECT w.date, s.city, w.temp_min, w.temp_max, w.precip, w.elevation, g.away_score, g.home_score, h.at_bats, h.hits
FROM STATIONS AS s
JOIN weather AS w ON w.station_id = s.id
JOIN games AS g ON g.date = w.date AND g.city = s.city
JOIN hitting AS h ON h.game_id = g.id
WHERE w.temp_min IS NOT NULL AND w.temp_max IS NOT NULL AND w.precip IS NOT NULL AND w.elevation IS NOT NULL;

-- average weather data
SELECT w.date, s.city, AVG(w.temp_min) AS temp_min, AVG(w.temp_max) AS temp_max, AVG((w.temp_min + w.temp_max) / 2) AS temp_mid,
    AVG(w.precip) AS precip, AVG(w.elevation) AS elevation
FROM weather AS w
JOIN stations AS s ON s.id = w.station_id
GROUP BY w.date, s.city;

-- join query with average weather data
WITH weather_avg AS (
    SELECT w.date, s.city, AVG(w.temp_min) AS temp_min, AVG(w.temp_max) AS temp_max, AVG((w.temp_min + w.temp_max) / 2) AS temp_mid,
        AVG(w.precip) AS precip, AVG(w.elevation) AS elevation
    FROM weather AS w
    JOIN stations AS s ON s.id = w.station_id
    GROUP BY w.date, s.city
)
SELECT w.date, w.city, w.temp_min, w.temp_max, w.temp_mid, w.precip, w.elevation, g.away_score, g.home_score, h.at_bats, h.hits, h.walks, h.strikeouts
FROM weather_avg AS w
JOIN games AS g ON g.date = w.date AND g.city = w.city
JOIN hitting AS h on h.game_id = g.id
WHERE w.temp_mid IS NOT NULL AND w.precip IS NOT NULL and w.elevation IS NOT NULL;

-- final join query
CREATE VIEW results AS (
    WITH weather_avg AS (
        SELECT w.date, s.city,
            AVG(w.temp_min) AS temp_min,
            AVG(w.temp_max) AS temp_max,
            AVG((w.temp_min + w.temp_max) / 2) AS temp_mid,
            AVG(w.precip)   AS precip,
            AVG(w.elevation) AS elevation
        FROM weather AS w
        JOIN stations AS s ON s.id = w.station_id
        GROUP BY w.date, s.city
    ),
    hitting_agg AS (
        SELECT game_id,
            SUM(at_bats)     AS at_bats,
            SUM(hits)        AS hits,
            SUM(walks)       AS walks,
            SUM(strikeouts)  AS strikeouts
        FROM hitting
        GROUP BY game_id
    )
    SELECT w.date, w.city,
        w.temp_min, w.temp_max, w.temp_mid, w.precip, w.elevation,
        g.away_score, g.home_score,
        h.at_bats, h.hits, h.walks, h.strikeouts
    FROM weather_avg w
    JOIN games g ON g.date = w.date AND g.city = w.city
    JOIN hitting_agg h ON h.game_id = g.id
    WHERE w.temp_mid IS NOT NULL
    AND w.precip IS NOT NULL
    AND w.elevation IS NOT NULL
);

-- copy results to csv
\COPY (SELECT * FROM results) TO 'output_data/results.csv' WITH (FORMAT CSV, HEADER);
