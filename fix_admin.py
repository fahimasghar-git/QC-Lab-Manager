import sys

with open('management/admin.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "@admin.action(description='🖨️ Print Non-Conformance Form (QCL-FRM-14.01)')" in line:
        skip = True
    if skip and 'return render(request, \'management/non_conformance_form.html\', {\'ncs\': queryset})' in line:
        skip = False
        continue
    if skip:
        continue
    
    if i == 24 and 'from django.utils import timezone' in line:
        continue # remove duplicate timezone import at line 25
        
    new_lines.append(line)

content = "".join(new_lines)

# Now insert the action inside NonConformanceAdmin
action_code = """
    @admin.action(description='🖨️ Print Non-Conformance Form (QCL-FRM-14.01)')
    def print_non_conformance(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'management/non_conformance_form.html', {'ncs': queryset})

"""

content = content.replace("super().save_model(request, obj, form, change)", "super().save_model(request, obj, form, change)\n" + action_code)

with open('management/admin.py', 'w') as f:
    f.write(content)
print("Fixed admin.py")
