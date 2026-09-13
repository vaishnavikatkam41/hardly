import csv
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score, KFold
from sklearn.dummy import DummyRegressor

X = np.load("data/embeddings.npy")

y = []
with open("data/difficulty_scores.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        y.append(float(row["difficulty"]))

y = np.array(y)

print("X shape:", X.shape)
print("y shape:", y.shape)
print("Difficulty range:", round(y.min(), 3), "to", round(y.max(), 3))
print()

cv = KFold(n_splits=5, shuffle=True, random_state=42)

baseline = DummyRegressor(strategy="mean")
base_scores = cross_val_score(baseline, X, y, cv=cv, scoring="r2")
print("Baseline R2:", round(base_scores.mean(), 3))

model = Ridge(alpha=1.0)
model_scores = cross_val_score(model, X, y, cv=cv, scoring="r2")
print("Ridge R2:   ", round(model_scores.mean(), 3))
print("Each fold:  ", [round(s, 3) for s in model_scores])
print()
print("TUNING ALPHA")

for alpha in [0.001, 0.005, 0.01, 0.05, 0.1, 0.3, 0.5, 1]:
    m = Ridge(alpha=alpha)
    s = cross_val_score(m, X, y, cv=cv, scoring="r2")
    print("alpha =", alpha, "-> R2 =", round(s.mean(), 3))
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

print()
print("COMPARING FEATURE SETS")

F = np.load("data/features.npy")
combined = np.hstack([X, F])

def test(name, data, alpha):
    m = make_pipeline(StandardScaler(), Ridge(alpha=alpha))
    s = cross_val_score(m, data, y, cv=cv, scoring="r2")
    print(name, "-> R2 =", round(s.mean(), 3))

test("Embeddings only  ", X, 0.1)
test("Features only    ", F, 1.0)
test("Both together    ", combined, 0.1)