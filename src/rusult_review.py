# --- 1. Import libraries ---
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- 2. Load dataset ---
df = pd.read_csv('output_data/results.csv')

# --- 3. Feature engineering ---
# Total runs in the game
df['total_runs'] = df['away_score'] + df['home_score']

# Temperature variability
df['temp_range'] = df['temp_max'] - df['temp_min']

# Precipitation flag (rain/snow)
df['precip_flag'] = df['precip'].apply(lambda x: 1 if x > 0 else 0)

# Batting efficiency metrics
df['hits_per_ab'] = df['hits'] / df['at_bats']
df['walk_rate'] = df['walks'] / df['at_bats']
df['strikeout_rate'] = df['strikeouts'] / df['at_bats']

# --- 4. Compute correlations on numeric columns only ---
numeric_cols = df.select_dtypes(include=['float64', 'int64'])
corr = numeric_cols.corr()

print("Correlation matrix:")
print(corr)

# --- 5. Visualize correlation heatmap ---
plt.figure(figsize=(12,8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', center=0)
plt.title("Correlation Heatmap")
plt.show()

# --- 6. Scatterplots for key relationships ---

# Total runs vs average temperature
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='temp_mid', y='total_runs', hue='precip_flag', palette='Set1')
plt.title("Total Runs vs. Temperature (Precipitation Highlighted)")
plt.xlabel("Average Temperature (°C)")
plt.ylabel("Total Runs")
plt.show()

# Batting efficiency (hits per at-bat) vs temperature
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='temp_mid', y='hits_per_ab', hue='precip_flag', palette='Set2')
plt.title("Batting Efficiency vs. Temperature")
plt.xlabel("Average Temperature (°C)")
plt.ylabel("Hits per At-Bat")
plt.show()

# Elevation vs total runs
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='elevation', y='total_runs')
plt.title("Total Runs vs. Stadium Elevation")
plt.xlabel("Elevation (meters)")
plt.ylabel("Total Runs")
plt.show()
