import zipfile
import xml.etree.ElementTree as ET

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Application File/Final Assessment NCs Records/Externally Provider products and Services/(QCL-FRM-6.03) External Provider Evaluation & Re-evaluation Form.xlsx'
try:
    with zipfile.ZipFile(path) as z:
        shared_strings_xml = z.read('xl/sharedStrings.xml')
        sst_tree = ET.XML(shared_strings_xml)
        NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        shared_strings = [t.text for t in sst_tree.findall('.//ns:t', NS)]
        
        sheet_xml = z.read('xl/worksheets/sheet1.xml')
        sheet_tree = ET.XML(sheet_xml)
        
        for row in sheet_tree.findall('.//ns:row', NS):
            row_data = []
            for cell in row.findall('.//ns:c', NS):
                t = cell.get('t')
                v = cell.find('ns:v', NS)
                if v is not None:
                    if t == 's':
                        idx = int(v.text)
                        if idx < len(shared_strings):
                            row_data.append(shared_strings[idx])
                        else:
                            row_data.append(v.text)
                    else:
                        row_data.append(v.text)
            if any(row_data):
                print(' | '.join([str(x) for x in row_data]))
                
except Exception as e:
    print("Error:", e)
