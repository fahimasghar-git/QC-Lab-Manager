import sys

def insert_after(file_path, search_str, insert_str):
    with open(file_path, 'r') as f:
        content = f.read()
    if insert_str.strip() in content:
        return
    parts = content.split(search_str)
    if len(parts) == 2:
        new_content = parts[0] + search_str + "\n" + insert_str + parts[1]
        with open(file_path, 'w') as f:
            f.write(new_content)

comp_search = "notes = models.TextField(blank=True, null=True, help_text=\"Reference to training evidence (e.g., passed blind sample)\")"
comp_insert = """
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_competencies', on_delete=models.SET_NULL, null=True, blank=True)
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='checked_competencies', on_delete=models.SET_NULL, null=True, blank=True)
    # approved_by is already authorized_by in CompetencyRecord? Wait, let's just add approved_by explicitly.
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_competencies', on_delete=models.SET_NULL, null=True, blank=True)
"""
insert_after('resources/models.py', comp_search, comp_insert)

