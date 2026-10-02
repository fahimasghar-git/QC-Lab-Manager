import os
import openpyxl

files = [
    '/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Resource Requirement Procedure/(QCL-LSP-06) Procedure for Provided Services/Updated LSP/(QCL-FRM-6.03) External Provider Evaluation & Re-evaluation Form.xlsx',
    '/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Management system requirement/(QCL-LSP-14) Internal Audit/Updated LSP/(QCL-FRM-14.01) Internal Audit Programme.xlsx',
    '/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Structural Requirement Procedure/(QCL-LSP-05) Personnel/Updated LSP/(QCL-FRM-5.01) Training Program.xlsx'
]

for f in files:
    if os.path.exists(f):
        print(f"\n--- {os.path.basename(f)} ---")
        wb = openpyxl.load_range(f) if hasattr(openpyxl, 'load_range') else openpyxl.load_workbook(f, data_only=True)
        sheet = wb.active
        for row in list(sheet.iter_rows(values_only=True))[:20]:
            print([str(cell)[:50] if cell is not None else '' for cell in row])
    else:
        print(f"File not found: {f}")
