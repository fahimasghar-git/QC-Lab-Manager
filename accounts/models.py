from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    employee_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(
        default=False, 
        help_text="Designates whether the user's account is approved by an administrator to use the LIMS."
    )
    
    # ISO 17025 often requires tracking the training/competence level of personnel
    competence_summary = models.TextField(
        blank=True, 
        null=True,
        help_text="Summary of tests the user is certified to perform."
    )

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"
