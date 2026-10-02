import re
import os

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(path, 'r') as f:
    content = f.read()

def inject_fields(model_name, sig_fields_str):
    global content
    # Find the end of the class definition before Meta
    pattern = rf"(class {model_name}\(models\.Model\):.*?)(    class Meta:)"
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        new_class_body = match.group(1) + sig_fields_str + "\n" + match.group(2)
        content = content.replace(match.group(0), new_class_body)
    else:
        print(f"Could not find injection point for {model_name}")

inject_fields('CalibrationRecord', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_calibrations', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_calibrations', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_calibrations', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
""")

inject_fields('CompetencyRecord', """
    prepared_at = models.DateTimeField(null=True, blank=True)
    checked_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
""")

inject_fields('CompetencyEvaluation', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_evaluations', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_evaluations', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
""")

inject_fields('ReagentStandard', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_reagents', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_reagents', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_reagents', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
""")

inject_fields('PurchaseRequest', """
    prepared_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
""")

inject_fields('ProductServiceInspection', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_inspections', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_inspections', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_inspections', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
""")

with open(path, 'w') as f:
    f.write(content)
print("Injected into resources/models.py")

