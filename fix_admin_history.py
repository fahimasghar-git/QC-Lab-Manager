import os

base_dir = '/Users/fahimasghar/Documents/QC-Lab-Manager'
apps = ['samples', 'testing', 'management', 'resources']

for app in apps:
    file_path = os.path.join(base_dir, app, 'admin.py')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
            
        content = content.replace("from unfold.contrib.simple_history.admin import SimpleHistoryAdmin", "from simple_history.admin import SimpleHistoryAdmin")
        # Also there was a bug where I might have replaced ModelAdmin, TabularInline, StackedInline.
        content = content.replace("from unfold.contrib.simple_history.admin import SimpleHistoryAdmin, TabularInline, StackedInline", "from simple_history.admin import SimpleHistoryAdmin")
        
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Fixed {app}/admin.py")
