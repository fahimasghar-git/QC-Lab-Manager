from django.db import migrations

def create_na_equipment(apps, schema_editor):
    Equipment = apps.get_model('resources', 'Equipment')
    Equipment.objects.get_or_create(
        name="N/A",
        defaults={
            'identification_no': 'N/A',
            'status': 'ACTIVE'
        }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0023_calibrationrecord_approved_at_and_more'),
    ]

    operations = [
        migrations.RunPython(create_na_equipment),
    ]
