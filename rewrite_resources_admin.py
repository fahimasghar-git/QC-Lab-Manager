with open('/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py', 'r') as f:
    text = f.read()

# Remove the broken part manually and insert correctly.
# Let's extract everything before CompetencyRecordAdmin
idx1 = text.find("@admin.register(CompetencyRecord)")
if idx1 != -1:
    head = text[:idx1]
    
    idx2 = text.find("from .models import Supplier, PurchaseRequest")
    tail = text[idx2:]
    
    comp = """@admin.register(CompetencyRecord)
class CompetencyRecordAdmin(ModelAdmin):
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
    with open('/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py', 'w') as f:
        f.write(head + comp + tail)
print("Done")
