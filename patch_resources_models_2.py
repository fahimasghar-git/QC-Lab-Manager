import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(path, 'r') as f:
    content = f.read()

# 1. Equipment
content = content.replace(
    "approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_equipments', on_delete=models.RESTRICT, null=True, blank=True)",
    "approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_equipments', on_delete=models.RESTRICT, null=True, blank=True)\n    prepared_at = models.DateTimeField(null=True, blank=True)\n    reviewed_at = models.DateTimeField(null=True, blank=True)\n    approved_at = models.DateTimeField(null=True, blank=True)\n    DIGITAL_STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]\n    signature_status = models.CharField(max_length=20, choices=DIGITAL_STATUS_CHOICES, default='DRAFT')"
)

# 2. EquipmentMaintenance
content = content.replace(
    "verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='verified_maintenances', blank=True, null=True)",
    "verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='verified_maintenances', blank=True, null=True)\n    performed_at = models.DateTimeField(null=True, blank=True)\n    verified_at = models.DateTimeField(null=True, blank=True)\n    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_VERIFICATION', 'Pending Verification'), ('APPROVED', 'Approved')]\n    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='DRAFT')"
)

# 3. Supplier
content = content.replace(
    "approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_suppliers', on_delete=models.RESTRICT, null=True, blank=True)",
    "approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_suppliers', on_delete=models.RESTRICT, null=True, blank=True)\n    prepared_at = models.DateTimeField(null=True, blank=True)\n    approved_at = models.DateTimeField(null=True, blank=True)\n    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]\n    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')"
)

with open(path, 'w') as f:
    f.write(content)
print("Patched models successfully.")
