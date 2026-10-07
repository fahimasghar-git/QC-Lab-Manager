from django.db import models
from django.conf import settings

# QCL-FRM-1.01 Personnel Authorization Permit
class PersonnelAuthorizationPermit(models.Model):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auth_permits')
    issue_date = models.DateField()
    valid_until = models.DateField(null=True, blank=True)
    authorized_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='issued_permits')
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Personnel Authorization Permit (1.01)"
        verbose_name_plural = "Personnel Authorization Permits (1.01)"

# QCL-FRM-1.01A Analyst Authorization For Tests and Instruments
class AnalystAuthorizationTestInstrument(models.Model):
    permit = models.ForeignKey(PersonnelAuthorizationPermit, on_delete=models.CASCADE, related_name='test_authorizations')
    test_or_instrument_name = models.CharField(max_length=255)
    authorization_status = models.CharField(max_length=50, choices=[('AUTHORIZED', 'Authorized'), ('UNDER_SUPERVISION', 'Under Supervision')])
    
    class Meta:
        verbose_name = "Analyst Auth Tests/Instruments (1.01A)"
        verbose_name_plural = "Analyst Auth Tests/Instruments (1.01A)"

# QCL-FRM-1.01B Product and Sample Testing Authorization
class AnalystAuthorizationProduct(models.Model):
    permit = models.ForeignKey(PersonnelAuthorizationPermit, on_delete=models.CASCADE, related_name='product_authorizations')
    product_name = models.CharField(max_length=255)
    authorization_status = models.CharField(max_length=50, choices=[('AUTHORIZED', 'Authorized'), ('UNDER_SUPERVISION', 'Under Supervision')])
    
    class Meta:
        verbose_name = "Product & Sample Auth (1.01B)"
        verbose_name_plural = "Product & Sample Auth (1.01B)"

# Evaluation choices used across C and D
EVAL_CHOICES = [
    ('SATISFACTORY', 'Satisfactory'),
    ('UNSATISFACTORY', 'Unsatisfactory'),
]

# QCL-FRM-1.01C Competency Evaluation Internal Samples
class CompetencyEvalInternalSample(models.Model):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evaluation_date = models.DateField()
    sample_id = models.CharField(max_length=100)
    parameter_tested = models.CharField(max_length=100)
    result_status = models.CharField(max_length=20, choices=EVAL_CHOICES)
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Eval Internal Samples (1.01C)"
        verbose_name_plural = "Eval Internal Samples (1.01C)"

# QCL-FRM-1.01D Competency Evaluation PT Samples
class CompetencyEvalPTSample(models.Model):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evaluation_date = models.DateField()
    pt_round_name = models.CharField(max_length=100)
    parameter_tested = models.CharField(max_length=100)
    z_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    result_status = models.CharField(max_length=20, choices=EVAL_CHOICES)
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Eval PT Samples (1.01D)"
        verbose_name_plural = "Eval PT Samples (1.01D)"

GRADING_CHOICES = [
    ('E', 'Exceptional'),
    ('HC', 'Highly Competent'),
    ('C', 'Competent'),
    ('AC', 'Approaching Competence'),
    ('ND', 'Needs Development'),
]

# QCL-FRM-1.01E Grading Matrix Equipment
class GradingMatrixEquipment(models.Model):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    equipment_name = models.CharField(max_length=100)
    calibration_check = models.CharField(max_length=2, choices=GRADING_CHOICES, default='ND')
    operation_skill = models.CharField(max_length=2, choices=GRADING_CHOICES, default='ND')
    maintenance_skill = models.CharField(max_length=2, choices=GRADING_CHOICES, default='ND')
    overall_grade = models.CharField(max_length=2, choices=GRADING_CHOICES, default='ND')
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Grading Matrix Equipment (1.01E)"
        verbose_name_plural = "Grading Matrix Equipment (1.01E)"

# QCL-FRM-1.01F Grading Matrix Product
class GradingMatrixProduct(models.Model):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    product_category = models.CharField(max_length=100)
    sample_prep_skill = models.CharField(max_length=2, choices=GRADING_CHOICES, default='ND')
    testing_skill = models.CharField(max_length=2, choices=GRADING_CHOICES, default='ND')
    overall_grade = models.CharField(max_length=2, choices=GRADING_CHOICES, default='ND')
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Grading Matrix Product (1.01F)"
        verbose_name_plural = "Grading Matrix Product (1.01F)"

# QCL-FRM-1.01G Grading Matrix Document
class GradingMatrixDocument(models.Model):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    document_comprehension = models.CharField(max_length=2, choices=GRADING_CHOICES, default='ND')
    record_keeping = models.CharField(max_length=2, choices=GRADING_CHOICES, default='ND')
    iso_awareness = models.CharField(max_length=2, choices=GRADING_CHOICES, default='ND')
    overall_grade = models.CharField(max_length=2, choices=GRADING_CHOICES, default='ND')
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Grading Matrix Document (1.01G)"
        verbose_name_plural = "Grading Matrix Document (1.01G)"

# QCL-FRM-1.02 List of Authorized Analyst / Staff
class AuthorizedAnalystList(models.Model):
    revision_number = models.CharField(max_length=20)
    date_issued = models.DateField()
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    file_attachment = models.FileField(upload_to='iso_personnel/', blank=True, null=True)
    
    class Meta:
        verbose_name = "List of Authorized Analysts (1.02)"
        verbose_name_plural = "List of Authorized Analysts (1.02)"

# QCL-FRM-1.03 List of Technical Personnel
class TechnicalPersonnelList(models.Model):
    revision_number = models.CharField(max_length=20)
    date_issued = models.DateField()
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    file_attachment = models.FileField(upload_to='iso_personnel/', blank=True, null=True)
    
    class Meta:
        verbose_name = "List of Technical Personnel (1.03)"
        verbose_name_plural = "List of Technical Personnel (1.03)"

