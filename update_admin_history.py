import os

base_dir = '/Users/fahimasghar/Documents/QC-Lab-Manager'
apps = ['samples', 'testing', 'management', 'resources']

for app in apps:
    file_path = os.path.join(base_dir, app, 'admin.py')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
            
        if 'SimpleHistoryAdmin' not in content:
            # Replace ModelAdmin with SimpleHistoryAdmin for the classes
            content = content.replace("from unfold.admin import ModelAdmin", "from unfold.admin import ModelAdmin\nfrom unfold.contrib.simple_history.admin import SimpleHistoryAdmin")
            # Replace 'class SomethingAdmin(ModelAdmin):' with 'class SomethingAdmin(SimpleHistoryAdmin, ModelAdmin):'
            # Note: unfold SimpleHistoryAdmin inherits from ModelAdmin, so we can just replace (ModelAdmin) with (SimpleHistoryAdmin)
            
            # Wait, accounts uses ModelAdmin too but no SimpleHistoryAdmin. We only want to replace ModelAdmin for specific models.
            # Let's just do it directly.
            models_to_track = ['SampleAdmin', 'TestResultAdmin', 'NonConformanceAdmin', 'DocumentAdmin', 'EquipmentAdmin', 'ReagentStandardAdmin', 'RecordArchiveAdmin']
            
            for m in models_to_track:
                content = content.replace(f"class {m}(ModelAdmin):", f"class {m}(SimpleHistoryAdmin):")
                
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Updated {app}/admin.py")
