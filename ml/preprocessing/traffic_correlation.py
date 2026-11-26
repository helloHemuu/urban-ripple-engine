import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "data/processed/metro_traffic_cleaned.csv"
OUTPUT_FILE = "data/processed/traffic_correlation.png"

print("Loading traffic dataset...")

traffic = pd.read_csv(INPUT_FILE)

print("Calculating correlations...")

numeric_data = traffic.select_dtypes(include="number")

correlation = numeric_data.corr()

print("\nCorrelation with Traffic Volume:")
print(correlation["traffic_volume"].sort_values(ascending=False))

plt.figure(figsize=(10, 8))

plt.imshow(correlation, interpolation="nearest", aspect="auto")

plt.colorbar()

plt.xticks(
    range(len(correlation.columns)),
    correlation.columns,
    rotation=90
)

plt.yticks(
    range(len(correlation.columns)),
    correlation.columns
)

plt.title("Traffic Dataset Correlation Matrix")

plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)

plt.show()

print("\nCorrelation graph saved successfully!")
print("Location:", OUTPUT_FILE)