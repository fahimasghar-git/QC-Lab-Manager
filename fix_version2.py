import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/lims_core/settings.py'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('"/static/js/custom_admin.js?v=2",', '"/static/js/custom_admin.js?v=3",')

with open(path, 'w') as f:
    f.write(content)
