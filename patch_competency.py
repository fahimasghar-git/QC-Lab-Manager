import os

resources_models = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(resources_models, 'r') as f:
    content = f.read()

old_comp = """class CompetencyRecord(models.Model):
    STATUS_CHOICES = [
        ('AUTHORIZED', 'Authorized to Perform Test'),
        ('IN_TRAINING', 'In Training (Supervised Only)'),
        ('SUSPENDED', 'Suspended / Revoked'),
    ]

    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='competencies')
    test_method = models.ForeignKey(TestMethod, on_delete=models.CASCADE)
    
    training_date = models.DateField(help_text="Date the training/assessment was completed")
    assessor = models.CharField(max_length=150, help_text="Who conducted the assessment? (e.g., QCM or External Expert)")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_TRAINING')
    comments = models.TextField(blank=True, null=True, help_text="Assessment notes or areas for improvement")

    class Meta:
        unique_together = ('analyst', 'test_method')

        verbose_name = 'CompetencyRecord (QCL-FRM-1.04)'
        verbose_name_plural = 'CompetencyRecords (QCL-FRM-1.04)'

    def __str__(self):
        return f"{self.analyst.username} - {self.test_method.name} ({self.get_status_display()})\"\"\""""

# We'll just write a script to replace the class CompetencyRecord.
import re
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
    test_method = models.ForeignKey('testing.TestMethod', on_delete=models.CASCADE, null=True, blank=True)
    
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
"""

content = re.sub(r'class CompetencyRecord.*?def __str__\(self\):\n.*?return .*?\)\)', new_comp, content, flags=re.DOTALL)
# One slight issue: TestMethod was imported directly, but I changed it to 'testing.TestMethod'. Let's see if that's safe. 
# Previously it was `test_method = models.ForeignKey(TestMethod, on_delete=models.CASCADE)`
# I'll just change it back if needed, but 'testing.TestMethod' avoids circular imports if it was imported differently.
# Wait, testing models are imported at the top? No, they probably are. Let's just use what was there.
content = content.replace("models.ForeignKey('testing.TestMethod'", "models.ForeignKey(TestMethod")

with open(resources_models, 'w') as f:
    f.write(content)

