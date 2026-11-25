
import pandas as pd
import numpy as np
import joblib
import os

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load dataset
print("Loading student dataset...")

df = pd.read_csv("data/career_dataset.csv")

# Separate features and target
X = df.drop("career", axis=1)
y = df["career"]

# Split dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Dataset loaded successfully!")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# Create Random Forest model
print("\nTraining Random Forest model...")

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)

# Train model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nMODEL TRAINING COMPLETED!")
print("Test Accuracy:", round(accuracy * 100, 2), "%")

# Classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Create model directory
os.makedirs("model", exist_ok=True)

# Save trained model and feature names
joblib.dump(model, "model/career_model.joblib")
joblib.dump(list(X.columns), "model/features.joblib")

print("Model saved successfully!")

# Generate confusion matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(10, 7))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=model.classes_,
    yticklabels=model.classes_
)

plt.title("Career Prediction - Confusion Matrix")
plt.xlabel("Predicted Career")
plt.ylabel("Actual Career")
plt.xticks(rotation=30, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()

plt.savefig("model/confusion_matrix.png", dpi=300)
plt.close()

# Save feature importance chart
importance = pd.Series(
    model.feature_importances_,
    index=X.columns
).sort_values(ascending=True)

plt.figure(figsize=(9, 6))
importance.plot(kind="barh")
plt.title("Feature Importance - Random Forest")
plt.xlabel("Importance Score")
plt.tight_layout()

plt.savefig("model/feature_importance.png", dpi=300)
plt.close()

print("\nEvaluation charts saved successfully!")
print("Project model training finished!")
