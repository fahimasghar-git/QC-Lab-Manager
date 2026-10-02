import os
import zipfile
import xml.etree.ElementTree as ET
import re

iso_dir = "/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025"

def get_signatures(texts):
    sigs = []
    for i, text in enumerate(texts):
        if re.search(r'(Prepared|Reviewed|Checked|Approved|Authorized|Evaluated)\s*By', text, re.IGNORECASE):
            # Grab a bit of context, especially following lines which often have the role
            context = " ".join(texts[max(0, i):min(len(texts), i+5)])
            sigs.append(context)
    return set(sigs)

def process_file(path):
    if "/Obselete" in path or "~$" in path: return
    try:
        with zipfile.ZipFile(path, 'r') as z:
            if path.endswith('.docx') and 'word/document.xml' in z.namelist():
                xml = z.read('word/document.xml')
                tree = ET.fromstring(xml)
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                texts = [t.text.strip() for t in tree.findall('.//w:t', ns) if t.text and t.text.strip()]
                sigs = get_signatures(texts)
                if sigs:
                    print(f"\\n[{os.path.basename(path)}]")
                    for s in sigs: print("  ->", s)
            elif path.endswith('.xlsx') and 'xl/sharedStrings.xml' in z.namelist():
                xml = z.read('xl/sharedStrings.xml')
                tree = ET.fromstring(xml)
                ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                texts = [t.text.strip() for t in tree.findall('.//main:t', ns) if t.text and t.text.strip()]
                sigs = get_signatures(texts)
                if sigs:
                    print(f"\\n[{os.path.basename(path)}]")
                    for s in sigs: print("  ->", s)
    except Exception:
        pass

for root, dirs, files in os.walk(iso_dir):
    for f in files:
        if f.endswith('.docx') or f.endswith('.xlsx'):
            process_file(os.path.join(root, f))
