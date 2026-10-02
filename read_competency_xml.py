import zipfile
import xml.etree.ElementTree as ET

def read_docx(path):
    print(f"--- READING: {path} ---")
    try:
        with zipfile.ZipFile(path, 'r') as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            # Find all text nodes
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            texts = tree.findall('.//w:t', namespaces)
            content = []
            for t in texts:
                if t.text:
                    content.append(t.text.strip())
            # Clean and print
            print(" ".join(content))
    except Exception as e:
        print("Error reading:", e)
    print("\n")

read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Resource Requirement Procedure/(QCL-LSP-02) Personal Management/Training Management (6.2) 2025/2.09. Evaluation of Competency (FRM-2.09).docx')
read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Resource Requirement Procedure/(QCL-LSP-02) Personal Management/Personal Management/Lab Personnel Competence and Authorization/Filled/QCL-FRM-1.04/Mubeen Ahmad/(QCL-FRM-1.04) Competency Monitoring of  Laboratory personnel Mubeen.doc')
read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Resource Requirement Procedure/(QCL-LSP-02) Personal Management/Personal Management/Lab Personnel Competence and Authorization/Filled/QCL-FRM-1.04/Awais Hameed/(QCL-FRM-1.04) Competency Monitoring of  Laboratory personnel Awais.docx')
