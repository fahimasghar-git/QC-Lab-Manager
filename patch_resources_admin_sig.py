import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(path, 'r') as f:
    content = f.read()

# Add mixin import
content = "from lims_core.admin_mixins import DigitalSignatureMixin\n" + content

# Apply mixin to models
for model_admin in ['EquipmentAdmin', 'EquipmentMaintenanceAdmin', 'ComparativeStatementAdmin', 'SupplierEvaluationPlanAdmin', 'SupplierAdmin', 'PersonnelAuthorizationAdmin']:
    content = content.replace(
        f"class {model_admin}(ModelAdmin, SimpleHistoryAdmin):",
        f"class {model_admin}(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):"
    )

# Fix prepared_date to prepared_at in list_display
content = content.replace("list_display = ('year', 'prepared_by', 'prepared_date', 'approved_by')", "list_display = ('year', 'prepared_by', 'prepared_at', 'approved_by')")

with open(path, 'w') as f:
    f.write(content)
print("Updated resources/admin.py")
