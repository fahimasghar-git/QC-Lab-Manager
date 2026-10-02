import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(path, 'r') as f:
    content = f.read()

old_fields = """    certificate_reference = models.CharField(max_length=150, blank=True, null=True, help_text="CoA number provided by the manufacturer")"""

new_fields = """    certificate_reference = models.CharField(max_length=150, blank=True, null=True, help_text="CoA number provided by the manufacturer")
    
    # Fields for QCL-FRM-5.01 (CRM List)
    is_crm = models.BooleanField(default=False, verbose_name="Is Certified Reference Material (CRM)")
    catalog_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cat No.")
    traceability = models.CharField(max_length=150, blank=True, null=True, verbose_name="Traceability (e.g., NIST)")
    quantity = models.CharField(max_length=50, blank=True, null=True, verbose_name="Quantity")
"""

content = content.replace(old_fields, new_fields)

with open(path, 'w') as f:
    f.write(content)
print("Added CRM fields to ReagentStandard.")
