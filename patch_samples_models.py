import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/models.py'
with open(path, 'r') as f:
    content = f.read()

pattern = rf"(class SampleReturn\(models\.Model\):.*?)(    class Meta:)"
match = re.search(pattern, content, flags=re.DOTALL)
if match:
    sig_fields = """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_returns', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_returns', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
"""
    new_class = match.group(1) + sig_fields + match.group(2)
    content = content.replace(match.group(0), new_class)
    with open(path, 'w') as f:
        f.write(content)
