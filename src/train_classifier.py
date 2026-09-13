import csv
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.dummy import DummyClassifier

X = np.load("data/embeddings.npy")

y_raw = []
with open("data/difficulty_scores.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        y_raw.append(float(row["difficulty"]))

y_raw = np.array(y_raw)

median = np.median(y_raw)
y = (y_raw > median).astype(int)

print("Median difficulty:", round(median, 3))
print("Easy (0):", (y == 0).sum())
print("Hard (1):", (y == 1).sum())
print()

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

dummy = DummyClassifier(strategy="most_frequent")
d = cross_val_score(dummy, X, y, cv=cv, scoring="accuracy")
print("Baseline accuracy:", round(d.mean(), 3))

for C in [0.01, 0.1, 1, 10, 100]:
    clf = LogisticRegression(C=C, max_iter=2000)
    s = cross_val_score(clf, X, y, cv=cv, scoring="accuracy")
    print("C =", C, "-> accuracy =", round(s.mean(), 3))