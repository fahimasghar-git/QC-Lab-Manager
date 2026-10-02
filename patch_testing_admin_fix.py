import os

file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/testing/admin.py'
with open(file_path, 'r') as f:
    content = f.read()

# Fix the decorator issue
old = """@admin.register(TestResult)

@admin.action(description='▶️ Submit Result for AQCM Verification')"""

new = """
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

@admin.register(TestResult)"""

content = content.replace(old, new)

# And remove the duplicate definitions from below
dup_to_remove = """
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
"""
content = content.replace(dup_to_remove, "")

with open(file_path, 'w') as f:
    f.write(content)
