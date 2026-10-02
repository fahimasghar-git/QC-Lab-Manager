file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(file_path, 'r') as f:
    content = f.read()

bad_indent = "            verbose_name = 'CompetencyRecord (QCL-FRM-1.04)'\n        verbose_name_plural = 'CompetencyRecords (QCL-FRM-1.04)'\ndef __str__"
good_indent = "        verbose_name = 'CompetencyRecord (QCL-FRM-1.04)'\n        verbose_name_plural = 'CompetencyRecords (QCL-FRM-1.04)'\n\n    def __str__"
content = content.replace(bad_indent, good_indent)

with open(file_path, 'w') as f:
    f.write(content)
