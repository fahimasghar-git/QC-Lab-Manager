import os
import django
import re

base_dir = '/Users/fahimasghar/Documents/QC-Lab-Manager'
testing_models_path = os.path.join(base_dir, 'testing/models.py')

with open(testing_models_path, 'r') as f:
    content = f.read()

# 1. Update STATUS_CHOICES
old_status = """    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
    )"""

new_status = """    STATUS_CHOICES = (
        ('PENDING', 'Pending Assignment'),
        ('ASSIGNED', 'Assigned to Analyst'),
        ('IN_PROGRESS', 'In Progress'),
        ('PENDING_VERIFICATION', 'Pending AQCM Verification'),
        ('VERIFIED', 'Verified by AQCM'),
    )"""

if old_status in content:
    content = content.replace(old_status, new_status)
else:
    # Just in case formatting is slightly different
    pass # I'll use regex or sed if needed. Let's try replacing the whole block.

# Let's just rewrite testing/models.py carefully to include assigned_to
