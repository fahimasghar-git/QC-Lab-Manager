import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/models.py'
with open(path, 'r') as f:
    content = f.read()

old_sample = """    batch_number = models.CharField(max_length=100, blank=True, null=True)
    
    description = models.TextField(help_text="Physical appearance/condition of the sample upon receipt")"""

new_sample = """    batch_number = models.CharField(max_length=100, blank=True, null=True)
    
    sample_quantity = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 500g, 1L")
    serial_number = models.CharField(max_length=50, blank=True, null=True, help_text="Serial # for Analysis Request")
    
    description = models.TextField(help_text="Physical appearance/condition of the sample upon receipt")"""

content = content.replace(old_sample, new_sample)

old_sample_status = """    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='RECEIVED')
    notes = models.TextField(blank=True, null=True)"""

new_sample_status = """    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='RECEIVED')
    rejection_reason = models.CharField(max_length=255, blank=True, null=True, help_text="Reason if rejected")
    
    customer_signature = models.CharField(max_length=100, blank=True, null=True, help_text="Customer/Sender Name")
    
    notes = models.TextField(blank=True, null=True)"""

content = content.replace(old_sample_status, new_sample_status)

with open(path, 'w') as f:
    f.write(content)
print("Sample model patched.")
