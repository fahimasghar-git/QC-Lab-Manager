import re

def dump_strings(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # decode ignoring errors, then regex find words
    text = data.decode('ascii', errors='ignore')
    words = re.findall(r'[A-Za-z0-9 _-]{4,}', text)
    
    # filter out likely junk
    words = [w for w in words if re.search(r'[A-Za-z]{3,}', w)]
    
    # print unique ordered
    seen = set()
    for w in words:
        if w not in seen:
            print(w)
            seen.add(w)

dump_strings("/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025/Resource Requirement Procedure/(QCL-LSP-06) Procedure for Provided Services/1st LSP/Filled Form/Rev# 00/6.05/(QCL-FRM 6.05) Comparative Statement Flame Photometer.xls")
