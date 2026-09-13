import csv
from pathlib import Path
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

rows = []
with open("data/difficulty_scores.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print("Loaded", len(rows), "questions")

questions = [r["question"] for r in rows]

print("Making embeddings...")
vectors = model.encode(questions)

print("Shape:", vectors.shape)
print("First question:", questions[0][:50])
print("First 8 numbers:", vectors[0][:8])
from sentence_transformers import util

print()
print("SIMILARITY CHECK")

scores = util.cos_sim(vectors, vectors)

target = 0
print("Question:", questions[target][:60])
print()

pairs = []
for i in range(len(questions)):
    if i == target:
        continue
    pairs.append((float(scores[target][i]), questions[i]))

pairs.sort(reverse=True)

print("MOST SIMILAR:")
for score, q in pairs[:3]:
    print(" ", round(score, 3), "-", q[:55])

print()
print("LEAST SIMILAR:")
for score, q in pairs[-3:]:
    print(" ", round(score, 3), "-", q[:55])
import numpy as np

np.save("data/embeddings.npy", vectors)

with open("data/question_order.txt", "w", encoding="utf-8") as f:
    for q in questions:
        f.write(q + "\n")

print()
print("Saved embeddings:", vectors.shape)