-- table creation
CREATE TABLE IF NOT EXISTS stations (
    id CHAR(11) PRIMARY KEY NOT NULL,
    city TEXT NOT NULL
);

-- bulk loading
\COPY stations FROM 'output_data/stations.csv' WITH (FORMAT CSV);
