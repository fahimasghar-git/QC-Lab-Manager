import re
admin_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/admin.py'
with open(admin_path, 'r') as f:
    content = f.read()

# Add render import if missing
if "from django.shortcuts import render" not in content:
    content = content.replace("from django.contrib import admin", "from django.contrib import admin\nfrom django.shortcuts import render")

new_action = """
    @admin.action(description='🖨️ Print Non-Conformance Form (QCL-FRM-14.01)')
    def print_non_conformance(self, request, queryset):
        return render(request, 'management/non_conformance_form.html', {'ncs': queryset})
"""

# Insert action into actions list
if "actions = [" not in content.split("class NonConformanceAdmin")[1]:
    # Add actions list
    content = re.sub(r'class NonConformanceAdmin.*?readonly_fields = .*?\n', lambda m: m.group(0) + "    actions = ['print_non_conformance']\n", content, flags=re.DOTALL)
    
    # Add the action method at the end of the class
    # Since it's tricky to find the end of the class reliably, I'll insert it before `class RecordArchiveAdmin`
    content = content.replace("@admin.register(RecordArchive)", new_action + "\n@admin.register(RecordArchive)")
    
with open(admin_path, 'w') as f:
    f.write(content)

print("Updated NC Admin.")
