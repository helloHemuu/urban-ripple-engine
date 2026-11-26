import pandas as pd
import matplotlib.pyplot as plt

FILE_PATH = "data/processed/feature_importance.csv"
OUTPUT_FILE = "data/processed/feature_importance.png"

print("Loading feature importance data...")

data = pd.read_csv(FILE_PATH)

# Select top 10 features
top_features = data.head(10).sort_values(
    by="Importance",
    ascending=True
)

# Create horizontal bar chart
plt.figure(figsize=(10, 6))

plt.barh(
    top_features["Feature"],
    top_features["Importance"]
)

plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.title("Traffic Prediction - Feature Importance")

plt.tight_layout()

# Save graph
plt.savefig(OUTPUT_FILE, dpi=300)

plt.show()

print("\nGraph saved successfully!")
print("Location:", OUTPUT_FILE)