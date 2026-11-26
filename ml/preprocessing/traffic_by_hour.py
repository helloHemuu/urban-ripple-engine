import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "data/processed/metro_traffic_cleaned.csv"
OUTPUT_FILE = "data/processed/traffic_by_hour.png"

print("Loading traffic dataset...")

traffic = pd.read_csv(INPUT_FILE)

print("Calculating average traffic by hour...")

hourly_traffic = traffic.groupby("hour")["traffic_volume"].mean()

plt.figure(figsize=(10, 6))

plt.plot(hourly_traffic.index, hourly_traffic.values, marker="o")

plt.title("Average Traffic Volume by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Average Traffic Volume")
plt.xticks(range(0, 24))
plt.grid(True)

plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)

plt.show()

print("\nGraph saved successfully!")
print("Saved at:", OUTPUT_FILE)