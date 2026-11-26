import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "data/processed/metro_traffic_cleaned.csv"
OUTPUT_FILE = "data/processed/traffic_by_day.png"

print("Loading traffic dataset...")

traffic = pd.read_csv(INPUT_FILE)

print("Calculating average traffic by day...")

daily_traffic = traffic.groupby("day_of_week")["traffic_volume"].mean()

day_names = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

plt.figure(figsize=(10, 6))

plt.bar(day_names, daily_traffic.values)

plt.title("Average Traffic Volume by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Average Traffic Volume")

plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)
plt.show()

print("\nGraph saved successfully!")
print("Location:", OUTPUT_FILE)