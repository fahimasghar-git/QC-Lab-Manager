import zipfile
import xml.etree.ElementTree as ET
import glob

def read_docx(path):
    print(f"\n--- READING DOCX: {path} ---")
    try:
        with zipfile.ZipFile(path, 'r') as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            texts = tree.findall('.//w:t', namespaces)
            content = [t.text.strip() for t in texts if t.text]
            print(" ".join(content[:150]))
            
            tables = tree.findall('.//w:tbl', namespaces)
            for i, tbl in enumerate(tables):
                print(f"[TABLE {i}]")
                for row in tbl.findall('.//w:tr', namespaces):
                    row_data = []
                    for cell in row.findall('.//w:tc', namespaces):
                        cell_texts = cell.findall('.//w:t', namespaces)
                        row_data.append(" ".join(t.text.strip() for t in cell_texts if t.text))
                    print(" | ".join(row_data))
    except Exception as e:
        print("Error reading:", e)

paths = glob.glob('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Resource Requirement Procedure/(QCL-LSP-06) Procedure for Provided Services/Updated LSP/*.docx')
for p in paths:
    if "6.04" in p or "6.05" in p or "6.06" in p or "6.08" in p:
        read_docx(p)
