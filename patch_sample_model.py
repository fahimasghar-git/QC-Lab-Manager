import os
import re

file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/models.py'
with open(file_path, 'r') as f:
    content = f.read()

# I want to add property testing_progress to Sample class
# Let's find def __str__(self): in Sample and put it above that.

progress_code = """
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

content = content.replace('    def __str__(self):', progress_code)

with open(file_path, 'w') as f:
    f.write(content)
