import re

model_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(model_path, 'r') as f:
    content = f.read()

# Add evaluated_by and approved_by
if "evaluated_by = " not in content:
    old_fields = """    evaluation_notes = models.TextField(blank=True, null=True, help_text="Notes on supplier quality and performance.")

    history = HistoricalRecords()"""
    
    new_fields = """    evaluation_notes = models.TextField(blank=True, null=True, help_text="Notes on supplier quality and performance.")
    
    evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='evaluated_suppliers', on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_suppliers', on_delete=models.SET_NULL, null=True, blank=True)

    history = HistoricalRecords()"""
    content = content.replace(old_fields, new_fields)
    
    with open(model_path, 'w') as f:
        f.write(content)
    print("Updated Supplier model.")
