import zipfile
import xml.etree.ElementTree as ET

def read_docx(path):
    print(f"\n--- READING DOCX: {path} ---")
    try:
        with zipfile.ZipFile(path, 'r') as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
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

read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Process Requirement Procedure/(QCL-LSP-14) Procedure for Non Conformence (8.7)/Revised/(QCL-FRM-14.02) Non Conformance Log.docx')
read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Application File/Final Assessment NCs Records/Ruf/(QCL-FRM-14.03) Rootcause Analysis Form.docx')
