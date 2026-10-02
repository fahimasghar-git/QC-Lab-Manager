import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lims_core.settings")
django.setup()

from django.apps import apps
from django.db import models

for app_name in ['resources', 'management', 'samples']:
    app_config = apps.get_app_config(app_name)
    print(f"\\n--- APP: {app_name} ---")
    for model in app_config.get_models():
        print(f"{model.__name__}:")
        for field in model._meta.get_fields():
            if isinstance(field, models.ForeignKey) and field.related_model.__name__ == 'User':
                print(f"  - {field.name}")
