import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

INPUT_PATH = "output_data/results.csv"
REMOVE_ELEVATION_OUTLIERS = False

df = pd.read_csv(
    INPUT_PATH,
    usecols=["temp_mid", "precip", "elevation", "score", "bat_avg"]
)

# remove outliers
if (REMOVE_ELEVATION_OUTLIERS):
    Q1 = df["elevation"].quantile(0.25)
    Q3 = df["elevation"].quantile(0.75)
    IQR = Q3 - Q1

    upper_bound = Q3 + 1.5 * IQR # define outliers as 1.5 IQR above Q3
    df = df[df["elevation"] <= upper_bound]

# compute correlations and p-values on numeric columns only
numeric_cols = df.select_dtypes(include=["float64", "int64"])
corr = numeric_cols.corr()

# compute p-values
pval_matrix = pd.DataFrame(np.zeros((len(numeric_cols.columns), len(numeric_cols.columns))),
                           columns=numeric_cols.columns,
                           index=numeric_cols.columns)
for col1 in numeric_cols.columns:
    for col2 in numeric_cols.columns:
        r, p = pearsonr(df[col1], df[col2])
        pval_matrix.loc[col1, col2] = p
sig_mask = pval_matrix < 0.05 # mask non-significant cells

# correlation heatmap
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, mask=~sig_mask)
plt.title("Correlation Heatmap (p < 0.05)")
plt.show()

# score vs temperature
plt.figure(figsize=(8,6))
sns.regplot(data=df, x="temp_mid", y="score", line_kws={"color": "red"})
plt.title("Game Score vs. Temperature")
plt.xlabel("Daily Mean Temperature (°C)")
plt.ylabel("Total Runs")
plt.show()

# score vs precipitation
plt.figure(figsize=(8,6))
sns.regplot(data=df, x="precip", y="score", line_kws={"color": "red"})
plt.title("Game Score vs. Precipitation")
plt.xlabel("Precipitation (millimeters)")
plt.ylabel("Total Runs")
plt.show()

# score vs elevation
plt.figure(figsize=(8,6))
sns.regplot(data=df, x="elevation", y="score", line_kws={"color": "red"})
plt.title("Game Score vs. Stadium Elevation")
plt.xlabel("Elevation (meters)")
plt.ylabel("Total Runs")
plt.show()

# batting average vs temperature
plt.figure(figsize=(8,6))
sns.regplot(data=df, x="temp_mid", y="bat_avg", line_kws={"color": "red"})
plt.title("Game Batting Average vs. Temperature")
plt.xlabel("Daily Mean Temperature (°C)")
plt.ylabel("Batting Average")
plt.show()

# batting average vs precipitation
plt.figure(figsize=(8,6))
sns.regplot(data=df, x="precip", y="bat_avg", line_kws={"color": "red"})
plt.title("Game Batting Average vs. Precipitation")
plt.xlabel("Precipitation (millimeters)")
plt.ylabel("Batting Average")
plt.show()

# batting average vs elevation
plt.figure(figsize=(8,6))
sns.regplot(data=df, x="elevation", y="bat_avg", line_kws={"color": "red"})
plt.title("Game Batting Average vs. Stadium Elevation")
plt.xlabel("Elevation (meters)")
plt.ylabel("Batting Average")
plt.show()
