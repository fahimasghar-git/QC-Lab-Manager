import zipfile
import xml.etree.ElementTree as ET
import sys

def read_docx(path):
    try:
        with zipfile.ZipFile(path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.XML(xml_content)
            
            # The namespace for Word XML
            WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
            PARA = WORD_NAMESPACE + 'p'
            TEXT = WORD_NAMESPACE + 't'
            
            paragraphs = []
            for paragraph in tree.iter(PARA):
                texts = [node.text for node in paragraph.iter(TEXT) if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            
            return '\n'.join(paragraphs)
    except Exception as e:
        return str(e)

print("=== COA (REPORT) ===")
print(read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Process Requirement Procedure/(QCL-LSP-12) Procedure for review of requests/QCL-FRM-12.03 Report Rev#04.docx')[:2000])

print("\n=== ANALYSIS REQUEST ===")
print(read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Process Requirement Procedure/(QCL-LSP-12) Procedure for review of requests/QCL-FRM-12.01 Analysis Request (Rev.#02).docx')[:2000])
