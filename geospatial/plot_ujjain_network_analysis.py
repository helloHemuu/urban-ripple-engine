import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "data/processed/ujjain_network_analysis.csv"
OUTPUT_FILE = "data/processed/ujjain_network_centrality.png"

print("Loading network analysis results...")

data = pd.read_csv(INPUT_FILE)

data = data.head(10)

plt.figure(figsize=(12, 7))

plt.barh(
    data["node"],
    data["betweenness_centrality"]
)

plt.xlabel("Betweenness Centrality")
plt.ylabel("Network Nodes")

plt.title("Top 10 Ujjain Network Nodes by Betweenness Centrality")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)

plt.show()

print("\nGraph generated successfully!")
print("Saved at:", OUTPUT_FILE)