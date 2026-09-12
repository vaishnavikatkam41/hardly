import csv
import random
from pathlib import Path

random.seed(42)

rows = []
with open("data/questions.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print("Loaded", len(rows), "questions")

good = []
seen = set()

for row in rows:
    q = row["question"]
    if len(q) < 20:
        continue
    if q.lower() in seen:
        continue
    seen.add(q.lower())
    good.append(row)

print("After cleaning:", len(good))

random.shuffle(good)
chosen = good[:50]

with open("data/survey_50.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["source_file", "question", "marks"])
    writer.writeheader()
    writer.writerows(chosen)

print("Saved 50 questions")
print()

for i, row in enumerate(chosen, start=1):
    print(i, ".", row["question"])