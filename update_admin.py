import os

apps = ['accounts', 'samples', 'testing', 'resources', 'management']
base_dir = '/Users/fahimasghar/Documents/QC-Lab-Manager'

for app in apps:
    admin_file = os.path.join(base_dir, app, 'admin.py')
    if os.path.exists(admin_file):
        with open(admin_file, 'r') as f:
            content = f.read()
        
        # Replace admin imports and usages
        if 'from unfold.admin import ModelAdmin' not in content:
            content = content.replace('from django.contrib import admin', 'from django.contrib import admin\nfrom unfold.admin import ModelAdmin, TabularInline, StackedInline')
            content = content.replace('admin.ModelAdmin', 'ModelAdmin')
            content = content.replace('admin.TabularInline', 'TabularInline')
            content = content.replace('admin.StackedInline', 'StackedInline')
            
            with open(admin_file, 'w') as f:
                f.write(content)
        print(f"Updated {app}/admin.py")
