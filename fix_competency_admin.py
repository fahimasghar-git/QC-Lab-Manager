import re

admin_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(admin_path, 'r') as f:
    content = f.read()

# I will replace the entire CompetencyRecordAdmin class.
# Need to find start and end
start_idx = content.find("class CompetencyRecordAdmin(ModelAdmin):")
if start_idx == -1:
    start_idx = content.find("class CompetencyRecordAdmin")

end_idx = content.find("from .models import Supplier, PurchaseRequest")

new_class = """class CompetencyRecordAdmin(ModelAdmin):
    list_display = ('analyst', 'competency_level', 'total_score', 'status', 'training_date')
    list_filter = ('status', 'analyst')
    search_fields = ('analyst__username', 'test_method__name')
    readonly_fields = ('total_score', 'competency_level')
    actions = ['print_competency_report']

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
    )

    def save_model(self, request, obj, form, change):
        if not change or not getattr(obj, 'authorized_by_id', None):
            obj.authorized_by = request.user
        super().save_model(request, obj, form, change)

    @admin.action(description='🖨️ Print Competency Report (QCL-FRM-1.04)')
    def print_competency_report(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/competency_report.html', {'records': queryset})

"""

if start_idx != -1 and end_idx != -1:
    # First, let's remove any stray print_competency_report at the top of the file
    content = re.sub(r'@admin\.action\(description=\'🖨️ Print Competency Report.*?return render\(.*?\n\n', '', content, flags=re.DOTALL)
    
    # Now replace the class
    new_content = content[:start_idx] + new_class + content[end_idx:]
    with open(admin_path, 'w') as f:
        f.write(new_content)
    print("Fixed admin action.")
else:
    print("Could not find boundaries")
