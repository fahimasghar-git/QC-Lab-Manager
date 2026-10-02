import PyPDF2

reader = PyPDF2.PdfReader("test_output.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

print(text)
