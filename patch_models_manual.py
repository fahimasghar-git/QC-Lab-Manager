path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(path, 'r') as f:
    content = f.read()

old_eq = """    date_put_into_service = models.DateField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')"""
new_eq = """    date_put_into_service = models.DateField(blank=True, null=True)
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_equipments', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_equipments', on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_equipments', on_delete=models.SET_NULL, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')"""
content = content.replace(old_eq, new_eq)

old_comp = """    remarks = models.TextField(blank=True, null=True, help_text="Any comments on the staff's performance")

    class Meta:"""
new_comp = """    remarks = models.TextField(blank=True, null=True, help_text="Any comments on the staff's performance")
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_competencies', on_delete=models.SET_NULL, null=True, blank=True)
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='checked_competencies', on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_competencies', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:"""
content = content.replace(old_comp, new_comp)

with open(path, 'w') as f:
    f.write(content)
print("Manual patch done.")
