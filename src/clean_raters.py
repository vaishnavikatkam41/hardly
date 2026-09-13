import csv
import numpy as np
from pathlib import Path

answer_map = {
    "yes": 0,
    "yes, i could answer this confidently": 0,
    "partly": 1,
    "partly — i'd lose some marks": 1,
    "partly - i'd lose some marks": 1,
    "no": 2,
    "no, i could not answer this": 2,
}

with open("data/responses.csv", "r", encoding="utf-8") as f:
    all_lines = list(csv.reader(f))

header = all_lines[0]
people = [p for p in all_lines[1:] if p[1].strip().lower() != "no"]
question_cols = list(range(2, len(header)))

matrix = []
for person in people:
    row = [answer_map.get(person[c].strip().lower(), np.nan) for c in question_cols]
    matrix.append(row)

M = np.array(matrix, dtype=float)
print("Before cleaning:", M.shape)

rater_sd = np.nanstd(M, axis=1)

print()
print("RATER VARIETY (sd of their own answers)")
for i, sd in enumerate(rater_sd):
    flag = "  <-- DROP (no variety)" if sd < 0.1 else ""
    print(" rater", i, "sd =", round(sd, 3), flag)

keep = rater_sd >= 0.1
M_clean = M[keep]

print()
print("After cleaning:", M_clean.shape)

new_scores = np.nanmean(M_clean, axis=0)

questions = [header[c] for c in question_cols]

rows = []
for q, s in zip(questions, new_scores):
    rows.append({
        "question": q,
        "difficulty": round(float(s), 3),
        "n_raters": int(M_clean.shape[0])
    })

with open("data/difficulty_scores.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["question", "difficulty", "n_raters"])
    writer.writeheader()
    writer.writerows(rows)

print("Saved cleaned difficulty scores")
print("New range:", round(new_scores.min(), 3), "to", round(new_scores.max(), 3))