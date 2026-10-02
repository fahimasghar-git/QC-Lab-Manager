import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(path, 'r') as f:
    content = f.read()

# 1. Equipment
eq_old = """    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_equipments', on_delete=models.RESTRICT, null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_equipments', on_delete=models.RESTRICT, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_equipments', on_delete=models.RESTRICT, null=True, blank=True)"""
eq_new = eq_old + """
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
"""
content = content.replace(eq_old, eq_new)

# 2. EquipmentMaintenance
em_old = """    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='performed_maintenances')
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='verified_maintenances', blank=True, null=True)"""
em_new = """    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='performed_maintenances', null=True, blank=True)
    performed_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='verified_maintenances', blank=True, null=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_VERIFICATION', 'Pending Verification'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='DRAFT')"""
content = content.replace(em_old, em_new)

# 3. ComparativeStatement
cs_old = """    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_statements', on_delete=models.RESTRICT, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_statements', on_delete=models.RESTRICT, null=True, blank=True)"""
cs_new = cs_old + """
    prepared_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
"""
content = content.replace(cs_old, cs_new)

# 4. SupplierEvaluationPlan
sep_old = """    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_evaluation_plans', on_delete=models.RESTRICT, null=True, blank=True)
    prepared_date = models.DateField(auto_now_add=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_evaluation_plans', on_delete=models.RESTRICT, null=True, blank=True)
    approved_date = models.DateField(null=True, blank=True)"""
sep_new = """    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_evaluation_plans', on_delete=models.RESTRICT, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_evaluation_plans', on_delete=models.RESTRICT, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')"""
content = content.replace(sep_old, sep_new)

# 5. Supplier
sup_old = """    evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='evaluated_suppliers', on_delete=models.RESTRICT, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_suppliers', on_delete=models.RESTRICT, null=True, blank=True)"""
sup_new = sup_old + """
    prepared_at = models.DateTimeField(null=True, blank=True) # Mapping evaluated_by -> prepared_at context
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
"""
content = content.replace(sup_old, sup_new)

# 6. PersonnelAuthorization
pa_old = """    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_authorizations', on_delete=models.RESTRICT, null=True, blank=True)
    authorized_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='authorized_authorizations', on_delete=models.RESTRICT, null=True, blank=True)"""
pa_new = pa_old + """
    prepared_at = models.DateTimeField(null=True, blank=True)
    authorized_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
"""
content = content.replace(pa_old, pa_new)

with open(path, 'w') as f:
    f.write(content)
print("Updated resources/models.py with signature fields.")
