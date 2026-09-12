import re
from pathlib import Path

text = Path("data/extracted_text/ml_2023_reg_a.txt").read_text(encoding="utf-8")

parts = text.split("*****")
body = parts[1]

pattern = r"(.*?)(\d+M)"
found = re.findall(pattern, body, re.DOTALL)


def clean_question(raw):
    q = raw.strip()
    q = re.sub(r"Answer the following.*?Marks\)", "", q)
    q = re.sub(r"\bOR\b", " ", q)
    q = re.sub(r"^\s*\d+\s*", "", q)
    q = re.sub(r"^\(?[a-j]\)\s*", "", q)
    q = re.sub(r"\s+", " ", q)
    return q.strip()


print("Found", len(found), "chunks")
print()

for chunk in found[:5]:
    print("Q:", clean_question(chunk[0]))
    print("MARKS:", chunk[1])
    print("---")