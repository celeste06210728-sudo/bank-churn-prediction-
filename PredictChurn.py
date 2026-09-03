import pandas as pd
import numpy as np
import os
import joblib


BASE = "."
DATA_PATH = os.path.join(BASE, "data", "BankChurners.csv")
OUT_DIR = os.path.join(BASE, "output")


df = pd.read_csv(DATA_PATH)

feature_cols = joblib.load(os.path.join(OUT_DIR, "feature_cols.pkl"))
encoders = joblib.load(os.path.join(OUT_DIR, "encoders.pkl"))
model = joblib.load(os.path.join(OUT_DIR, "rf_model.pkl"))

cat_cols = [c for c in feature_cols if c in df.select_dtypes(include=["object", "category"]).columns]
num_cols = [c for c in feature_cols if c in df.select_dtypes(include=[np.number]).columns]

X = df[feature_cols].copy()

for col in cat_cols:
    le = encoders[col]
    X[col] = X[col].astype(str).apply(
        lambda v: le.transform([v])[0] if v in le.classes_ else -1
    )

X[num_cols] = X[num_cols].astype(float)

preds = model.predict(X)
probs = model.predict_proba(X)[:, 1]

result = pd.DataFrame({
    "CLIENTNUM": df["CLIENTNUM"],
    "predicted_churn": preds,
    "churn_probability": np.round(probs, 4)
})

if "Attrition_Flag" in df.columns:
    result["actual_churn"] = df["Attrition_Flag"].map({
        "Attrited Customer": 1,
        "Existing Customer": 0
    })

OUT_PATH = os.path.join(OUT_DIR, "predictions.csv")
result.to_csv(OUT_PATH, index=False, encoding="utf-8-sig")

print(f"Predictions saved: {OUT_PATH}")
print(f"Total: {len(result)}, Churn predicted: {(result['predicted_churn'] == 1).sum()}")