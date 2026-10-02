import os

resources_models = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(resources_models, 'r') as f:
    content = f.read()

# We will inject the new CompetencyEvaluation model right after CompetencyRecord
new_model = """
class CompetencyEvaluation(models.Model):
    SCALE_CHOICES = [
        ('E', 'Exceptional (Hold Full Command, Can Supervise)'),
        ('HC', 'Highly Competent (Can Supervise Lab Activities)'),
        ('C', 'Competent (Can Work Independently)'),
        ('AC', 'Approaching Competence (Can Work Under Supervision)'),
        ('ND', 'Needs Development (Lacks Basics, Needs Training)'),
    ]

    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluations')
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.RESTRICT, 
        related_name='evaluations_conducted',
        help_text="Supervisor / Evaluator"
    )
    evaluation_date = models.DateField(help_text="Date of Supervision")

    score_analysis_skills = models.CharField(max_length=2, choices=SCALE_CHOICES, default='ND', verbose_name="Analysis Skills")
    score_equipment_handling = models.CharField(max_length=2, choices=SCALE_CHOICES, default='ND', verbose_name="Lab Equipment Handling")
    score_iso_awareness = models.CharField(max_length=2, choices=SCALE_CHOICES, default='ND', verbose_name="Awareness ISO 17025: 2023")
    score_testing_skills = models.CharField(max_length=2, choices=SCALE_CHOICES, default='ND', verbose_name="Testing Skills")
    score_sample_prep = models.CharField(max_length=2, choices=SCALE_CHOICES, default='ND', verbose_name="Sample Preparation Skills")

    remarks = models.TextField(blank=True, null=True, help_text="Remarks / Comments")

    class Meta:
        verbose_name = 'Competency Evaluation (QCL-FRM-2.09)'
        verbose_name_plural = 'Competency Evaluations (QCL-FRM-2.09)'

    def __str__(self):
        return f"Evaluation: {self.analyst.username} on {self.evaluation_date}"
"""

# Find where CompetencyRecord ends. We'll find "# --- NEW ISO 17025 CLAUSE 6.5"
marker = "# --- NEW ISO 17025 CLAUSE 6.5 METROLOGICAL TRACEABILITY ---"
content = content.replace(marker, new_model + "\n" + marker)

with open(resources_models, 'w') as f:
    f.write(content)

print("QCL-FRM-2.09 model added.")
