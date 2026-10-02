import zipfile
import xml.etree.ElementTree as ET

def read_docx_text(path):
    print(f"\n--- TEXT DOCX: {path} ---")
    try:
        with zipfile.ZipFile(path, 'r') as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            texts = tree.findall('.//w:t', namespaces)
            content = [t.text.strip() for t in texts if t.text]
            print("\n".join(content))
    except Exception as e:
        print("Error reading:", e)

read_docx_text('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Resource Requirement Procedure/(QCL-LSP-02) Personal Management/Personal Management/Lab Personnel Competence and Authorization/(QCL-FRM-1.01) Personnel Authorization Permit.docx')
