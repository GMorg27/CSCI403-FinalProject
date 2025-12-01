import pandas as pd
import os
import csv

INPUT_PATH = "input_data/games.csv"
OUTPUT_PATH = "output_data/games.csv"

# TODO: Update this list with the actual features you want to keep
FEATURES_TO_KEEP = [
    'Game', 
    'away',
    'home',
    'Date',
    'away-score',
    'home-score',
    'Location'
]

def filter_games():
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    try:
        df = pd.read_csv(
            INPUT_PATH,
            engine="python",
            quoting=csv.QUOTE_MINIMAL
        )
        
        # Filter columns, keeping only those that exist in the dataframe
        available_features = [f for f in FEATURES_TO_KEEP if f in df.columns]
        missing_features = set(FEATURES_TO_KEEP) - set(available_features)
        
        if missing_features:
            print(f"Warning: The following features were not found in the input file: {missing_features}")
        
        df_filtered = df[available_features]
        
        df_filtered.to_csv(OUTPUT_PATH, index=False)
        print(f"Successfully filtered data. Saved to {OUTPUT_PATH}")
        print(f"Columns kept: {available_features}")
        
    except FileNotFoundError:
        print(f"Error: Input file not found at {INPUT_PATH}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    filter_games()

