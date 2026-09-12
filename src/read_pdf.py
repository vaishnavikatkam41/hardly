from pypdf import PdfReader

reader = PdfReader("data/raw_pdfs/ml_2022_reg.pdf")

print("Number of pages:", len(reader.pages))

first_page = reader.pages[0]
text = first_page.extract_text()

print(text)