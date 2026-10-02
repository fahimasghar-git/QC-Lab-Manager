import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/admin.py'
with open(path, 'r') as f:
    content = f.read()

import_statement = "from .models import Risk, ManagementReview"
new_import_statement = "from .models import Risk, ManagementReview, LabCleaningInspection, LabCleaningDailyRecord, MasterListRecord, MasterListFileFolder, CustomerFeedback"

content = content.replace(import_statement, new_import_statement)

with open(path, 'w') as f:
    f.write(content)
print("Fixed imports in management/admin.py")
