import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/models.py'
with open(path, 'r') as f:
    content = f.read()

classes = re.findall(r'class (\w+)\(models\.Model\):', content)
for c in classes:
    class_block = re.search(rf'class {c}\(.*?class Meta:(.*?)\n\n', content, re.DOTALL)
    if class_block:
        meta = re.search(r'verbose_name = (.*?)\n', class_block.group(1))
        if meta:
            print(f"{c}: {meta.group(1)}")
        else:
            print(f"{c}: Meta exists but no verbose_name")
    else:
        print(f"{c}: NO META")
