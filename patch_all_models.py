import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(path, 'r') as f:
    content = f.read()

# 1. CompetencyRecord
if "prepared_by = models.ForeignKey(" not in content.split("class CompetencyRecord")[1]:
    old_comp_rec = """    remarks = models.TextField(blank=True, null=True, help_text="Any comments on the staff's performance")

    class Meta:"""
    new_comp_rec = """    remarks = models.TextField(blank=True, null=True, help_text="Any comments on the staff's performance")
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_competencies', on_delete=models.SET_NULL, null=True, blank=True)
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='checked_competencies', on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_competencies', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:"""
    content = content.replace(old_comp_rec, new_comp_rec)

# 2. CompetencyEvaluation
if "manager_qc = models.ForeignKey(" not in content.split("class CompetencyEvaluation")[1]:
    old_comp_eval = """    remarks = models.TextField(blank=True, null=True, help_text="Remarks / Comments")

    class Meta:"""
    new_comp_eval = """    remarks = models.TextField(blank=True, null=True, help_text="Remarks / Comments")
    
    manager_qc = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='manager_evaluations', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:"""
    content = content.replace(old_comp_eval, new_comp_eval)

# 3. PurchaseRequest
if "spd_no = models.CharField(" not in content:
    old_pr = """    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchase_requests', on_delete=models.RESTRICT)"""
    
    new_pr = """    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    
    spd_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="SPD No")
    insp_mints_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="Insp Mints NO & Date")
    service_call_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="Service Call No & Date")
    store_keeper = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='store_keeper_purchases', on_delete=models.SET_NULL, null=True, blank=True)
    
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchase_requests', on_delete=models.RESTRICT)"""
    content = content.replace(old_pr, new_pr)

# 4. Equipment
if "prepared_by =" not in content.split("class Equipment(")[1]:
    old_eq = """    date_put_into_service = models.DateField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')"""
    
    new_eq = """    date_put_into_service = models.DateField(blank=True, null=True)
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_equipments', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_equipments', on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_equipments', on_delete=models.SET_NULL, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')"""
    content = content.replace(old_eq, new_eq)

# 5. EquipmentMaintenance
if "prepared_by =" not in content.split("class EquipmentMaintenance(")[1]:
    old_maint = """    remarks = models.TextField(blank=True, null=True)

    class Meta:"""
    
    new_maint = """    remarks = models.TextField(blank=True, null=True)
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_maintenances', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_maintenances', on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_maintenances', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:"""
    content = content.replace(old_maint, new_maint)

with open(path, 'w') as f:
    f.write(content)

print("Models patched successfully.")
