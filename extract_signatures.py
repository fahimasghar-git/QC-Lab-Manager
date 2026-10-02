import os
import zipfile
import xml.etree.ElementTree as ET
import re

iso_dir = "/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Process Requirement Procedure"

def extract_docx_signatures(path):
    try:
        with zipfile.ZipFile(path, 'r') as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            texts = [t.text.strip() for t in tree.findall('.//w:t', namespaces) if t.text and t.text.strip()]
            
            # Look for signature keywords in the last 100 elements
            tail = texts[-150:]
            sig_roles = []
            for i, text in enumerate(tail):
                if re.search(r'(Prepared|Reviewed|Checked|Approved|Authorized|Evaluated)\s*By', text, re.IGNORECASE):
                    # Try to grab surrounding context
                    context = " ".join(tail[max(0, i-2):min(len(tail), i+5)])
                    sig_roles.append(context)
            
            if sig_roles:
                print(f"\\n--- {os.path.basename(path)} ---")
                for sr in set(sig_roles):
                    print("  ->", sr)
    except Exception as e:
        pass

def extract_xlsx_signatures(path):
    try:
        with zipfile.ZipFile(path, 'r') as z:
            if 'xl/sharedStrings.xml' in z.namelist():
                xml_content = z.read('xl/sharedStrings.xml')
                tree = ET.fromstring(xml_content)
                ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                texts = [t.text.strip() for t in tree.findall('.//main:t', ns) if t.text and t.text.strip()]
                
                sig_roles = []
                for i, text in enumerate(texts):
                    if re.search(r'(Prepared|Reviewed|Checked|Approved|Authorized|Evaluated)\s*By', text, re.IGNORECASE):
                        context = " ".join(texts[max(0, i-1):min(len(texts), i+3)])
                        sig_roles.append(context)
                
                if sig_roles:
                    print(f"\\n--- {os.path.basename(path)} ---")
                    for sr in set(sig_roles):
                        print("  ->", sr)
    except Exception as e:
        pass

for root, dirs, files in os.walk(iso_dir):
    for f in files:
        if f.startswith("~"): continue
        if f.endswith('.docx'):
            extract_docx_signatures(os.path.join(root, f))
        elif f.endswith('.xlsx'):
            extract_xlsx_signatures(os.path.join(root, f))

