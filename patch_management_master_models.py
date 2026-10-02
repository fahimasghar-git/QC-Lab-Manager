import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/models.py'
with open(path, 'r') as f:
    content = f.read()

sig_fields = """
    # Digital Signatures
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)s_prepared", on_delete=models.RESTRICT, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)s_reviewed", on_delete=models.RESTRICT, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)s_approved", on_delete=models.RESTRICT, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
"""

# Inject into MasterListRecord
content = content.replace(
    'retention_period = models.CharField(max_length=100, verbose_name="Retention Period")\n    remarks = models.TextField(blank=True, null=True)',
    'retention_period = models.CharField(max_length=100, verbose_name="Retention Period")\n    remarks = models.TextField(blank=True, null=True)' + sig_fields
)

# Inject into MasterListFileFolder
content = content.replace(
    'location = models.CharField(max_length=200, verbose_name="Location")\n    status = models.CharField(max_length=50, verbose_name="Status")',
    'location = models.CharField(max_length=200, verbose_name="Location")\n    folder_status = models.CharField(max_length=50, verbose_name="Status", default="Active")' + sig_fields
)
# Note: I renamed 'status' in MasterListFileFolder to 'folder_status' to not clash with the signature 'status'.

with open(path, 'w') as f:
    f.write(content)

print("Updated management models with signature fields.")
