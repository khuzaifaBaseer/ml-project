from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
FEATURES = ["Protocol", "Tot_Bwd_Pkts", "Flow_Pkts/s", "Flow_IAT_Min", "Fwd_IAT_Mean",
            "Fwd_Pkts/s", "SYN_Flag_Cnt", "RST_Flag_Cnt", "URG_Flag_Cnt", "ECE_Flag_Cnt",
            "Fwd_Seg_Size_Avg", "Subflow_Fwd_Pkts", "Subflow_Bwd_Pkts",
            "Subflow_Bwd_Byts", "Fwd_Act_Data_Pkts"]

df = pd.read_csv(ROOT / "data/processed.csv", usecols=FEATURES + ["Cat"])
# same split as train_bundle.py, so no training rows leak into the gate sample
_, test = train_test_split(df, test_size=0.2, random_state=42)

sample = pd.concat([g.sample(min(len(g), 1500), random_state=42)
                    for _, g in test.groupby("Cat")])
sample.to_csv(ROOT / "data/gate_test.csv", index=False)
print(sample["Cat"].value_counts())
print("Saved data/gate_test.csv:", len(sample), "rows")