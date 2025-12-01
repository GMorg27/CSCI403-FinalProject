import pandas as pd

INPUT_PATH = "input_data/raw/hitters.csv"
OUTPUT_PATH = "output_data/hitting.csv"

df = pd.read_csv(
    INPUT_PATH,
    usecols=["Hitters", "AB", "H", "BB", "K", "Game", "Team"]
)

# filter and clean data
df = df[df["Hitters"] == "TEAM"]
df = df.drop("Hitters", axis=1)
df.drop_duplicates(
    subset=["Game", "Team"],
    keep="first",
    inplace=True
)
df.rename(
    columns={
        "AB": "at_bats",
        "H": "hits",
        "BB": "walks",
        "K": "strikeouts",
        "Game": "game_id",
        "Team": "team"
    },
    inplace=True
)
df.to_csv(OUTPUT_PATH, header=True, index=False)
