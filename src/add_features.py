import csv
import numpy as np

rows = []
with open("data/difficulty_scores.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

hard_verbs = ["prove", "derive", "formulate", "differentiate", "compare", "analyse", "analyze"]
easy_verbs = ["what", "define", "list", "state", "mention", "write"]

features = []

for row in rows:
    q = row["question"].strip().lower()

    n_chars = len(q)
    n_words = len(q.split())

    has_hard = 0
    for v in hard_verbs:
        if v in q:
            has_hard = 1

    has_easy = 0
    for v in easy_verbs:
        if q.startswith(v):
            has_easy = 1

    has_explain = 1 if "explain" in q else 0
    has_example = 1 if "example" in q else 0
    n_parts = q.count("(i)") + q.count("?")

    features.append([n_chars, n_words, has_hard, has_easy, has_explain, has_example, n_parts])

F = np.array(features, dtype=float)

print("Feature shape:", F.shape)
print()
print("Example - first question:")
print(rows[0]["question"][:60])
print("chars, words, hard, easy, explain, example, parts")
print(F[0])

np.save("data/features.npy", F)
print()
print("Saved features")