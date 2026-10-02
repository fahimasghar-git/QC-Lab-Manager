import zipfile
import xml.etree.ElementTree as ET

def read_xlsx(path):
    print(f"--- READING XLSX: {path} ---")
    try:
        with zipfile.ZipFile(path, 'r') as z:
            # Get shared strings
            shared_strings = []
            if 'xl/sharedStrings.xml' in z.namelist():
                xml_content = z.read('xl/sharedStrings.xml')
                tree = ET.fromstring(xml_content)
                namespaces = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for t in tree.findall('.//ns:t', namespaces):
                    shared_strings.append(t.text if t.text else '')

            # Get sheet1
            if 'xl/worksheets/sheet1.xml' in z.namelist():
                sheet_xml = z.read('xl/worksheets/sheet1.xml')
                tree = ET.fromstring(sheet_xml)
                namespaces = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for row in tree.findall('.//ns:row', namespaces):
                    row_data = []
                    for cell in row.findall('.//ns:c', namespaces):
                        t = cell.get('t')
                        v = cell.find('ns:v', namespaces)
                        if v is not None:
                            val = v.text
                            if t == 's':  # Shared string
                                val = shared_strings[int(val)]
                            row_data.append(str(val))
                        else:
                            row_data.append('')
                    if any(row_data):
                        print(" | ".join(row_data))
    except Exception as e:
        print("Error reading:", e)

read_xlsx('/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Resource Requirement Procedure/(QCL-LSP-06) Procedure for Provided Services/Updated LSP/(QCL-FRM-6.03) External Provider Evaluation & Re-evaluation Form.xlsx')
