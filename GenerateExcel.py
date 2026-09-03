import pandas as pd
import os


BASE = "."
OUT_DIR = os.path.join(BASE, "output")
PRED_PATH = os.path.join(OUT_DIR, "predictions.csv")
DATA_PATH = os.path.join(BASE, "data", "BankChurners.csv")
EXCEL_PATH = os.path.join(OUT_DIR, "churn_prediction_report.xlsx")

pred_df = pd.read_csv(PRED_PATH)
raw_df = pd.read_csv(DATA_PATH)

report_df = raw_df.merge(pred_df, on="CLIENTNUM", how="left")

high_risk = report_df[report_df["churn_probability"] >= 0.7].sort_values(
    "churn_probability", ascending=False
)

summary = pd.DataFrame({
    "Metric": [
        "Total Customers",
        "Predicted Churn",
        "Predicted Churn Rate",
        "High Risk (>=0.7)",
        "High Risk %"
    ],
    "Value": [
        len(report_df),
        int((report_df["predicted_churn"] == 1).sum()),
        f"{(report_df['predicted_churn'] == 1).mean():.2%}",
        len(high_risk),
        f"{len(high_risk) / len(report_df):.2%}"
    ]
})

with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl") as writer:
    summary.to_excel(writer, sheet_name="Summary", index=False)
    high_risk.to_excel(writer, sheet_name="HighRisk", index=False)
    report_df.to_excel(writer, sheet_name="Predictions", index=False)

print(f"Report saved: {EXCEL_PATH}")