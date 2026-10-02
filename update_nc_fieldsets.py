import re

admin_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/admin.py'
with open(admin_path, 'r') as f:
    content = f.read()

old_fieldsets = """    fieldsets = (
        ('Identification', {
            'fields': ('nc_id', 'description', 'identified_by', 'related_test', 'status')
        }),
        ('Root Cause Analysis & CAPA', {
            'fields': ('root_cause_analysis', 'corrective_action', 'preventive_action')
        }),
        ('Closure', {
            'fields': ('closed_by', 'closed_date')
        }),
    )"""

new_fieldsets = """    fieldsets = (
        ('Identification & Source', {
            'fields': ('nc_id', 'date_identified', 'source', 'description', 'identified_by', 'related_test', 'status')
        }),
        ('Review & Risk Assessment', {
            'fields': (
                'impact_on_previous_result', 'level_of_risk', 'nc_type',
                'acceptance_status', 'withhold_reports', 'halt_work', 'recall_work',
                'reviewed_by', 'evaluated_by'
            )
        }),
        ('Root Cause Analysis & CAPA', {
            'fields': ('root_cause_analysis', 'corrective_action', 'preventive_action')
        }),
        ('Closure', {
            'fields': ('closed_by', 'closed_date')
        }),
    )"""

content = content.replace(old_fieldsets, new_fieldsets)
with open(admin_path, 'w') as f:
    f.write(content)
print("Updated fieldsets.")
