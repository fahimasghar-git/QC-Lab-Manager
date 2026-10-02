import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(path, 'r') as f:
    content = f.read()

new_models = """

# QCL-FRM-6.05 Comparative Statement
class ComparativeStatement(models.Model):
    history = HistoricalRecords()
    
    item_name = models.CharField(max_length=200, help_text="Item or Service Name")
    date = models.DateField(auto_now_add=True)
    purchase_demand = models.ForeignKey('PurchaseRequest', on_delete=models.SET_NULL, null=True, blank=True)
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_statements', on_delete=models.RESTRICT, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_statements', on_delete=models.RESTRICT, null=True, blank=True)
    
    def __str__(self):
        return f"CS - {self.item_name} ({self.date})"

class ComparativeStatementSupplier(models.Model):
    statement = models.ForeignKey(ComparativeStatement, on_delete=models.CASCADE, related_name='suppliers')
    supplier_name = models.CharField(max_length=150)
    rate = models.CharField(max_length=100, verbose_name="Rate (RS)")
    quantity = models.CharField(max_length=100)
    delivery_time = models.CharField(max_length=100)
    quality = models.CharField(max_length=150, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    is_selected = models.BooleanField(default=False, verbose_name="Selected Supplier")

# QCL-FRM-6.06 Supplier Evaluation Plan
class SupplierEvaluationPlan(models.Model):
    history = HistoricalRecords()
    
    year = models.CharField(max_length=4, help_text="e.g. 2024")
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_evaluation_plans', on_delete=models.RESTRICT, null=True, blank=True)
    prepared_date = models.DateField(auto_now_add=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_evaluation_plans', on_delete=models.RESTRICT, null=True, blank=True)
    approved_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Supplier Evaluation Plan - {self.year}"

class SupplierEvaluationPlanItem(models.Model):
    plan = models.ForeignKey(SupplierEvaluationPlan, on_delete=models.CASCADE, related_name='items')
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    frequency = models.CharField(max_length=50, default="Annually")
    evaluation_date = models.DateField()
    next_evaluation_date = models.DateField()
    responsibility = models.CharField(max_length=100, default="QCM / Lab Incharge")
    records = models.CharField(max_length=100, default="QCL-FRM-6.03")
"""

content = content + "\n" + new_models

with open(path, 'w') as f:
    f.write(content)
print("Added 6.05 and 6.06 models to resources/models.py")
