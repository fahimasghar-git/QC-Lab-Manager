import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(path, 'r') as f:
    content = f.read()

models = ['CalibrationRecordAdmin', 'CompetencyRecordAdmin', 'CompetencyEvaluationAdmin', 'ReagentStandardAdmin', 'PurchaseRequestAdmin', 'ProductServiceInspectionAdmin']

for model in models:
    content = content.replace(f"class {model}(ModelAdmin, SimpleHistoryAdmin):", f"class {model}(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):")

with open(path, 'w') as f:
    f.write(content)
