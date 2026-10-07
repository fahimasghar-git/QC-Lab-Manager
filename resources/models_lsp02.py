from django.db import models
from django.conf import settings

# QCL-FRM-2.02 Training Need Assessment Form
class TrainingNeedAssessment(models.Model):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assessment_year = models.IntegerField()
    amendment_no = models.CharField(max_length=20, blank=True)
    
    score_work_output = models.IntegerField(help_text="Neatness, accuracy, on-time completion (out of 100)")
    score_initiative = models.IntegerField(help_text="Corrective/preventive actions, suggestions")
    score_validation = models.IntegerField(help_text="Validation of Analytical Methods and STM")
    score_equipment = models.IntegerField(help_text="Equipment Operation")
    score_audit = models.IntegerField(help_text="Internal Audit ISO 17025")
    score_sample_handling = models.IntegerField(help_text="Sample Handling")
    score_reporting = models.IntegerField(help_text="Reporting, Opinion and Interpretation")
    
    trainings_required = models.TextField(help_text="List of trainings required, separated by newlines")
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    approval_date = models.DateField(null=True, blank=True)
    
    @property
    def total_percentage(self):
        return sum([
            self.score_work_output, self.score_initiative, self.score_validation,
            self.score_equipment, self.score_audit, self.score_sample_handling, self.score_reporting
        ]) / 7

    class Meta:
        verbose_name = "Training Need Assessment (2.02)"
        verbose_name_plural = "Training Need Assessments (2.02)"

# QCL-FRM-2.03 Annual Training Plan
class AnnualTrainingPlan(models.Model):
    month_year = models.CharField(max_length=50)
    plan_no = models.CharField(max_length=50)
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Annual Training Plan (2.03)"
        verbose_name_plural = "Annual Training Plans (2.03)"

class TrainingPlanItem(models.Model):
    plan = models.ForeignKey(AnnualTrainingPlan, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=255)
    section = models.CharField(max_length=100)
    training_type = models.CharField(max_length=50, choices=[('INTERNAL', 'Internal'), ('EXTERNAL', 'External')])
    duration = models.CharField(max_length=100)
    resource = models.CharField(max_length=100)
    num_personnel = models.IntegerField()
    status = models.CharField(max_length=50)

# QCL-FRM-2.04 Attendance Sheet
class TrainingAttendanceSheet(models.Model):
    reference = models.CharField(max_length=100)
    date_held = models.DateField()
    time_held = models.TimeField()
    venue = models.CharField(max_length=200)
    title = models.CharField(max_length=255)
    
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Attendance Sheet (2.04)"
        verbose_name_plural = "Attendance Sheets (2.04)"

class AttendanceRecord(models.Model):
    sheet = models.ForeignKey(TrainingAttendanceSheet, on_delete=models.CASCADE, related_name='attendees')
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attended = models.BooleanField(default=True)

# QCL-FRM-2.05 Training Evaluation Form
class TrainingEvaluation(models.Model):
    training = models.ForeignKey(TrainingAttendanceSheet, on_delete=models.CASCADE)
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    evaluation_date = models.DateField()
    score = models.IntegerField(help_text="Score or grade")
    remarks = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Training Evaluation (2.05)"
        verbose_name_plural = "Training Evaluations (2.05)"

# QCL-FRM-2.07 Training Feedback Form
class TrainingFeedback(models.Model):
    training = models.ForeignKey(TrainingAttendanceSheet, on_delete=models.CASCADE)
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    instructor_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comments = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Training Feedback (2.07)"
        verbose_name_plural = "Training Feedbacks (2.07)"

# QCL-FRM-2.08 Individual Training Record
class IndividualTrainingRecord(models.Model):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    training_title = models.CharField(max_length=255)
    date_completed = models.DateField()
    result = models.CharField(max_length=100)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Individual Training Record (2.08)"
        verbose_name_plural = "Individual Training Records (2.08)"

# QCL-FRM-2.09 Orientation Plan
class OrientationPlan(models.Model):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    department = models.CharField(max_length=100)
    topics_covered = models.TextField()
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Orientation Plan (2.09)"
        verbose_name_plural = "Orientation Plans (2.09)"

# QCL-FRM-2.10 Competence Reassessment form
class CompetenceReassessment(models.Model):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    reason_for_reassessment = models.TextField()
    outcome = models.CharField(max_length=255)
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Competence Reassessment (2.10)"
        verbose_name_plural = "Competence Reassessments (2.10)"

# QCL-FRM-2.12 Trainer Evaluation Form
class TrainerEvaluation(models.Model):
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluated_as_trainer')
    date = models.DateField()
    knowledge_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    communication_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    overall_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Trainer Evaluation (2.12)"
        verbose_name_plural = "Trainer Evaluations (2.12)"

