import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/models.py'
with open(path, 'r') as f:
    content = f.read()

old_rca = 'root_cause_analysis = models.TextField(blank=True, null=True, help_text="Why did this happen? (e.g., 5 Whys)")'
new_rca = """root_cause_analysis = models.TextField(blank=True, null=True, help_text="General RCA / Summary")
    
    # 14.03 Root Cause Analysis (4M) Fields
    rca_man = models.TextField(blank=True, null=True, verbose_name="Man / Personnel")
    rca_method = models.TextField(blank=True, null=True, verbose_name="Method / Procedure")
    rca_machine = models.TextField(blank=True, null=True, verbose_name="Machine / Equipment")
    rca_material = models.TextField(blank=True, null=True, verbose_name="Material / Environment")
    similar_non_conformance = models.BooleanField(default=False, verbose_name="Similar Non-Conformance exist?")
    rca_carried_out_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rca_carried_out', on_delete=models.RESTRICT, null=True, blank=True)
"""

content = content.replace(old_rca, new_rca)

with open(path, 'w') as f:
    f.write(content)

print("Added 14.03 fields to NonConformance.")
