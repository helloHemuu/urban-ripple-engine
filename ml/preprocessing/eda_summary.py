import pandas as pd

INPUT_FILE = "data/processed/metro_traffic_cleaned.csv"
OUTPUT_FILE = "data/processed/eda_summary.txt"

print("Loading traffic dataset...")

traffic = pd.read_csv(INPUT_FILE)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

    file.write("URBAN RIPPLE ENGINE - TRAFFIC DATA EDA REPORT\n")
    file.write("=" * 50 + "\n\n")

    file.write("Dataset Information\n")
    file.write("-" * 30 + "\n")

    file.write(f"Total Rows: {traffic.shape[0]}\n")
    file.write(f"Total Columns: {traffic.shape[1]}\n\n")

    file.write("Traffic Volume Statistics\n")
    file.write("-" * 30 + "\n")

    file.write(str(traffic["traffic_volume"].describe()))
    file.write("\n\n")

    file.write("Average Traffic by Hour\n")
    file.write("-" * 30 + "\n")

    hourly = traffic.groupby("hour")["traffic_volume"].mean()
    file.write(str(hourly))
    file.write("\n\n")

    file.write("Average Traffic by Day\n")
    file.write("-" * 30 + "\n")

    daily = traffic.groupby("day_of_week")["traffic_volume"].mean()
    file.write(str(daily))
    file.write("\n\n")

    file.write("Missing Values\n")
    file.write("-" * 30 + "\n")

    file.write(str(traffic.isnull().sum()))

print("\nEDA report created successfully!")
print("Saved at:", OUTPUT_FILE)