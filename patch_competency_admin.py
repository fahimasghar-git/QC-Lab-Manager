import re

admin_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(admin_path, 'r') as f:
    content = f.read()

old_comp_admin = """@admin.register(CompetencyRecord)
class CompetencyRecordAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('analyst', 'test_method', 'status', 'training_date')
    list_filter = ('status', 'test_method')
    search_fields = ('analyst__username', 'test_method__name')"""

new_comp_admin = """@admin.register(CompetencyRecord)
class CompetencyRecordAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('analyst', 'competency_level', 'total_score', 'status', 'training_date')
    list_filter = ('status', 'analyst')
    search_fields = ('analyst__username', 'test_method__name')
    readonly_fields = ('total_score', 'competency_level')

    fieldsets = (
        ('Analyst Information', {
            'fields': ('analyst', 'test_method', 'training_date', 'status')
        }),
        ('QCL-FRM-1.04 (Competency Scores 1-4)', {
            'fields': (
                'score_education', 'score_qualification', 'score_experience', 
                'score_training', 'score_technical_knowledge', 'score_skills', 
                'score_challenge_testing', 'score_proficiency_testing'
            ),
            'description': '4 = High Competence | 3 = Partial Competence | 2 = Low Competence | 1 = No Competence'
        }),
        ('Authorization & Approval', {
            'fields': ('total_score', 'competency_level', 'assessor', 'authorized_by', 'comments', 'notes')
        }),
    )"""

content = content.replace(old_comp_admin, new_comp_admin)
with open(admin_path, 'w') as f:
    f.write(content)
print("Admin updated")
