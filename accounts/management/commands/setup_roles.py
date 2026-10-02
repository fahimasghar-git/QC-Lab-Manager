from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Create default roles (Groups) for the ISO 17025 LIMS'

    def handle(self, *args, **kwargs):
        # Define the roles based on ISO 17025 requirements for a fertilizer lab
        roles = [
            'Admin',
            'Lab Manager',
            'Analyst',
            'QA/QC Officer',
            'Sample Custodian'
        ]

        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created role: "{role}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Role "{role}" already exists.'))
        
        self.stdout.write(self.style.SUCCESS('Role setup complete.'))
