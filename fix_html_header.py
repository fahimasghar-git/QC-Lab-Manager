import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/templates/management/non_conformance_log.html'
with open(path, 'r') as f:
    content = f.read()

# Replace percentage widths in style with HTML width attributes
content = content.replace('style="width: 20%;"', 'width="20%"')
content = content.replace('style="width: 50%; font-size: 16px; font-weight: bold;"', 'width="50%" style="font-size: 16px; font-weight: bold;"')
content = content.replace('style="width: 30%; text-align: left;"', 'width="30%" style="text-align: left;"')

with open(path, 'w') as f:
    f.write(content)
