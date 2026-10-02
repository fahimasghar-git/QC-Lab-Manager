import os
import re

base_dir = '/Users/fahimasghar/Documents/QC-Lab-Manager'
models_to_track = {
    'samples': ['Sample'],
    'testing': ['TestResult'],
    'management': ['NonConformance', 'Document', 'RecordArchive'],
    'resources': ['Equipment', 'ReagentStandard']
}

for app, models in models_to_track.items():
    file_path = os.path.join(base_dir, app, 'models.py')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        if 'HistoricalRecords' not in content:
            # Add import
            import_statement = "from simple_history.models import HistoricalRecords\n"
            
            # Find last import or just put at top (after from django.db import models)
            content = content.replace("from django.db import models", "from django.db import models\n" + import_statement)
            
            for model_name in models:
                # Regex to find class definition and insert history at the end of fields, before def __str__ or similar
                # Just replace "class ModelName(models.Model):" and then append the history field somewhere.
                # Actually, an easier way is to just append `history = HistoricalRecords()` right after the class declaration line
                class_def = f"class {model_name}(models.Model):"
                replacement = f"{class_def}\n    history = HistoricalRecords()\n"
                content = content.replace(class_def, replacement)
            
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Updated {app}/models.py")
