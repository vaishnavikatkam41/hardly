from pathlib import Path
import re

text = Path("data/extracted_text/ml_2023_sup.txt").read_text(encoding="utf-8")

print("Stars found:", text.count("*****"))
print("Marks found:", len(re.findall(r"\d+M", text)))
print()
print("FIRST 600 CHARACTERS:")
print(text[:600])