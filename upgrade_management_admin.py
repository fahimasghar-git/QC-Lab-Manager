import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/admin.py'
with open(path, 'r') as f:
    content = f.read()

models = ['DocumentAdmin', 'NonConformanceAdmin', 'RecordArchiveAdmin', 'InternalAuditAdmin', 'RiskAdmin', 'ManagementReviewAdmin', 'LabCleaningInspectionAdmin', 'CustomerFeedbackAdmin']

for model in models:
    content = content.replace(f"class {model}(ModelAdmin, SimpleHistoryAdmin):", f"class {model}(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):")
    # Also handle if it's just `class ModelAdmin(admin.ModelAdmin):` etc...
    # Oh wait, they inherit `(ModelAdmin, SimpleHistoryAdmin)` usually.

with open(path, 'w') as f:
    f.write(content)
print("Upgraded management admin.")
