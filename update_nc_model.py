import os

file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/models.py'
with open(file_path, 'r') as f:
    content = f.read()

new_fields = """    # QCL-FRM-14.01 Fields
    NC_SOURCE_CHOICES = [
        ('AUDIT', 'Audit NC'),
        ('LAB', 'Laboratory Activities'),
        ('SUGGESTION', 'Suggestion'),
        ('PT_ILC', 'PT/ILC'),
        ('COMPLAINT', 'Complaint'),
        ('FEEDBACK', 'Customer Feedback'),
        ('RISK', 'Risk Assessment'),
        ('OTHER', 'Any Other'),
    ]
    source = models.CharField(max_length=20, choices=NC_SOURCE_CHOICES, default='LAB')
    
    impact_on_previous_result = models.BooleanField(default=False)
    
    RISK_LEVEL_CHOICES = [
        ('VERY_LOW', 'Very Low'),
        ('LOW', 'Low'),
        ('MODERATE', 'Moderate'),
        ('HIGH', 'High'),
        ('VERY_HIGH', 'Very High'),
    ]
    level_of_risk = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='MODERATE')
    
    nc_type = models.CharField(max_length=30, choices=[('ESSENTIAL', 'Essential'), ('MINOR', 'Minor Non-Essential')], default='ESSENTIAL')
    
    acceptance_status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING')
    
    withhold_reports = models.BooleanField(default=False)
    halt_work = models.BooleanField(default=False)
    recall_work = models.BooleanField(default=False)
    
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_ncs', help_text="AQCM")
    evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluated_ncs', help_text="QCM")

    """

content = content.replace("    nc_id = models.CharField(max_length=50, unique=True, help_text=\"e.g., NC-2026-001\")", "    nc_id = models.CharField(max_length=50, unique=True, help_text=\"e.g., NC-2026-001\")\n" + new_fields)

with open(file_path, 'w') as f:
    f.write(content)
