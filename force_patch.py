import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(path, 'r') as f:
    content = f.read()

# 1. Equipment
eq_old = "approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_equipments', on_delete=models.RESTRICT, null=True, blank=True)"
eq_new = eq_old + "\n    prepared_at = models.DateTimeField(null=True, blank=True)\n    reviewed_at = models.DateTimeField(null=True, blank=True)\n    approved_at = models.DateTimeField(null=True, blank=True)\n    DIGITAL_STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]\n    signature_status = models.CharField(max_length=20, choices=DIGITAL_STATUS_CHOICES, default='DRAFT')"
content = content.replace(eq_old, eq_new)

# 2. EquipmentMaintenance
em_old = "verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='verified_maintenances', blank=True, null=True)"
em_new = em_old + "\n    performed_at = models.DateTimeField(null=True, blank=True)\n    verified_at = models.DateTimeField(null=True, blank=True)\n    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_VERIFICATION', 'Pending Verification'), ('APPROVED', 'Approved')]\n    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='DRAFT')"
content = content.replace(em_old, em_new)

# 3. Supplier
sup_old = "approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_suppliers', on_delete=models.RESTRICT, null=True, blank=True)"
sup_new = sup_old + "\n    prepared_at = models.DateTimeField(null=True, blank=True)\n    approved_at = models.DateTimeField(null=True, blank=True)\n    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]\n    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')"
# In case Supplier also matches Eq, we only replace the specific one if it didn't already
# Actually eq_old and sup_old are different related_names.
content = content.replace(sup_old, sup_new)

with open(path, 'w') as f:
    f.write(content)
