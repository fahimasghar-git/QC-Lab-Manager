file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/models.py'
with open(file_path, 'r') as f:
    content = f.read()

# 1. Remove the properties from Client
bad_client = """    @property
    def testing_progress(self):
        total = self.test_results.exclude(result_type='BLANK').exclude(result_type='CRM').count()
        if total == 0:
            return "No parameters assigned"
        verified = self.test_results.filter(status='VERIFIED').count()
        return f"{verified}/{total} Verified"
        
    @property
    def is_ready_for_approval(self):
        total = self.test_results.exclude(result_type='BLANK').exclude(result_type='CRM').count()
        verified = self.test_results.filter(status='VERIFIED').count()
        return total > 0 and total == verified

    def __str__(self):"""

content = content.replace(bad_client, "    def __str__(self):")

# 2. Add them correctly to Sample, along with the new fields
new_sample_fields = """
    # --- QCL-FRM-12.01 (Analysis Request) Fields ---
    priority = models.CharField(max_length=20, choices=(('NORMAL', 'Normal'), ('URGENT', 'Urgent')), default='NORMAL')
    uncertainty_required = models.BooleanField(default=True)
    sample_quantity = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Kg/L")
    packing_condition = models.CharField(max_length=100, blank=True, null=True)
    environmental_conditions = models.CharField(max_length=255, blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    capability_decision = models.CharField(max_length=20, choices=(('ACCEPT', 'Accept'), ('REJECT', 'Reject')), default='ACCEPT')
    rejection_reason = models.TextField(blank=True, null=True)
    
    # --- QCL-FRM-12.03 (Report / CoA) Fields ---
    mfg_date = models.DateField(blank=True, null=True)
    exp_date = models.DateField(blank=True, null=True)
    sample_type_category = models.CharField(max_length=50, choices=(('RAW_MATERIAL', 'Raw Material'), ('BATCH_ANALYSIS', 'Batch Analysis'), ('OUTSIDE_SAMPLE', 'Outside Sample')), default='OUTSIDE_SAMPLE')
    standard_reference = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=150, default="Vital Agri Nutrients (Pvt) Ltd")
    temperature = models.CharField(max_length=50, blank=True, null=True, help_text="Temperature ˚C")
    humidity = models.CharField(max_length=50, blank=True, null=True, help_text="Humidity %")

    @property
    def testing_progress(self):
        total = self.test_results.exclude(result_type='BLANK').exclude(result_type='CRM').count()
        if total == 0:
            return "No parameters assigned"
        verified = self.test_results.filter(status='VERIFIED').count()
        return f"{verified}/{total} Verified"
        
    @property
    def is_ready_for_approval(self):
        total = self.test_results.exclude(result_type='BLANK').exclude(result_type='CRM').count()
        verified = self.test_results.filter(status='VERIFIED').count()
        return total > 0 and total == verified

    def __str__(self):"""

# Find def __str__(self): inside Sample
# Sample class is defined around line 32. Let's just find "    def __str__(self):" after "class Sample"
parts = content.split("class Sample(models.Model):")
sample_part = parts[1]
sample_part = sample_part.replace("    def __str__(self):", new_sample_fields, 1) # Only replace the first occurrence in Sample

with open(file_path, 'w') as f:
    f.write(parts[0] + "class Sample(models.Model):" + sample_part)
