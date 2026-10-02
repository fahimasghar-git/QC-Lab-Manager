with open('resources/models.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="prepared_equipments"' in line: continue
    if 'reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviewed_equipments"' in line: continue
    if 'approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="approved_equipments"' in line: continue
    if 'prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="prepared_competencies"' in line: continue
    if 'checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="checked_competencies"' in line: continue
    if 'approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="approved_competencies"' in line: continue
    new_lines.append(line)

with open('resources/models.py', 'w') as f:
    f.writelines(new_lines)
