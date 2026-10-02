import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(path, 'r') as f:
    content = f.read()

em_old = "approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_maintenances', on_delete=models.SET_NULL, null=True, blank=True)"
em_new = em_old + "\n    prepared_at = models.DateTimeField(null=True, blank=True)\n    reviewed_at = models.DateTimeField(null=True, blank=True)\n    approved_at = models.DateTimeField(null=True, blank=True)\n    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]\n    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')"
content = content.replace(em_old, em_new)

with open(path, 'w') as f:
    f.write(content)
