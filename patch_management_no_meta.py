import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/models.py'
with open(path, 'r') as f:
    content = f.read()

def append_to_class(model_name, fields):
    global content
    # Find the class and append before the next class or end of file
    pattern = rf"(class {model_name}\(models\.Model\):.*?)(?=\nclass |\Z)"
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        new_block = match.group(1) + fields + "\n"
        content = content.replace(match.group(1), new_block)

append_to_class('ManagementReview', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
""")

append_to_class('LabCleaningInspection', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_cleanings', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_cleanings', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_cleanings', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES_SIG = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES_SIG, default='DRAFT')
""")

append_to_class('CustomerFeedback', """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_feedbacks', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_feedbacks', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_feedbacks', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES_SIG = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES_SIG, default='DRAFT')
""")

with open(path, 'w') as f:
    f.write(content)
print("Appended fields successfully.")
