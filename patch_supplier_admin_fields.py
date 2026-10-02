import re

admin_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(admin_path, 'r') as f:
    content = f.read()

old_fields = "'remarks', 'last_evaluation_date', 'next_evaluation_date'"
new_fields = "'remarks', 'evaluated_by', 'approved_by', 'last_evaluation_date', 'next_evaluation_date'"
content = content.replace(old_fields, new_fields)

with open(admin_path, 'w') as f:
    f.write(content)
print("Updated Supplier admin fieldsets.")
