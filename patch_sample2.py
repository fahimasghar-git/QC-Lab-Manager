import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/models.py'
with open(path, 'r') as f: content = f.read()
if "assay =" not in content:
    content = content.replace('serial_number = models.CharField', 'assay = models.CharField(max_length=100, blank=True, null=True, help_text="Assay value for CoA")\n    serial_number = models.CharField')
    with open(path, 'w') as f: f.write(content)
    print("Added assay")
