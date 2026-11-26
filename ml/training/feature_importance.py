import joblib
import pandas as pd

MODEL_FILE = "ml/training/traffic_model.pkl"

print("Loading trained model...")

model = joblib.load(MODEL_FILE)

# Get preprocessing and trained Random Forest
preprocessor = model.named_steps["preprocessor"]
regressor = model.named_steps["regressor"]

# Get feature names after preprocessing
feature_names = preprocessor.get_feature_names_out()

# Get feature importance scores
importance_scores = regressor.feature_importances_

# Create DataFrame
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance_scores
})

# Sort by importance
importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance Results:")
print(importance_df.to_string(index=False))

# Save results
importance_df.to_csv(
    "data/processed/feature_importance.csv",
    index=False
)

print("\nFeature importance analysis completed!")
print("Results saved to data/processed/feature_importance.csv")