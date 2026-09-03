import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
import matplotlib.pyplot as plt


BASE = "."
DATA_PATH = os.path.join(BASE, "data", "BankChurners.csv")
OUT_DIR = os.path.join(BASE, "output")

os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

df = df.loc[:, ~df.columns.str.startswith("Naive_Bayes_")]
df = df.drop(columns=["CLIENTNUM"], errors="ignore")

y = df["Attrition_Flag"].map({
    "Attrited Customer": 1,
    "Existing Customer": 0
})

X = df.drop(columns=["Attrition_Flag"])
feature_cols = X.columns.tolist()

encoders = {}
for col in X.select_dtypes(include=["object", "category"]).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    encoders[col] = le

X = X.astype(float)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(X_train, y_train)

preds = model.predict(X_test)
probs = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, preds))
auc_score = roc_auc_score(y_test, probs)
print("ROC AUC:", auc_score)

with open(os.path.join(OUT_DIR, "metrics.txt"), "w", encoding="utf-8") as f:
    f.write(f"ROC-AUC: {auc_score:.3f}\n")

plt.figure(figsize=(8, 6))
fpr, tpr, _ = roc_curve(y_test, probs)
plt.plot(fpr, tpr, label=f"ROC AUC = {auc_score:.3f}")
plt.plot([0, 1], [0, 1], "--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "roc_curve.png"))
plt.close()

importance = model.feature_importances_
fi = pd.DataFrame({
    "feature": feature_cols,
    "importance": importance
}).sort_values("importance", ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(fi["feature"][:20][::-1], fi["importance"][:20][::-1])
plt.title("Top 20 Feature Importance")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "feature_importance.png"))
plt.close()

fi.to_csv(os.path.join(OUT_DIR, "feature_importance.csv"), index=False, encoding="utf-8-sig")

joblib.dump(encoders, os.path.join(OUT_DIR, "encoders.pkl"))
joblib.dump(feature_cols, os.path.join(OUT_DIR, "feature_cols.pkl"))
joblib.dump(model, os.path.join(OUT_DIR, "rf_model.pkl"))

df.to_csv(os.path.join(OUT_DIR, "credit_card_customers_processed.csv"), index=False, encoding="utf-8-sig")

print("Done.")