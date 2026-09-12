from pathlib import Path
from pypdf import PdfReader

pdf_folder = Path("data/raw_pdfs")
pdf_files = list(pdf_folder.glob("*.pdf"))

output_folder = Path("data/extracted_text")
output_folder.mkdir(exist_ok=True)

print("Found", len(pdf_files), "files")

for one_file in pdf_files:
    reader = PdfReader(one_file)
    all_text = ""

    for page in reader.pages:
        all_text = all_text + page.extract_text()

    out_name = one_file.stem + ".txt"
    out_path = output_folder / out_name
    out_path.write_text(all_text, encoding="utf-8")

    print("Saved", out_name, "-", len(all_text), "characters")