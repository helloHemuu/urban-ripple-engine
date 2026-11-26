import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "data/processed/road_impact_report.csv"
OUTPUT_FILE = "data/processed/road_impact_comparison.png"

print("Loading road impact report...")

df = pd.read_csv(INPUT_FILE)
report = df.iloc[0]

original_distance = report["original_distance_m"]
alternate_distance = report["alternate_distance_m"]
increase = report["increase_percent"]
severity = report["impact_severity"]

print("Creating comparison chart...")

labels = ["Original Route", "Alternate Route"]
distances = [original_distance, alternate_distance]

plt.figure(figsize=(9, 6))

bars = plt.bar(labels, distances)

plt.title("Urban Ripple Engine - Road Impact Analysis")
plt.ylabel("Route Distance (meters)")
plt.xlabel("Route Type")

for bar, distance in zip(bars, distances):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{distance:.2f} m",
        ha="center",
        va="bottom"
    )

plt.figtext(
    0.5,
    0.01,
    f"Distance Increase: {increase:.2f}% | Impact Severity: {severity}",
    ha="center",
    fontsize=10
)

plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")

print("\nVisualization completed!")
print("Saved at:", OUTPUT_FILE)

plt.show()