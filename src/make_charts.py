import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

Path("figures").mkdir(exist_ok=True)

rows = []
with open("data/difficulty_scores.csv", "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        rows.append(row)

scores = np.array([float(r["difficulty"]) for r in rows])

plt.figure(figsize=(7, 4))
plt.hist(scores, bins=12, color="#4a7fb5", edgecolor="white")
plt.xlabel("Difficulty score (0 = easy, 2 = hard)")
plt.ylabel("Number of questions")
plt.title("Distribution of question difficulty")
plt.tight_layout()
plt.savefig("figures/difficulty_distribution.png", dpi=150)
plt.close()

M = np.load("data/ratings_matrix.npy")
spread = np.nanstd(M, axis=0)

plt.figure(figsize=(7, 4))
plt.scatter(scores, spread, alpha=0.7, color="#c4643a")
plt.xlabel("Mean difficulty")
plt.ylabel("Disagreement between raters (SD)")
plt.title("Do raters agree more on easy or hard questions?")
plt.tight_layout()
plt.savefig("figures/agreement_vs_difficulty.png", dpi=150)
plt.close()

rater_means = np.nanmean(M, axis=1)

plt.figure(figsize=(7, 4))
plt.bar(range(len(rater_means)), sorted(rater_means), color="#5a9367")
plt.xlabel("Rater (sorted)")
plt.ylabel("Their average score")
plt.title("Some raters say 'no' far more than others")
plt.tight_layout()
plt.savefig("figures/rater_strictness.png", dpi=150)
plt.close()

print("Saved 3 charts to figures/")