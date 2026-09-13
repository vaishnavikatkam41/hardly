import csv
import numpy as np

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
    row = []
    for col in question_cols:
        answer = person[col].strip().lower()
        row.append(answer_map.get(answer, np.nan))
    matrix.append(row)

M = np.array(matrix, dtype=float)

print("Ratings matrix:", M.shape, "(raters x questions)")
print()

per_question_sd = np.nanstd(M, axis=0)

print("AGREEMENT PER QUESTION")
print("Average spread:", round(per_question_sd.mean(), 3))
print("Most agreed on:", round(per_question_sd.min(), 3))
print("Most argued about:", round(per_question_sd.max(), 3))
print()

per_rater_mean = np.nanmean(M, axis=1)
print("RATER STRICTNESS")
print("Most confident rater:", round(per_rater_mean.min(), 3))
print("Least confident rater:", round(per_rater_mean.max(), 3))
print("Spread across raters:", round(per_rater_mean.std(), 3))

np.save("data/ratings_matrix.npy", M)