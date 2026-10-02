import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/lims_core/settings.py'
with open(path, 'r') as f:
    content = f.read()

pattern = r'(UNFOLD = \{)(.*?)(\n\})'
match = re.search(pattern, content, flags=re.DOTALL)
if match:
    unfold_content = match.group(2)
    if '"SCRIPTS"' not in unfold_content:
        new_unfold_content = unfold_content + ',\n    "SCRIPTS": [\n        "/static/js/custom_admin.js",\n    ]'
        content = content.replace(unfold_content, new_unfold_content)
        with open(path, 'w') as f:
            f.write(content)
        print("Patched UNFOLD settings.")
    else:
        print("SCRIPTS already in UNFOLD.")
else:
    print("UNFOLD not found.")
