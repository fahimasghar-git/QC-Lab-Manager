import os
import re

admin_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(admin_path, 'r') as f:
    content = f.read()

# Make sure we import the model
content = content.replace("from .models import Supplier", "from .models import Supplier, CompetencyEvaluation")

# Add the admin action and registration
new_admin = """
@admin.register(CompetencyEvaluation)
class CompetencyEvaluationAdmin(ModelAdmin):
    list_display = ('analyst', 'evaluation_date', 'supervisor')
    list_filter = ('evaluation_date', 'analyst')
    search_fields = ('analyst__username', 'supervisor__username')
    actions = ['print_competency_evaluation']

    fieldsets = (
        ('Basic Information (Section A)', {
            'fields': ('analyst', 'supervisor', 'evaluation_date')
        }),
        ('Evaluation Description (Section C)', {
            'fields': (
                'score_analysis_skills', 'score_equipment_handling', 'score_iso_awareness',
                'score_testing_skills', 'score_sample_prep'
            ),
            'description': 'Scale: ND, AC, C, HC, E. (If ND in any parameter, training is required).'
        }),
        ('Remarks & Conclusion', {
            'fields': ('remarks',)
        }),
    )

    @admin.action(description='🖨️ Print Evaluation of Competency (QCL-FRM-2.09)')
    def print_competency_evaluation(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/competency_evaluation_report.html', {'evaluations': queryset})

"""

content += new_admin

with open(admin_path, 'w') as f:
    f.write(content)

print("Admin updated.")
