import os

file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/models.py'
with open(file_path, 'r') as f:
    content = f.read()

# Add the new fields to Sample model to mirror QCL-FRM-12.01
new_fields = """    # --- QCL-FRM-12.01 (Analysis Request) Fields ---
    customer_name = models.CharField(max_length=150, blank=True, null=True)
    customer_org = models.CharField(max_length=150, blank=True, null=True)
    customer_contact = models.CharField(max_length=50, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    
    batch_no = models.CharField(max_length=50, blank=True, null=True)
    mfg_date = models.DateField(blank=True, null=True)
    exp_date = models.DateField(blank=True, null=True)
    sample_quantity = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Kg/L")
    packing_condition = models.CharField(max_length=100, blank=True, null=True)
    
    priority = models.CharField(max_length=20, choices=(('NORMAL', 'Normal'), ('URGENT', 'Urgent')), default='NORMAL')
    uncertainty_required = models.BooleanField(default=True)
    
    environmental_conditions = models.CharField(max_length=255, blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    
    capability_decision = models.CharField(max_length=20, choices=(('ACCEPT', 'Accept'), ('REJECT', 'Reject')), default='ACCEPT')
    rejection_reason = models.TextField(blank=True, null=True)
    
    # --- QCL-FRM-12.03 (Report / CoA) Fields ---
    sample_type_category = models.CharField(max_length=50, choices=(('RAW_MATERIAL', 'Raw Material'), ('BATCH_ANALYSIS', 'Batch Analysis'), ('OUTSIDE_SAMPLE', 'Outside Sample')), default='OUTSIDE_SAMPLE')
    standard_reference = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=150, default="Vital Agri Nutrients (Pvt) Ltd")
    temperature = models.CharField(max_length=50, blank=True, null=True, help_text="Temperature ˚C")
    humidity = models.CharField(max_length=50, blank=True, null=True, help_text="Humidity %")
    
    # """

content = content.replace("    sample_type = models.CharField(max_length=50, choices=SAMPLE_TYPES)", new_fields + "sample_type = models.CharField(max_length=50, choices=SAMPLE_TYPES)")

with open(file_path, 'w') as f:
    f.write(content)
