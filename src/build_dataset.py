import re
import csv
from pathlib import Path

text_folder = Path("data/extracted_text")
text_files = sorted(text_folder.glob("*.txt"))


def clean_question(raw):
    q = raw.strip()
    q = re.sub(r"Contd\.? in [Pp]age \d+", "", q)
    q = re.sub(r"Page \d+ of \d+", "", q)
    q = re.sub(r"Code:\s*\w+", "", q)
    q = re.sub(r"R\d{2}\b", "", q)
    q = re.sub(r"PART\s*[–-]\s*[AB]", "", q)
    q = re.sub(r"\(?Answer.*?Marks\)", "", q)
    q = re.sub(r"\(Compulsory Question\)", "", q)
    q = re.sub(r"\*+", "", q)
    q = re.sub(r"\bOR\b", " ", q)
    q = re.sub(r"^\s*\d+\s*", "", q)
    q = re.sub(r"^\(?[a-j]\)\s*", "", q)
    q = re.sub(r"^\s*\d+\s*", "", q)
    q = re.sub(r"^\(?[a-j]\)\s*", "", q)
    q = re.sub(r"\s+", " ", q)
    return q.strip()


all_rows = []

for one_file in text_files:
    text = one_file.read_text(encoding="utf-8")

    parts = text.split("*****")
    if len(parts) < 2:
        print("SKIPPED (no marker):", one_file.name)
        continue

    body = parts[1]
    found = re.findall(r"(.*?)(\d+M)", body, re.DOTALL)

    for chunk in found:
        question = clean_question(chunk[0])
        marks = chunk[1].replace("M", "")

        if len(question) < 10:
            continue

        all_rows.append({
            "source_file": one_file.stem,
            "question": question,
            "marks": marks
        })

    print(one_file.name, "->", len(found), "chunks")

print()
print("Total questions:", len(all_rows))

output_path = Path("data/questions.csv")

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["source_file", "question", "marks"])
    writer.writeheader()
    writer.writerows(all_rows)

print("Saved to", output_path)