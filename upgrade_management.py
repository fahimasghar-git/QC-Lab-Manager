import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/models.py'
with open(path, 'r') as f:
    content = f.read()

def inject_fields(model_name, sig_fields_str):
    global content
    pattern = rf"(class {model_name}\(models\.Model\):.*?)(    class Meta:)"
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        new_class_body = match.group(1) + sig_fields_str + "\n" + match.group(2)
        content = content.replace(match.group(0), new_class_body)
    else:
        print(f"Could not find injection point for {model_name}")

inject_fields('Document', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_documents', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_documents', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    doc_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
""")

inject_fields('NonConformance', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_ncs', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_ncs', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
""")

inject_fields('RecordArchive', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_archives', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_archives', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_archives', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
""")

inject_fields('InternalAudit', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_audits', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_audits', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_audits', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
""")

inject_fields('Risk', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_risks', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_risks', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_risks', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
""")

inject_fields('ManagementReview', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
""")

inject_fields('LabCleaningInspection', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_cleanings', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_cleanings', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_cleanings', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
""")

inject_fields('CustomerFeedback', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_feedbacks', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_feedbacks', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_feedbacks', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
""")

with open(path, 'w') as f:
    f.write(content)
print("Injected into management/models.py")

