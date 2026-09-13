import csv
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sentence_transformers import SentenceTransformer

X = np.load("data/embeddings.npy")

y_raw = []
with open("data/difficulty_scores.csv", "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        y_raw.append(float(row["difficulty"]))

y_raw = np.array(y_raw)
median = np.median(y_raw)
y = (y_raw > median).astype(int)

clf = LogisticRegression(C=10, max_iter=2000)
clf.fit(X, y)

with open("data/model.pkl", "wb") as f:
    pickle.dump({"clf": clf, "median": median}, f)

print("Model trained on", len(y), "questions")
print("Saved to data/model.pkl")