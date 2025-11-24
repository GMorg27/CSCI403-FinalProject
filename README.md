# CSCI 403 Final Project
`pip install -r requirements.txt`


## Input Datasets
- [MLB Game Data](https://www.kaggle.com/datasets/josephvm/mlb-game-data)
    - `games.csv`
        - ..., Date, Location, ...
        - Unique Location values manually entered into `input_data/cities.csv`.
- [Weather Data (US)](https://www.kaggle.com/datasets/nachiketkamod/weather-dataset-us)
    - `Weather Data (US).csv`
        - ID, DATE, ...
- Weather station data: `input_data/stations.txt`
    - ID, ..., state/province, city, ...


## Outputs
- CSV mapping weather station ID to city matching MLB game data
    - ID, city
