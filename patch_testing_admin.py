import os

file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/testing/admin.py'
with open(file_path, 'r') as f:
    content = f.read()

new_actions = """
@admin.action(description='▶️ Submit Result for AQCM Verification')
def submit_test_for_verification(modeladmin, request, queryset):
    from django.utils import timezone
    updated = queryset.filter(status__in=['ASSIGNED', 'IN_PROGRESS']).update(status='PENDING_VERIFICATION', tested_at=timezone.now(), analyst=request.user)
    modeladmin.message_user(request, f"{updated} test(s) submitted to AQCM for verification.", messages.SUCCESS)

@admin.action(description='✔️ Verify Test Result (AQCM)')
def verify_test_result(modeladmin, request, queryset):
    from django.utils import timezone
    updated = queryset.filter(status='PENDING_VERIFICATION').update(status='VERIFIED', reviewed_by=request.user, reviewed_at=timezone.now())
    modeladmin.message_user(request, f"{updated} test(s) verified.", messages.SUCCESS)

class TestResultAdmin(ModelAdmin, SimpleHistoryAdmin):
"""

content = content.replace("class TestResultAdmin(ModelAdmin, SimpleHistoryAdmin):", new_actions)

list_display_old = "list_display = ('sample', 'parameter', 'result_type', 'result_value', 'unit', 'status', 'analyst')"
list_display_new = "list_display = ('sample', 'parameter', 'assigned_to', 'result_value', 'unit', 'status', 'analyst')\n    list_editable = ('assigned_to', 'status')\n    actions = [submit_test_for_verification, verify_test_result]"

content = content.replace(list_display_old, list_display_new)

with open(file_path, 'w') as f:
    f.write(content)
