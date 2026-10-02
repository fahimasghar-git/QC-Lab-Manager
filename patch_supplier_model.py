import os

file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(file_path, 'r') as f:
    content = f.read()

new_fields = """    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # QCL-FRM-6.03 Fields
    evaluation_type = models.CharField(max_length=50, choices=[('NEW', 'New Supplier'), ('EXISTING', 'Existing Supplier Re-evaluation')], default='NEW')
    
    # Rating 0-3
    score_market_image = models.IntegerField(default=0, help_text="Market Image and Reputation (0-3)")
    score_market_share = models.IntegerField(default=0, help_text="Market Share (0-3)")
    score_technical_capacity = models.IntegerField(default=0, help_text="Technical Capacity (0-3)")
    score_lead_time = models.IntegerField(default=0, help_text="Lead Time (0-3)")
    score_product_quality = models.IntegerField(default=0, help_text="Product Quality/Services (0-3)")
    score_order_processing = models.IntegerField(default=0, help_text="Order Processing (0-3)")
    score_fulfill_requirements = models.IntegerField(default=0, help_text="Fulfill Technical Requirement (0-3)")
    
    sample_approved_by_qc = models.CharField(max_length=10, choices=[('YES', 'Yes'), ('NO', 'No'), ('NA', 'N/A')], default='NA')
    
    decision = models.CharField(max_length=20, choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('CONTINUE', 'Continue (Existing)')], default='APPROVED')
    
    remarks = models.TextField(blank=True, null=True)

    @property
    def total_score(self):
        return sum([self.score_market_image, self.score_market_share, self.score_technical_capacity, self.score_lead_time, self.score_product_quality, self.score_order_processing, self.score_fulfill_requirements])
        
    @property
    def grading(self):
        total = self.total_score
        if total <= 6: return "Poor"
        if total <= 12: return "Fair"
        if total <= 18: return "Good"
        return "Excellence"

"""

content = content.replace("    phone = models.CharField(max_length=20, blank=True, null=True)", new_fields)

with open(file_path, 'w') as f:
    f.write(content)
