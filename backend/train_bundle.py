from pathlib import Path
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

ROOT = Path(__file__).resolve().parent.parent

FEATURES = ["Protocol", "Tot_Bwd_Pkts", "Flow_Pkts/s", "Flow_IAT_Min", "Fwd_IAT_Mean",
            "Fwd_Pkts/s", "SYN_Flag_Cnt", "RST_Flag_Cnt", "URG_Flag_Cnt", "ECE_Flag_Cnt",
            "Fwd_Seg_Size_Avg", "Subflow_Fwd_Pkts", "Subflow_Bwd_Pkts",
            "Subflow_Bwd_Byts", "Fwd_Act_Data_Pkts"]

df = pd.read_csv(ROOT / "data/processed.csv", usecols=FEATURES + ["Cat"])
X, y = df[FEATURES], df["Cat"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ("preprocess", MinMaxScaler()),
    ("model", HistGradientBoostingClassifier(max_iter=300, learning_rate=0.1,
                                             max_leaf_nodes=127, random_state=42)),
])
pipeline.fit(X_train, y_train)

pred = pipeline.predict(X_test)
print("Accuracy:", round(accuracy_score(y_test, pred) * 100, 2))
print("F1 (weighted):", round(f1_score(y_test, pred, average="weighted") * 100, 2))

bundle = {"pipeline": pipeline, "features": FEATURES,
          "task": "classification", "model_version": "1.0"}
(ROOT / "backend/models").mkdir(parents=True, exist_ok=True)
joblib.dump(bundle, ROOT / "backend/models/model_bundle.joblib")

X_test.head(1).to_csv(ROOT / "data/sample_inputs.csv", index=False)
print("Saved bundle and data/sample_inputs.csv")