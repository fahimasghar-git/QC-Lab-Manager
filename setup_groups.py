import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lims_core.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Our specific LIMS models
from samples.models import Sample, Client
from testing.models import TestResult
from resources.models import Equipment, ReagentStandard, CompetencyRecord, CalibrationRecord
from management.models import Document, NonConformance, RecordArchive

# Define the groups
group_names = ['Analyst', 'Reviewer', 'Approver', 'Admin', 'Record Keeper']

for name in group_names:
    Group.objects.get_or_create(name=name)

def assign_perms(group_name, models, actions=['view', 'add', 'change']):
    group = Group.objects.get(name=group_name)
    perms = []
    for model in models:
        ct = ContentType.objects.get_for_model(model)
        for action in actions:
            codename = f"{action}_{model._meta.model_name}"
            try:
                perm = Permission.objects.get(content_type=ct, codename=codename)
                perms.append(perm)
            except Permission.DoesNotExist:
                pass
    group.permissions.add(*perms)

# 1. Analyst: Can add/edit samples, tests, and view resources
assign_perms('Analyst', [Sample, TestResult, Client], ['view', 'add', 'change'])
assign_perms('Analyst', [Equipment, ReagentStandard, Document], ['view'])

# 2. Reviewer (AQCM): Can view/edit samples, tests, and view resources
assign_perms('Reviewer', [Sample, TestResult, Client], ['view', 'change'])
assign_perms('Reviewer', [Equipment, ReagentStandard, CompetencyRecord, CalibrationRecord], ['view'])

# 3. Approver (QCM): Can view/edit samples, tests, and handle CAPA (NonConformance)
assign_perms('Approver', [Sample, TestResult, Client], ['view', 'change'])
assign_perms('Approver', [NonConformance], ['view', 'add', 'change'])
assign_perms('Approver', [RecordArchive, Document], ['view'])

# 4. Record Keeper: Handles ISO 17025 Docs, CAPA, and Archives
assign_perms('Record Keeper', [Document, RecordArchive, NonConformance], ['view', 'add', 'change'])
assign_perms('Record Keeper', [CompetencyRecord, CalibrationRecord, Equipment, ReagentStandard], ['view', 'add', 'change'])

# 5. Admin: Gets everything (excluding actual superuser deletion powers unless specified)
all_models = [Sample, Client, TestResult, Equipment, ReagentStandard, CompetencyRecord, CalibrationRecord, Document, NonConformance, RecordArchive]
assign_perms('Admin', all_models, ['view', 'add', 'change', 'delete'])

print("Groups and initial permissions created successfully!")
