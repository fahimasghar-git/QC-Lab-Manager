from django.db import models
from simple_history.models import HistoricalRecords

from django.conf import settings
import uuid

class Client(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name

class Sample(models.Model):
    history = HistoricalRecords()

    STATUS_CHOICES = [
        ('RECEIVED', 'Received (Pending Analysis)'),
        ('IN_PROGRESS', 'In Progress (Testing)'),
        ('PENDING_VERIFICATION', 'Pending Verification (AQCM)'),
        ('PENDING_APPROVAL', 'Pending Approval (QCM)'),
        ('APPROVED', 'Approved (CoA Ready)'),
        ('REJECTED', 'Rejected'),
    ]

    # ISO 17025 requires unique, unambiguous sample identification
    CATEGORY_CHOICES = [
        ('PSQCA', 'PSQCA'),
        ('SFRI', 'SFRI'),
        ('Raw Material', 'Raw Material'),
        ('Outside', 'Outside'),
        ('Third Party', 'Third Party'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Raw Material', help_text="Select sample category for serial numbering")
    sample_id = models.CharField(max_length=50, unique=True, editable=False, verbose_name="AR Serial Number", help_text="Auto-generated Analysis Request Number")
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='samples')
    product_name = models.CharField(max_length=150, help_text="e.g., Urea, DAP, NPK 15-15-15")
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    
    sample_quantity = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 500g, 1L")
    assay = models.CharField(max_length=100, blank=True, null=True, help_text="Assay value for CoA")
    serial_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Category Serial", help_text="Category Serial #")
    
    description = models.TextField(help_text="Physical appearance/condition of the sample upon receipt")
    storage_condition = models.CharField(max_length=100, default="Room Temperature", help_text="e.g., Room Temp, Refrigerated")
    
    # Chain of custody & Workflow details
    received_date = models.DateTimeField(auto_now_add=True)
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='received_samples'
    )
    
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='verified_samples', blank=True, null=True
    )
    verified_at = models.DateTimeField(blank=True, null=True)
    
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='approved_samples', blank=True, null=True
    )
    approved_at = models.DateTimeField(blank=True, null=True)
    
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='RECEIVED')
    rejection_reason = models.CharField(max_length=255, blank=True, null=True, help_text="Reason if rejected")
    
    customer_signature = models.CharField(max_length=100, blank=True, null=True, help_text="Customer/Sender Name")
    
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # 1. Generate Main AR Serial Number (e.g. 1, 2, 3... 10)
        if not self.sample_id or self.sample_id.startswith('QC') or self.sample_id.startswith('FERT'):
            # Find the last sample that has a pure digit sample_id
            last_sample = Sample.objects.order_by('-id').first()
            
            # Since we might have old FERT- or QC records, let's safely get the highest integer
            all_ids = Sample.objects.values_list('sample_id', flat=True)
            valid_nums = [int(i) for i in all_ids if str(i).isdigit()]
            
            if valid_nums:
                new_ar_num = max(valid_nums) + 1
            else:
                new_ar_num = 1
                
            self.sample_id = str(new_ar_num)
            
        # 2. Generate Category Serial Number (e.g. RM001)
        if not self.serial_number:
            prefix_map = {
                'PSQCA': 'PQ',
                'SFRI': 'SF',
                'Raw Material': 'RM',
                'Outside': 'OS',
                'Third Party': 'TP',
            }
            prefix = prefix_map.get(self.category, 'SMP')
            last_cat = Sample.objects.filter(serial_number__startswith=prefix).order_by('-id').first()
            
            if last_cat and last_cat.serial_number and len(last_cat.serial_number) > len(prefix):
                number_part = last_cat.serial_number[len(prefix):]
                if number_part.isdigit():
                    new_cat_num = int(number_part) + 1
                else:
                    new_cat_num = 1
            else:
                new_cat_num = 1
                
            self.serial_number = f"{prefix}{new_cat_num:03d}"
            
        super().save(*args, **kwargs)


    @property
    def testing_progress(self):
        total = self.test_results.exclude(result_type='BLANK').exclude(result_type='CRM').count()
        if total == 0:
            return "No parameters assigned"
        verified = self.test_results.filter(status='VERIFIED').count()
        return f"{verified}/{total} Verified"
        
    @property
    def is_ready_for_approval(self):
        total = self.test_results.exclude(result_type='BLANK').exclude(result_type='CRM').count()
        verified = self.test_results.filter(status='VERIFIED').count()
        return total > 0 and total == verified


    class Meta:
        verbose_name = 'Sample (QCL-FRM-12.01)'
        verbose_name_plural = 'Samples (QCL-FRM-12.01)'


    # --- QCL-FRM-19.01 (Assignment, Summary and Review) Fields ---
    assigned_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    container_type = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Glass Bottle, Plastic Bag")
    
    # --- QCL-FRM-12.01 (Analysis Request) Fields ---
    priority = models.CharField(max_length=20, choices=(('NORMAL', 'Normal'), ('URGENT', 'Urgent')), default='NORMAL')
    uncertainty_required = models.BooleanField(default=True)
    sample_quantity = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Kg/L")
    packing_condition = models.CharField(max_length=100, blank=True, null=True)
    environmental_conditions = models.CharField(max_length=255, blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    capability_decision = models.CharField(max_length=20, choices=(('ACCEPT', 'Accept'), ('REJECT', 'Reject')), default='ACCEPT')
    rejection_reason = models.TextField(blank=True, null=True)
    
    # --- QCL-FRM-12.03 (Report / CoA) Fields ---
    mfg_date = models.DateField(blank=True, null=True)
    exp_date = models.DateField(blank=True, null=True)
    sample_type_category = models.CharField(max_length=50, choices=(('RAW_MATERIAL', 'Raw Material'), ('BATCH_ANALYSIS', 'Batch Analysis'), ('OUTSIDE_SAMPLE', 'Outside Sample')), default='OUTSIDE_SAMPLE')
    standard_reference = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=150, default="Vital Agri Nutrients (Pvt) Ltd")
    temperature = models.CharField(max_length=50, blank=True, null=True, help_text="Temperature ˚C")
    humidity = models.CharField(max_length=50, blank=True, null=True, help_text="Humidity %")

    @property
    def testing_progress(self):
        total = self.test_results.exclude(result_type='BLANK').exclude(result_type='CRM').count()
        if total == 0:
            return "No parameters assigned"
        verified = self.test_results.filter(status='VERIFIED').count()
        return f"{verified}/{total} Verified"
        
    @property
    def is_ready_for_approval(self):
        total = self.test_results.exclude(result_type='BLANK').exclude(result_type='CRM').count()
        verified = self.test_results.filter(status='VERIFIED').count()
        return total > 0 and total == verified

    def __str__(self):
        return f"{self.sample_id} - {self.product_name}"


class SampleReturn(models.Model):
    history = HistoricalRecords()
    
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='returns')
    return_date = models.DateField()
    reason = models.TextField(verbose_name="Reason for sample return")
    

    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_returns', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_returns', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    class Meta:
        verbose_name = 'Sample Return (22.01)'
        verbose_name_plural = 'Sample Returns (22.01)'
        
    def __str__(self):
        return f"Return - {self.sample.sample_id}"
