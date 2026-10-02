import os

resources_models = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(resources_models, 'r') as f:
    content = f.read()

start_idx = content.find("class CompetencyRecord(models.Model):")
end_idx = content.find("class ReagentStandard(models.Model):")

new_comp = """class CompetencyRecord(models.Model):
    SCORE_CHOICES = [
        (4, '4 - High Competence (Completes task independently)'),
        (3, '3 - Partial Competence (Need occasional support)'),
        (2, '2 - Low Competence (Needs ongoing support)'),
        (1, '1 - No Competence (Needs Training & direction)'),
    ]

    STATUS_CHOICES = [
        ('AUTHORIZED', 'Authorized to Perform Test'),
        ('IN_TRAINING', 'In Training (Supervised Only)'),
        ('SUSPENDED', 'Suspended / Revoked'),
    ]

    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='competencies')
    test_method = models.ForeignKey(TestMethod, on_delete=models.CASCADE, null=True, blank=True)
    
    training_date = models.DateField(help_text="Date the training/assessment was completed")
    assessor = models.CharField(max_length=150, help_text="Who conducted the assessment? (e.g., QCM or External Expert)")
    
    # QCL-FRM-1.04 Exact Fields
    score_education = models.IntegerField(choices=SCORE_CHOICES, default=1)
    score_qualification = models.IntegerField(choices=SCORE_CHOICES, default=1)
    score_experience = models.IntegerField(choices=SCORE_CHOICES, default=1)
    score_training = models.IntegerField(choices=SCORE_CHOICES, default=1)
    score_technical_knowledge = models.IntegerField(choices=SCORE_CHOICES, default=1)
    score_skills = models.IntegerField(choices=SCORE_CHOICES, default=1)
    score_challenge_testing = models.IntegerField(choices=SCORE_CHOICES, default=1)
    score_proficiency_testing = models.IntegerField(choices=SCORE_CHOICES, default=1)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_TRAINING')
    comments = models.TextField(blank=True, null=True, help_text="Assessment notes or areas for improvement")

    authorized_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.RESTRICT, 
        related_name='authorizations_granted',
        help_text="The Lab Manager or QCM who authorized this analyst",
        null=True, blank=True
    )
    notes = models.TextField(blank=True, null=True, help_text="Reference to training evidence (e.g., passed blind sample)")

    @property
    def total_score(self):
        return sum([
            self.score_education, self.score_qualification, self.score_experience, 
            self.score_training, self.score_technical_knowledge, self.score_skills, 
            self.score_challenge_testing, self.score_proficiency_testing
        ])

    @property
    def competency_level(self):
        avg = self.total_score / 8
        if avg >= 3.5: return "High Competence"
        if avg >= 2.5: return "Partial Competence"
        if avg >= 1.5: return "Low Competence"
        return "No Competence"

    class Meta:
        verbose_name = 'Competency Monitoring (QCL-FRM-1.04)'
        verbose_name_plural = 'Competency Monitoring (QCL-FRM-1.04)'

    def __str__(self):
        return f"{self.analyst.username} - Score: {self.total_score}/32 ({self.get_status_display()})"

# --- NEW ISO 17025 CLAUSE 6.5 METROLOGICAL TRACEABILITY ---

"""

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_comp + content[end_idx + len("class ReagentStandard(models.Model):\n"):]
    # Wait, the end_idx finds "class ReagentStandard". I want to preserve ReagentStandard!
    content = content[:start_idx] + new_comp + content[end_idx:]

with open(resources_models, 'w') as f:
    f.write(content)

