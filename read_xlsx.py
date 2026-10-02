import openpyxl

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Application File/Final Assessment NCs Records/Externally Provider products and Services/(QCL-FRM-6.03) External Provider Evaluation & Re-evaluation Form.xlsx'
try:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    
    for row in ws.iter_rows(min_row=1, max_row=40, values_only=True):
        print(row)
except Exception as e:
    print("Error:", e)
