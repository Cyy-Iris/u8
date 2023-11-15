import pdftotext
import json

pdf_path = "../data/assets/pdf/motor.pdf"
with open(pdf_path, "rb") as f:
    pdf = pdftotext.PDF(f, physical=True)

full_pdf = []
for page in pdf:
    full_pdf.append(page)

textFile = open("sample.txt", "w")
textFile.write(json.dumps(full_pdf))
textFile.close()