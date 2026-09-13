import csv
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
    reader = csv.reader(f)
    all_lines = list(reader)

header = all_lines[0]
people = all_lines[1:]

print("Columns:", len(header))
print("People:", len(people))

studied_col = 1
question_cols = list(range(2, len(header)))

print("Question columns:", len(question_cols))

good_people = []
for person in people:
    studied = person[studied_col].strip().lower()
    if studied == "no":
        continue
    good_people.append(person)

print("Usable people:", len(good_people))
print()

results = []

for col in question_cols:
    question_text = header[col]
    scores = []

    for person in good_people:
        answer = person[col].strip().lower()
        if answer in answer_map:
            scores.append(answer_map[answer])

    if len(scores) == 0:
        continue

    average = sum(scores) / len(scores)

    results.append({
        "question": question_text,
        "difficulty": round(average, 3),
        "n_raters": len(scores)
    })

results.sort(key=lambda r: r["difficulty"])

print("EASIEST 3:")
for r in results[:3]:
    print(" ", r["difficulty"], "-", r["question"][:60])

print()
print("HARDEST 3:")
for r in results[-3:]:
    print(" ", r["difficulty"], "-", r["question"][:60])

output_path = Path("data/difficulty_scores.csv")

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["question", "difficulty", "n_raters"])
    writer.writeheader()
    writer.writerows(results)

print()
print("Saved", len(results), "questions to", output_path)