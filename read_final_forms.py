import zipfile
import xml.etree.ElementTree as ET
import re

def read_docx(path):
    print(f"\n--- READING DOCX: {path} ---")
    try:
        with zipfile.ZipFile(path, 'r') as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            tables = tree.findall('.//w:tbl', namespaces)
            if not tables:
                print("No tables found. Printing raw text:")
                texts = tree.findall('.//w:t', namespaces)
                print(" ".join(t.text.strip() for t in texts if t.text))
                return
            
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

def dump_xlsx_strings(filepath):
    print(f"\n--- READING XLSX: {filepath} ---")
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            if 'xl/sharedStrings.xml' in z.namelist():
                xml_content = z.read('xl/sharedStrings.xml')
                tree = ET.fromstring(xml_content)
                ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                texts = tree.findall('.//main:t', ns)
                strings = [t.text.strip() for t in texts if t.text and len(t.text.strip()) > 2]
                print("\n".join(strings))
    except Exception as e:
        print("Error reading xlsx:", e)

read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Process Requirement Procedure/(QCL-LSP-19) Reporting of Results/(QCL-FRM-19.01) Assgnment, Summary and Review Form.docx')
read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Process Requirement Procedure/(QCL-LSP-20) Control of Technical Records/QCL-FRM-20.01 Master List of Records.docx')
read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Process Requirement Procedure/(QCL-LSP-20) Control of Technical Records/QCL-FRM-20.02 Master List of Files and Folders.docx')
read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Process Requirement Procedure/(QCL-LSP-21) Customer Feedfack/QCL-FRM-21.01 Customer Feed back.docx')
read_docx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Process Requirement Procedure/(QCL-LSP-22)  handling of test and calibration/(QCL-FRM-22.01) Sample return form.docx')
dump_xlsx_strings('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Process Requirement Procedure/(QCL-LSP-17) Procedure for Quality Assurance/Procedure for Quality Assurance/(QCL-FRM-17.14) Lab Cleaning Inspection Sheet.xlsx')

