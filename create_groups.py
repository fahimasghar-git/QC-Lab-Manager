import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lims_core.settings')
django.setup()

from django.contrib.auth.models import Group, Permission

def setup_groups():
    groups_config = {
        'Analyst': [],
        'AQCM': [],
        'QCM': [],
        'CEO': [],
        'IT Admin': []
    }

    for perm in Permission.objects.all():
        app = perm.content_type.app_label
        action = perm.codename.split('_')[0] # add, change, delete, view
        
        # 1. Analyst: Receive sample, test, submit results, add methods, parameters, equipment.
        if app in ['samples', 'testing', 'resources', 'inbox']:
            if action in ['add', 'change', 'view']:
                groups_config['Analyst'].append(perm)

        # 2. AQCM: Analyst perms + filling/adding/reviewing management forms. No deleting samples/results.
        if app in ['samples', 'testing', 'resources', 'management', 'inbox']:
            if action in ['add', 'change', 'view']:
                groups_config['AQCM'].append(perm)

        # 3. QCM: All permissions for lab operations, no user management.
        if app in ['samples', 'testing', 'resources', 'management', 'inbox']:
            groups_config['QCM'].append(perm)

        # 4. CEO: Only approval related (needs view and change to trigger approval actions)
        if app in ['samples', 'testing', 'management']:
            if action in ['view', 'change']:
                groups_config['CEO'].append(perm)

        # 5. IT Admin: All infrastructure/user permissions, NO testing/sample permissions
        if app not in ['samples', 'testing']:
            groups_config['IT Admin'].append(perm)

    # Save to Database
    for group_name, perms in groups_config.items():
        group, created = Group.objects.get_or_create(name=group_name)
        group.permissions.set(perms)
        print(f"Successfully configured group: {group_name} ({len(perms)} permissions)")

if __name__ == '__main__':
    setup_groups()
