import zipfile
import re
import sys

def read_strings(path):
    print(f"\n--- {path.split('/')[-1]} ---")
    try:
        with zipfile.ZipFile(path, 'r') as z:
            strings = []
            if 'xl/sharedStrings.xml' in z.namelist():
                xml = z.read('xl/sharedStrings.xml').decode('utf-8')
                strings = re.findall(r'<t.*?>(.*?)</t>', xml)
                print("\n".join(strings[:50]))
            else:
                print("No shared strings found.")
    except Exception as e:
        print("Error:", e)

paths = [
    '/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Resource Requirement Procedure/(QCL-LSP-06) Procedure for Provided Services/Updated LSP/(QCL-FRM-6.03) External Provider Evaluation & Re-evaluation Form.xlsx',
    '/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Management system requirement/(QCL-LSP-14) Internal Audit/Updated LSP/(QCL-FRM-14.01) Internal Audit Programme.xlsx',
    '/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Structural Requirement Procedure/(QCL-LSP-05) Personnel/Updated LSP/(QCL-FRM-5.01) Training Program.xlsx'
]
for p in paths:
    read_strings(p)
