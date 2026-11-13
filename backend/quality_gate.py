import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import recall_score

ROOT = Path(__file__).resolve().parent.parent
MIN_RECALL = float(sys.argv[1]) if len(sys.argv) > 1 else 0.60

# identifiers that let a model separate classes without learning attack behaviour
FORBIDDEN = {"Src_Port", "Dst_Port", "Src_IP", "Dst_IP", "Flow_ID", "Timestamp"}

bundle = joblib.load(ROOT / "backend/models/model_bundle.joblib")
model, features = bundle["pipeline"], bundle["features"]
data = pd.read_csv(ROOT / "data/gate_test.csv")

failures = []

# Gate 1: leakage check
leaky = sorted(FORBIDDEN.intersection(features))
if leaky:
    failures.append(f"Leaky identifier features in model: {leaky}")

# Gate 2: per-class recall check
pred = model.predict(data[features])
classes = list(model.classes_)
recalls = recall_score(data["Cat"], pred, labels=classes, average=None)
report = {c: round(float(r), 4) for c, r in zip(classes, recalls)}

print(f"Per-class recall (threshold {MIN_RECALL:.2f}):")
for c, r in report.items():
    status = "PASS" if r >= MIN_RECALL else "FAIL"
    print(f"  {c:20s} {r:.4f}  {status}")
    if r < MIN_RECALL:
        failures.append(f"Recall for {c} is {r:.4f} < {MIN_RECALL:.2f}")

(ROOT / "backend/gate_report.json").write_text(
    json.dumps({"threshold": MIN_RECALL, "recall": report,
                "worst_class": min(report, key=report.get),
                "failures": failures}, indent=2), encoding="utf-8")

if failures:
    print("\nQUALITY GATE: FAILED")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print("\nQUALITY GATE: PASSED")