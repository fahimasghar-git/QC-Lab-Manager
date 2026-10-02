import zipfile
import xml.etree.ElementTree as ET

def read_docx(path):
    print(f"--- READING DOCX: {path} ---")
    try:
        with zipfile.ZipFile(path, 'r') as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            texts = tree.findall('.//w:t', namespaces)
            content = [t.text.strip() for t in texts if t.text]
            print(" ".join(content[:100]))
            
            tables = tree.findall('.//w:tbl', namespaces)
            for tbl in tables:
                print("[TABLE]")
                for row in tbl.findall('.//w:tr', namespaces):
                    row_data = []
                    for cell in row.findall('.//w:tc', namespaces):
                        cell_texts = cell.findall('.//w:t', namespaces)
                        row_data.append(" ".join(t.text.strip() for t in cell_texts if t.text))
                    print(" | ".join(row_data))
    except Exception as e:
        print("Error reading:", e)
    print("\n")

read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Obselete Documents ISO17025/ISO17025/Supporting Data for ISO 17025/Store Purchase Demand.docx')
