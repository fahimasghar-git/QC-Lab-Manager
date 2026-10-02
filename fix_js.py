import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/static/js/custom_admin.js'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('sidebar.style.position = "relative"; // Ensure absolute positioning works', '')

with open(path, 'w') as f:
    f.write(content)
