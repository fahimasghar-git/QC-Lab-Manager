import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lims_core.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from management.models import Risk, ManagementReview

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

models_new = [Risk, ManagementReview]
assign_perms('Record Keeper', models_new, ['view', 'add', 'change'])
assign_perms('Approver', models_new, ['view', 'add', 'change'])
assign_perms('Admin', models_new, ['view', 'add', 'change', 'delete'])

print("Permissions updated for 8.5 and 8.9")
