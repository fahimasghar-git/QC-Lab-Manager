import os

file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/testing/models.py'
with open(file_path, 'r') as f:
    content = f.read()

new_field = """    specs = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Min 98%, 10-15 ppm")
    result_value = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)"""

content = content.replace("    result_value = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)", new_field)

with open(file_path, 'w') as f:
    f.write(content)
