import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/lims_core/settings.py'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('},,', '},')

with open(path, 'w') as f:
    f.write(content)
print("Fixed syntax error.")
