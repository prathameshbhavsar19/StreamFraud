import os
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

# 1. Compute the path to the CSV inside your repo:
#    __file__ is .../StreamFraud/app/evaluate_model.py
script_dir   = os.path.dirname(os.path.abspath(__file__))  # .../StreamFraud/app
project_root = os.path.dirname(script_dir)                 # .../StreamFraud
csv_path     = os.path.join(project_root, "data", "creditcard.csv")

print(f"Loading data from: {csv_path}")  # debug

# 2. Load and shuffle the data
df = pd.read_csv(csv_path)
df = df.sample(frac=1, random_state=42)

# 3. Split features/label
X = df.drop(['Class', 'Time'], axis=1)
y = df['Class']

# 4. Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# 6. Train the model
model = IsolationForest(n_estimators=100, contamination=0.001, random_state=42)
model.fit(X_train)

# 7. Predict & map to 0/1
y_pred = model.predict(X_test)
y_pred_mapped = [1 if p == -1 else 0 for p in y_pred]

# 8. Evaluate
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred_mapped, digits=4))
print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, y_pred_mapped))