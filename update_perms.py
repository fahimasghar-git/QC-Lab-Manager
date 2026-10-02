import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lims_core.settings')
django.setup()

from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from resources.models import Supplier, PurchaseRequest
from management.models import InternalAudit, AuditFinding

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

# Assign to Record Keeper and Admin
models_new = [Supplier, PurchaseRequest, InternalAudit, AuditFinding]

assign_perms('Record Keeper', models_new, ['view', 'add', 'change'])
assign_perms('Approver', models_new, ['view', 'add', 'change']) # QCM usually oversees these
assign_perms('Admin', models_new, ['view', 'add', 'change', 'delete'])

print("New permissions added successfully!")
