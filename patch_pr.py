import re

models_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(models_path, 'r') as f:
    content = f.read()

new_pr = """class PurchaseRequest(models.Model):
    STATUS_CHOICES = (
        ('REQUESTED', 'Requested'),
        ('APPROVED', 'Approved by QCM'),
        ('ORDERED', 'Ordered'),
        ('RECEIVED', 'Received'),
        ('REJECTED', 'Rejected'),
    )
    
    item_description = models.CharField(max_length=255, verbose_name="Item Name")
    specification = models.CharField(max_length=255, blank=True, null=True, help_text="Model, Brand, Quality, Capacity")
    purpose = models.CharField(max_length=255, blank=True, null=True, help_text="Purpose of Purchase")
    
    quantity_required = models.PositiveIntegerField(default=1)
    stock_in_hand = models.PositiveIntegerField(default=0)
    
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchase_requests', on_delete=models.RESTRICT)
    requested_date = models.DateField(auto_now_add=True)
    
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_purchases', on_delete=models.SET_NULL, null=True, blank=True)
    
    history = HistoricalRecords()

    @property
    def net_purchase_required(self):
        return max(0, self.quantity_required - self.stock_in_hand)

    class Meta:
        verbose_name = 'Purchase Request (QCL-FRM-6.07)'
        verbose_name_plural = 'Purchase Requests (QCL-FRM-6.07)'

    def __str__(self):
        return f"PR-{self.id}: {self.item_description} ({self.status})"
"""

content = re.sub(r'class PurchaseRequest\(models\.Model\):.*?def __str__\(self\):\n.*?return .*?\n', new_pr, content, flags=re.DOTALL)

with open(models_path, 'w') as f:
    f.write(content)
