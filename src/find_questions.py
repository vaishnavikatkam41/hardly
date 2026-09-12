import re
from pathlib import Path

text = Path("data/extracted_text/ml_2023_reg_a.txt").read_text(encoding="utf-8")

parts = text.split("*****")
body = parts[1]

pattern = r"(.*?)(\d+M)"
found = re.findall(pattern, body, re.DOTALL)

print("Found", len(found), "chunks")
print()

for chunk in found[:3]:
    print("QUESTION:", chunk[0].strip())
    print("MARKS:", chunk[1])
    print("---")