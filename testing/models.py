from django.db import models
from simple_history.models import HistoricalRecords

from django.conf import settings
from samples.models import Sample

class Parameter(models.Model):
    name = models.CharField(max_length=100, help_text="e.g., Total Nitrogen, Moisture, pH, Biuret")
    default_unit = models.CharField(max_length=50, default="%")

    def __str__(self):
        return self.name

class TestMethod(models.Model):
    name = models.CharField(max_length=150, help_text="e.g., AOAC 993.13, ISO 5315, In-House SOP-01")
    description = models.TextField(blank=True, null=True)
    is_accredited = models.BooleanField(default=True, help_text="Is this method accredited under ISO 17025?")
    
    def __str__(self):
        return f"{self.name} {'(Accredited)' if self.is_accredited else '(Not Accredited)'}"

class TestResult(models.Model):
    history = HistoricalRecords()

    STATUS_CHOICES = [
        ('PENDING', 'Pending Assignment'),
        ('ASSIGNED', 'Assigned to Analyst'),
        ('IN_PROGRESS', 'In Progress'),
        ('PENDING_VERIFICATION', 'Pending AQCM Verification'),
        ('VERIFIED', 'Verified by AQCM'),
    ]
    
    RESULT_TYPE_CHOICES = [
        ('REGULAR', 'Regular Sample'),
        ('BLANK', 'Method Blank'),
        ('DUPLICATE', 'Duplicate'),
        ('CRM', 'Certified Reference Material (CRM)'),
    ]

    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='test_results', blank=True, null=True, help_text="Blank for standalone QC tests")
    parameter = models.ForeignKey(Parameter, on_delete=models.RESTRICT)
    method = models.ForeignKey(TestMethod, on_delete=models.RESTRICT, blank=True, null=True)
    
    # QC Specific Fields
    result_type = models.CharField(max_length=20, choices=RESULT_TYPE_CHOICES, default='REGULAR')
    parent_result = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, help_text="If Duplicate, select the original TestResult")
    target_value = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, help_text="Expected value for CRMs")
    
    # ISO 17025 Clause 6.4 and 6.5 - Metrological Traceability
    equipment_used = models.ManyToManyField('resources.Equipment', blank=True, help_text="Equipment used for this specific test")
    reagents_used = models.ManyToManyField('resources.ReagentStandard', blank=True, help_text="Standards or reagents used")
    
    # These are blank initially when the sample is just received
    specs = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Min 98%, 10-15 ppm")
    result_value = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    unit = models.CharField(max_length=50, default="%", blank=True, null=True)
    
    # ISO 17025 requires reporting Measurement Uncertainty
    measurement_uncertainty = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, help_text="e.g., 0.05 (will be reported as ± 0.05)")
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='tests_assigned',
        blank=True, null=True,
        help_text="Analyst assigned to perform this parameter"
    )

    # Traceability of testing (Blank initially when requested)
    analyst = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.RESTRICT, 
        related_name='tests_performed',
        blank=True,
        null=True
    )
    tested_at = models.DateTimeField(blank=True, null=True)
    
    # Traceability of review/approval (four-eyes principle)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.RESTRICT, 
        related_name='tests_reviewed',
        blank=True, 
        null=True
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)
    
    remarks = models.TextField(blank=True, null=True, help_text="Deviations from method or QC notes.")

    def __str__(self):
        s_id = self.sample.sample_id if self.sample else f"QC-{self.get_result_type_display()}"
        return f"{s_id} - {self.parameter.name}: {self.result_value} {self.unit}"

    @property
    def qc_recovery_percentage(self):
        if self.result_type == 'CRM' and self.result_value and self.target_value:
            return round((self.result_value / self.target_value) * 100, 2)
        return None

    @property
    def qc_rpd(self):
        # Relative Percent Difference for duplicates
        if self.result_type == 'DUPLICATE' and self.parent_result and self.result_value and self.parent_result.result_value:
            diff = abs(self.result_value - self.parent_result.result_value)
            avg = (self.result_value + self.parent_result.result_value) / 2
            if avg == 0:
                return 0
            return round((diff / avg) * 100, 2)
        return None

    class Meta:
        # We can no longer enforce unique_together = ('sample', 'parameter') if we allow duplicates 
        # on the same sample, unless we remove that constraint or modify it. 
        # Actually, let's just drop the unique constraint for now to allow QC flexibility.
        pass


class MyAssignedTest(TestResult):
    class Meta:
        proxy = True
        verbose_name = 'My Assigned Test'
        verbose_name_plural = 'My Assigned Tests'

