from django.db import models
from simple_history.models import HistoricalRecords

from django.conf import settings
from .approval_utils import ISOApprovalModel
from testing.models import TestMethod

class Equipment(models.Model):
    history = HistoricalRecords()

    STATUS_CHOICES = [
        ('ACTIVE', 'Active / In Use'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('OUT_OF_SERVICE', 'Out of Service (Do Not Use)'),
        ('DECOMMISSIONED', 'Decommissioned'),
    ]

    name = models.CharField(max_length=150, help_text="e.g., Analytical Balance, UV-Vis Spectrophotometer")
    identification_no = models.CharField(max_length=50, blank=True, null=True, help_text="Internal ID e.g., EQ-01")
    manufacturer = models.CharField(max_length=150, blank=True, null=True)
    model_number = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, unique=True)
    
    operating_range = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 0-200g, 190-1100nm")
    location = models.CharField(max_length=100, help_text="Where is the equipment located?", blank=True, null=True)
    
    date_received = models.DateField(blank=True, null=True)
    date_put_into_service = models.DateField(blank=True, null=True)
    
    calibration_frequency = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Annually, 6 Months")
    maintenance_frequency = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Weekly, Monthly")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_equipments', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_equipments', on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_equipments', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    DIGITAL_STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    signature_status = models.CharField(max_length=20, choices=DIGITAL_STATUS_CHOICES, default='DRAFT')



    class Meta:
        verbose_name = 'Equipment (QCL-FRM-4.02)'
        verbose_name_plural = 'Equipments (QCL-FRM-4.02)'

    def __str__(self):
        return f"{self.name} ({self.identification_no or self.serial_number})"

class CalibrationRecord(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='calibrations')
    calibration_date = models.DateField()
    next_due_date = models.DateField(help_text="When is the next calibration due?")
    
    performed_by = models.CharField(max_length=150, help_text="Name of internal staff or external vendor")
    certificate_number = models.CharField(max_length=100, blank=True, null=True)
    
    passed = models.BooleanField(default=True, help_text="Did the equipment pass calibration?")
    notes = models.TextField(blank=True, null=True, help_text="Details of adjustments or maintenance performed")




    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_calibrations', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_calibrations', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_calibrations', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    class Meta:
        verbose_name = 'CalibrationRecord (QCL-FRM-4.04)'
        verbose_name_plural = 'CalibrationRecords (QCL-FRM-4.04)'

    def __str__(self):
        return f"Cal: {self.equipment.name} on {self.calibration_date}"


class EquipmentMaintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenances')
    maintenance_date = models.DateField()
    
    parts_repaired_replaced = models.CharField(max_length=255, blank=True, null=True, help_text="If any")
    maintenance_by = models.CharField(max_length=100, help_text="Who performed the maintenance?")
    remarks = models.TextField(blank=True, null=True)
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_maintenances', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_maintenances', on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_maintenances', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')


    class Meta:
        verbose_name = 'Maintenance Record (QCL-FRM-4.03)'
        verbose_name_plural = 'Maintenance Records (QCL-FRM-4.03)'

    def __str__(self):
        return f"Maintenance: {self.equipment.name} on {self.maintenance_date}"

class CompetencyRecord(models.Model):
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
    assessor = models.CharField(max_length=150, blank=True, null=True, help_text="Who conducted the assessment? (e.g., QCM or External Expert)")
    
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

    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_competencies', on_delete=models.SET_NULL, null=True, blank=True)
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='checked_competencies', on_delete=models.SET_NULL, null=True, blank=True)
    # approved_by is already authorized_by in CompetencyRecord? Wait, let's just add approved_by explicitly.
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_competencies', on_delete=models.SET_NULL, null=True, blank=True)


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



    prepared_at = models.DateTimeField(null=True, blank=True)
    checked_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    class Meta:
        verbose_name = 'Competency Monitoring (QCL-FRM-1.04)'
        verbose_name_plural = 'Competency Monitoring (QCL-FRM-1.04)'

    def __str__(self):
        return f"{self.analyst.username} - Score: {self.total_score}/32 ({self.get_status_display()})"


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
    
    manager_qc = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='manager_evaluations', on_delete=models.SET_NULL, null=True, blank=True)



    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_evaluations', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_evaluations', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    class Meta:
        verbose_name = 'Competency Evaluation (QCL-FRM-2.09)'
        verbose_name_plural = 'Competency Evaluations (QCL-FRM-2.09)'

    def __str__(self):
        return f"Evaluation: {self.analyst.username} on {self.evaluation_date}"

# --- NEW ISO 17025 CLAUSE 6.5 METROLOGICAL TRACEABILITY ---

class ReagentStandard(models.Model):
    history = HistoricalRecords()

    STATUS_CHOICES = [
        ('QUARANTINED', 'Quarantined (Pending QC Verification)'),
        ('APPROVED', 'Approved for Use'),
        ('EXPIRED', 'Expired (Do Not Use)'),
        ('DEPLETED', 'Depleted / Discarded'),
    ]

    name = models.CharField(max_length=150, help_text="e.g., 0.1N Sulfuric Acid, Certified Reference Material (CRM)")
    lot_number = models.CharField(max_length=100)
    supplier = models.CharField(max_length=150)
    
    receipt_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='QUARANTINED')
    
    certificate_reference = models.CharField(max_length=150, blank=True, null=True, help_text="CoA number provided by the manufacturer")
    
    # Fields for QCL-FRM-5.01 (CRM List)
    is_crm = models.BooleanField(default=False, verbose_name="Is Certified Reference Material (CRM)")
    catalog_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cat No.")
    traceability = models.CharField(max_length=150, blank=True, null=True, verbose_name="Traceability (e.g., NIST)")
    quantity = models.CharField(max_length=50, blank=True, null=True, verbose_name="Quantity")

    
    def __str__(self):
        return f"{self.name} (Lot: {self.lot_number})"



    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_reagents', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_reagents', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_reagents', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    class Meta:
        unique_together = ('name', 'lot_number')

        verbose_name = 'CRM / Reagent List (QCL-FRM-5.01)'
        verbose_name_plural = 'CRM / Reagent Lists (QCL-FRM-5.01)'

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    requirements_from_supplier = models.TextField(blank=True, null=True, help_text="Range of products/services required")
    
    # --- QCL-FRM-6.01 Selection Criteria ---
    # General
    crit_1_registered = models.BooleanField(default=False, verbose_name="Supplier is legally registered")
    crit_1_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    crit_2_market_1yr = models.BooleanField(default=False, verbose_name="At least 1 year in market")
    crit_2_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    crit_3_offers_range = models.BooleanField(default=False, verbose_name="Offers required range of products/services")
    crit_3_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # Equipment
    crit_4_equipment_docs = models.BooleanField(default=False, verbose_name="Fulfills tech specs & provides docs (manuals/training)")
    crit_4_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # Calibration
    crit_5_calibration_traceability = models.BooleanField(default=False, verbose_name="Capability for traceability, uncertainty, range")
    crit_5_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    crit_6_iso17025 = models.BooleanField(default=False, verbose_name="Accredited on ISO/IEC 17025")
    crit_6_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # PT Services
    crit_7_iso17043 = models.BooleanField(default=False, verbose_name="Accredited for PT services (ISO/IEC 17043)")
    crit_7_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # Training
    crit_8_training_exp = models.BooleanField(default=False, verbose_name="Experience & Qualification of Trainers (PNAC preferred)")
    crit_8_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # Chemicals
    crit_9_msds = models.BooleanField(default=False, verbose_name="Provides supporting docs / MSDS")
    crit_9_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # CRM
    crit_10_crm_coa = models.BooleanField(default=False, verbose_name="Provides CoA & uncertainty (ISO/IEC 17034 certified)")
    crit_10_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # 6.01 Approval
    selection_evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="supplier_selections_evaluated", verbose_name="Selection Evaluator"
    )

    # --- QCL-FRM-6.03 Fields ---
    evaluation_type = models.CharField(max_length=50, choices=[('NEW', 'New Supplier'), ('EXISTING', 'Existing Supplier Re-evaluation')], default='NEW')
    
    # Rating 0-3
    score_market_image = models.IntegerField(default=0, help_text="Market Image and Reputation (0-3)")
    score_market_share = models.IntegerField(default=0, help_text="Market Share (0-3)")
    score_technical_capacity = models.IntegerField(default=0, help_text="Technical Capacity (0-3)")
    score_lead_time = models.IntegerField(default=0, help_text="Lead Time (0-3)")
    score_product_quality = models.IntegerField(default=0, help_text="Product Quality/Services (0-3)")
    score_order_processing = models.IntegerField(default=0, help_text="Order Processing (0-3)")
    score_fulfill_requirements = models.IntegerField(default=0, help_text="Fulfill Technical Requirement (0-3)")
    
    sample_approved_by_qc = models.CharField(max_length=10, choices=[('YES', 'Yes'), ('NO', 'No'), ('NA', 'N/A')], default='NA')
    
    decision = models.CharField(max_length=20, choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('CONTINUE', 'Continue (Existing)')], default='APPROVED')
    
    remarks = models.TextField(blank=True, null=True)

    @property
    def total_score(self):
        return sum([self.score_market_image, self.score_market_share, self.score_technical_capacity, self.score_lead_time, self.score_product_quality, self.score_order_processing, self.score_fulfill_requirements])
        
    @property
    def grading(self):
        total = self.total_score
        if total <= 6: return "Poor"
        if total <= 12: return "Fair"
        if total <= 18: return "Good"
        return "Excellence"


    
    # ISO 17025 Clause 6.6 requires evaluating suppliers
    is_approved = models.BooleanField(default=False)
    last_evaluation_date = models.DateField(blank=True, null=True)
    next_evaluation_date = models.DateField(blank=True, null=True)
    evaluation_notes = models.TextField(blank=True, null=True, help_text="Notes on supplier quality and performance.")
    
    evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='evaluated_suppliers', on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_suppliers', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    history = HistoricalRecords()



    class Meta:
        verbose_name = 'Supplier (QCL-FRM-6.03)'
        verbose_name_plural = 'Suppliers (QCL-FRM-6.03)'

    def __str__(self):
        status = "✅ Approved" if self.is_approved else "❌ Not Approved"
        return f"{self.name} ({status})"

class PurchaseRequest(models.Model):
    STATUS_CHOICES = (
        ('REQUESTED', 'Requested'),
        ('APPROVED', 'Approved by QCM'),
        ('ORDERED', 'Ordered'),
        ('RECEIVED', 'Received'),
        ('REJECTED', 'Rejected'),
    )
    
    item_description = models.CharField(max_length=255, verbose_name="Item Name")
    specification = models.CharField(max_length=255, blank=True, null=True, help_text="Model, Brand, Quality, Capacity")
    purpose = models.CharField(max_length=255, blank=True, null=True, help_text="Purpose of Purchase")
    
    quantity_required = models.PositiveIntegerField(default=1)
    stock_in_hand = models.PositiveIntegerField(default=0)
    
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    
    spd_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="SPD No")
    insp_mints_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="Insp Mints NO & Date")
    service_call_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="Service Call No & Date")
    store_keeper = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='store_keeper_purchases', on_delete=models.SET_NULL, null=True, blank=True)
    
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchase_requests', on_delete=models.RESTRICT)
    requested_date = models.DateField(auto_now_add=True)
    
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_purchases', on_delete=models.SET_NULL, null=True, blank=True)
    
    history = HistoricalRecords()

    @property
    def net_purchase_required(self):
        return max(0, self.quantity_required - self.stock_in_hand)



    prepared_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    class Meta:
        verbose_name = 'Purchase Request (QCL-FRM-6.07)'
        verbose_name_plural = 'Purchase Requests (QCL-FRM-6.07)'

    def __str__(self):
        return f"PR-{self.id}: {self.item_description} ({self.status})"

class ProductServiceInspection(models.Model):
    INSPECTION_TYPE_CHOICES = [('PRODUCT', 'Products'), ('SERVICE', 'Services')]
    PROVIDER_STATUS_CHOICES = [('NEW', 'Newly engaged'), ('EXISTING', 'Pre-existing')]
    STATUS_CHOICES = [('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')]

    inspection_type = models.CharField(max_length=20, choices=INSPECTION_TYPE_CHOICES)
    description = models.CharField(max_length=200, verbose_name="Products/Services")
    external_provider = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='inspections')
    provider_status = models.CharField(max_length=20, choices=PROVIDER_STATUS_CHOICES)
    
    gate_pass_no = models.CharField(max_length=50, blank=True, null=True)
    pr_po_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="PR No./PO No.")
    invoice_no = models.CharField(max_length=50, blank=True, null=True)
    date_of_receipt = models.DateField()
    
    # Checkboxes/Remarks - Products
    prod_coa_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="Product COA Remarks")
    prod_spec_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="Specification Remarks")
    prod_qty_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="Quantity Remarks")
    prod_lot_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="Verification of Lot No. Remarks")
    prod_mfg_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="MFG Date Remarks")
    prod_exp_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="EXP Date Remarks")
    prod_model_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="Model/Make Remarks")
    
    # Checkboxes/Remarks - Services
    srv_traceability_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="Traceability of accreditation Remarks")
    srv_scope_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="Scope of Accreditation Remarks")
    srv_training_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="Traceability of Training Remarks")
    srv_response_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="Response to queries Remarks")
    srv_skills_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="Trainer/engineer skills Remarks")
    srv_validity_remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name="Validity of certificate Remarks")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_inspections', on_delete=models.RESTRICT, null=True, blank=True)


    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_inspections', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_inspections', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_inspections', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    class Meta:
        verbose_name = 'Inspection (QCL-FRM-6.08)'
        verbose_name_plural = 'Inspections (QCL-FRM-6.08)'

    def __str__(self):
        return f"Inspection: {self.description} ({self.get_status_display()})"


class PersonnelAuthorization(models.Model):
    history = HistoricalRecords()

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authorization_permit')
    employee_code = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    
    # 1.01 Instrument Operation
    op_flame_photometer = models.BooleanField(default=False, verbose_name="Operation of Flame Photometer")
    op_uv_vis = models.BooleanField(default=False, verbose_name="Operation of UV-Visible Spectrophotometer")
    op_karl_fischer = models.BooleanField(default=False, verbose_name="Operation of Karl Fischer")
    op_kjeldhals = models.BooleanField(default=False, verbose_name="Operation of Kjeldhal’s Apparatus")
    op_furnace = models.BooleanField(default=False, verbose_name="Operation of Furnace")
    op_ph_meter = models.BooleanField(default=False, verbose_name="Operation of pH Meter")
    op_tds_meter = models.BooleanField(default=False, verbose_name="Operation of TDS Meter")
    op_analytical_balance = models.BooleanField(default=False, verbose_name="Operation of Analytical Balance")
    
    # 1.01 Tests & Parameters
    test_loi = models.BooleanField(default=False, verbose_name="Loss on Ignition")
    test_density = models.BooleanField(default=False, verbose_name="Density Test")
    test_ph = models.BooleanField(default=False, verbose_name="pH Test")
    test_conductivity = models.BooleanField(default=False, verbose_name="Conductivity Test")
    test_tds = models.BooleanField(default=False, verbose_name="TDS Test")
    test_lod = models.BooleanField(default=False, verbose_name="Loss on Drying")
    test_weighing = models.BooleanField(default=False, verbose_name="Weighing")
    test_sieve = models.BooleanField(default=False, verbose_name="Sieve Test")
    test_calcium = models.BooleanField(default=False, verbose_name="Calcium test")
    test_sulfur = models.BooleanField(default=False, verbose_name="Sulfur/Sulfate Test")
    test_nitrogen = models.BooleanField(default=False, verbose_name="Nitrogen Test")
    test_titrations = models.BooleanField(default=False, verbose_name="Manual Titrations")
    test_humic_acid = models.BooleanField(default=False, verbose_name="Humic Acid Test")
    test_phosphorus = models.BooleanField(default=False, verbose_name="Phosphorus Testing")
    test_toc = models.BooleanField(default=False, verbose_name="Total Organic Carbon")
    test_cn_ratio = models.BooleanField(default=False, verbose_name="C/N Ratio Calculation")
    test_organic_matter = models.BooleanField(default=False, verbose_name="Organic Matter")
    test_cec = models.BooleanField(default=False, verbose_name="CEC")
    test_sodium = models.BooleanField(default=False, verbose_name="Sodium Test")
    test_zinc = models.BooleanField(default=False, verbose_name="Zinc Test")
    test_boron = models.BooleanField(default=False, verbose_name="Boron Analysis")
    test_copper = models.BooleanField(default=False, verbose_name="Copper Test")
    test_moisture = models.BooleanField(default=False, verbose_name="Moisture Test")
    
    # 1.01 Quality & Lab Activities
    act_environmental = models.BooleanField(default=False, verbose_name="Monitoring Environmental Conditions")
    act_intermediate_checks = models.BooleanField(default=False, verbose_name="Perform the Intermediate Checks")
    act_control_chart = models.BooleanField(default=False, verbose_name="Prepare Control Chart")
    act_sample_receiving = models.BooleanField(default=False, verbose_name="Sample Receiving")
    act_method_validation = models.BooleanField(default=False, verbose_name="Method Validation/Verification")
    act_sample_handling = models.BooleanField(default=False, verbose_name="Sample Handling")
    act_report_prep = models.BooleanField(default=False, verbose_name="Report Preparation")
    act_review_reports = models.BooleanField(default=False, verbose_name="Preparing/Review the Analysis Reports")
    act_measurement_uncertainty = models.BooleanField(default=False, verbose_name="Measurements of Uncertainty")
    act_internal_auditing = models.BooleanField(default=False, verbose_name="Internal Auditing")
    act_training_lms = models.BooleanField(default=False, verbose_name="Training of Lab Staff on LMS 17025:2017")
    act_prep_procedures = models.BooleanField(default=False, verbose_name="Preparation and Reviewing of Procedures/Other Documents")
    act_approve_reports = models.BooleanField(default=False, verbose_name="Preparation, Reviewing and Approved of Reports/Other Documents")
    act_prep_release_slip = models.BooleanField(default=False, verbose_name="Preparation and Review/Verify the Release slip")
    act_practical_demo = models.BooleanField(default=False, verbose_name="Practical Demonstration of Testing Parameters")
    act_assign_samples = models.BooleanField(default=False, verbose_name="Assigned the samples for testing to analysts/assistant analyst")
    act_analyze_samples = models.BooleanField(default=False, verbose_name="Analyzed the samples")
    act_housekeeping = models.BooleanField(default=False, verbose_name="House Keeping")
    act_solution_prep = models.BooleanField(default=False, verbose_name="Solution Preparation")
    act_sample_retaining = models.BooleanField(default=False, verbose_name="Sample Retaining")
    act_sample_discard = models.BooleanField(default=False, verbose_name="Sample Discard/Dispose")
    act_stock_management = models.BooleanField(default=False, verbose_name="Stock Management")
    act_id_non_conformity = models.BooleanField(default=False, verbose_name="Identification of Non-Conformity")
    act_id_improvement = models.BooleanField(default=False, verbose_name="Identification of Need for improvement or Deviation")
    act_temp_humidity = models.BooleanField(default=False, verbose_name="Prepare the temperature/humidity charts")
    act_cleaning_inspections = models.BooleanField(default=False, verbose_name="Perform the Cleaning Inspections")
    act_standardization = models.BooleanField(default=False, verbose_name="Standardization")
    act_pt_samples = models.BooleanField(default=False, verbose_name="PT Samples/Blind Samples")
    
    # 1.02 Master List Authorizations
    auth_dev_mod = models.BooleanField(default=False, verbose_name="Development & Modification")
    auth_perform = models.BooleanField(default=False, verbose_name="Perform")
    auth_validation = models.BooleanField(default=False, verbose_name="Validation / Verification")
    auth_supervision = models.BooleanField(default=False, verbose_name="Supervision")
    auth_report_review = models.BooleanField(default=False, verbose_name="Report and Review of Results")
    auth_analysis_results = models.BooleanField(default=False, verbose_name="Analysis of results (Conformity/Opinions)")
    auth_auth_results = models.BooleanField(default=False, verbose_name="Authorization of Results")
    auth_uncertainty = models.BooleanField(default=False, verbose_name="Uncertainty Measurement of Assay")
    
    authorization_date = models.DateField(auto_now_add=True)
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_authorizations', on_delete=models.RESTRICT, null=True, blank=True)
    authorized_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='authorized_authorizations', on_delete=models.RESTRICT, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    authorized_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')


    class Meta:
        verbose_name = 'Personnel Authorization (1.01 & 1.02)'
        verbose_name_plural = 'Personnel Authorizations (1.01 & 1.02)'

    def __str__(self):
        return f"Authorization Permit - {self.user.get_full_name() or self.user.username}"




# QCL-FRM-6.05 Comparative Statement
class ComparativeStatement(models.Model):
    history = HistoricalRecords()
    
    item_name = models.CharField(max_length=200, help_text="Item or Service Name")
    date = models.DateField(auto_now_add=True)
    purchase_demand = models.ForeignKey('PurchaseRequest', on_delete=models.SET_NULL, null=True, blank=True)
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_statements', on_delete=models.RESTRICT, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_statements', on_delete=models.RESTRICT, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    
    def __str__(self):
        return f"CS - {self.item_name} ({self.date})"

    class Meta:
        verbose_name = 'Comparative Statement (QCL-FRM-6.05)'
        verbose_name_plural = 'Comparative Statement (QCL-FRM-6.05)s'

class ComparativeStatementSupplier(models.Model):
    statement = models.ForeignKey(ComparativeStatement, on_delete=models.CASCADE, related_name='suppliers')
    supplier_name = models.CharField(max_length=150)
    rate = models.CharField(max_length=100, verbose_name="Rate (RS)")
    quantity = models.CharField(max_length=100)
    delivery_time = models.CharField(max_length=100)
    quality = models.CharField(max_length=150, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    is_selected = models.BooleanField(default=False, verbose_name="Selected Supplier")

# QCL-FRM-6.06 Supplier Evaluation Plan
class SupplierEvaluationPlan(models.Model):
    history = HistoricalRecords()
    
    year = models.CharField(max_length=4, help_text="e.g. 2024")
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_evaluation_plans', on_delete=models.RESTRICT, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_evaluation_plans', on_delete=models.RESTRICT, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    def __str__(self):
        return f"Supplier Evaluation Plan - {self.year}"

    class Meta:
        verbose_name = 'Supplier Evaluation Plan (QCL-FRM-6.06)'
        verbose_name_plural = 'Supplier Evaluation Plan (QCL-FRM-6.06)s'

class SupplierEvaluationPlanItem(models.Model):
    plan = models.ForeignKey(SupplierEvaluationPlan, on_delete=models.CASCADE, related_name='items')
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    frequency = models.CharField(max_length=50, default="Annually")
    evaluation_date = models.DateField()
    next_evaluation_date = models.DateField()
    responsibility = models.CharField(max_length=100, default="QCM / Lab Incharge")
    records = models.CharField(max_length=100, default="QCL-FRM-6.03")
from django.db import models
from django.conf import settings
from .approval_utils import ISOApprovalModel

# QCL-FRM-1.01 Personnel Authorization Permit
class PersonnelAuthorizationPermit(ISOApprovalModel):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_date = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    
    # Checkboxes
    op_flame_photometer = models.BooleanField("Operation of Flame Photometer", default=False)
    op_uv_vis = models.BooleanField("Operation of UV-Visible Spectrophotometer", default=False)
    op_karl_fischer = models.BooleanField("Operation of Karl Fischer", default=False)
    op_kjeldhal = models.BooleanField("Operation of Kjeldhal's Apparatus", default=False)
    op_furnace = models.BooleanField("Operation of Furnace", default=False)
    op_ph_meter = models.BooleanField("Operation of pH Meter", default=False)
    op_tds_meter = models.BooleanField("Operation of TDS Meter", default=False)
    op_analytical_balance = models.BooleanField("Operation of Analytical Balance", default=False)
    loss_on_ignition = models.BooleanField("Loss on Ignition", default=False)
    monitoring_env_cond = models.BooleanField("Monitoring Environmental Conditions", default=False)
    intermediate_checks = models.BooleanField("Perform the Intermediate Checks", default=False)
    control_chart = models.BooleanField("Prepare Control Chart", default=False)
    sample_receiving = models.BooleanField("Sample Receiving", default=False)
    method_validation = models.BooleanField("Method Validation/Verification", default=False)
    sample_handling = models.BooleanField("Sample Handling", default=False)
    report_preparation = models.BooleanField("Report Preparation", default=False)
    preparing_review_reports = models.BooleanField("Preparing/Review the Analysis Reports", default=False)
    measurements_uncertainty = models.BooleanField("Measurements of Uncertainty", default=False)
    internal_auditing = models.BooleanField("Internal Auditing", default=False)
    training_lms = models.BooleanField("Training of Lab Staff on LMS 17025:2017", default=False)
    prep_review_procedures = models.BooleanField("Preparation and Reviewing of Procedures/Other Documents", default=False)
    prep_review_approved_reports = models.BooleanField("Preparation, Reviewing and Approved of Reports", default=False)
    prep_review_release_slip = models.BooleanField("Preparation and Review/Verify the Release slip", default=False)
    review_analysis_reports = models.BooleanField("Review the Analysis Reports", default=False)
    practical_demo = models.BooleanField("Practical Demonstration of Testing Parameters", default=False)
    assigned_samples = models.BooleanField("Assigned the samples for testing", default=False)
    analyzed_samples = models.BooleanField("Analyzed the samples", default=False)
    release_slip_prep = models.BooleanField("Release Slip Preparation", default=False)
    house_keeping = models.BooleanField("House Keeping", default=False)
    solution_prep = models.BooleanField("Solution Preparation", default=False)
    sample_retaining = models.BooleanField("Sample Retaining", default=False)
    sample_discard = models.BooleanField("Sample Discard/Dispose", default=False)
    stock_management = models.BooleanField("Stock Management", default=False)
    ident_non_conformity = models.BooleanField("Identification of Non-Conformity", default=False)
    ident_improvement = models.BooleanField("Identification of Need for improvement or Deviation", default=False)
    prep_temp_charts = models.BooleanField("Prepare the temperature/humidity charts", default=False)
    cleaning_inspections = models.BooleanField("Perform the Cleaning Inspections", default=False)
    density_test = models.BooleanField("Density Test", default=False)
    ph_test = models.BooleanField("pH Test", default=False)
    conductivity_test = models.BooleanField("Conductivity Test", default=False)
    tds_test = models.BooleanField("TDS Test", default=False)
    loss_on_drying = models.BooleanField("Loss on Drying", default=False)
    weighing = models.BooleanField("Weighing", default=False)
    sieve_test = models.BooleanField("Sieve Test", default=False)
    calcium_test = models.BooleanField("Calcium test", default=False)
    sulfur_test = models.BooleanField("Sulfur/Sulfate Test", default=False)
    nitrogen_test = models.BooleanField("Nitrogen Test", default=False)
    manual_titrations = models.BooleanField("Manual Titrations", default=False)
    humic_acid_test = models.BooleanField("Humic Acid Test", default=False)
    phosphorus_test = models.BooleanField("Phosphorus Testing", default=False)
    total_organic_carbon = models.BooleanField("Total Organic Carbon", default=False)
    cn_ratio = models.BooleanField("C/N Ratio Calculation", default=False)
    organic_matter = models.BooleanField("Organic Matter", default=False)
    cec = models.BooleanField("CEC", default=False)
    sodium_test = models.BooleanField("Sodium Test", default=False)
    zinc_test = models.BooleanField("Zinc Test", default=False)
    boron_analysis = models.BooleanField("Boron Analysis", default=False)
    copper_test = models.BooleanField("Copper Test", default=False)
    moisture_test = models.BooleanField("Moisture Test", default=False)
    standardization = models.BooleanField("Standardization", default=False)
    pt_samples = models.BooleanField("PT Samples/Blind Samples", default=False)
    
    remarks = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Personnel Auth Permit (1.01)"
        verbose_name_plural = "Personnel Auth Permits (1.01)"

# QCL-FRM-1.01A Analyst Authorization For Tests and Instruments
class CompetencyEvalInternalSample(ISOApprovalModel):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evaluation_date = models.DateField(null=True, blank=True)
    
    material_description = models.CharField(max_length=255, null=True, blank=True)
    reference_method = models.CharField(max_length=255, null=True, blank=True)
    batch_lot_no = models.CharField(max_length=100, null=True, blank=True)
    mfg_date = models.DateField(null=True, blank=True)
    working_standard_qty = models.CharField(max_length=100, null=True, blank=True)
    exp_date = models.DateField(null=True, blank=True)
    unknown_sample_qty = models.CharField(max_length=100, null=True, blank=True)
    analysis_date = models.DateField(null=True, blank=True)
    temp_rh = models.CharField(max_length=100, null=True, blank=True)
    result_submission_date = models.DateField(null=True, blank=True)
    source_of_material = models.CharField(max_length=255, null=True, blank=True)
    
    remarks = models.TextField(null=True, blank=True)
    state_deviation = models.TextField(null=True, blank=True)
    interpretation_of_result = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Eval Internal Samples (1.01C)"
        verbose_name_plural = "Eval Internal Samples (1.01C)"

class InternalSampleTestRow(models.Model):
    evaluation = models.ForeignKey(CompetencyEvalInternalSample, on_delete=models.CASCADE, related_name='tests')
    test_description = models.CharField(max_length=255)
    assigned_value = models.CharField(max_length=100, null=True, blank=True)
    report_value = models.CharField(max_length=100, null=True, blank=True)
    z_score = models.CharField(max_length=100, null=True, blank=True)
    nmt_2_0 = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)


# QCL-FRM-1.01D Competency Evaluation PT Samples
class CompetencyEvalPTSample(ISOApprovalModel):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evaluation_date = models.DateField(null=True, blank=True)
    pt_round_name = models.CharField(max_length=100, null=True, blank=True)
    
    material_description = models.CharField(max_length=255, null=True, blank=True)
    reference_method = models.CharField(max_length=255, null=True, blank=True)
    batch_lot_no = models.CharField(max_length=100, null=True, blank=True)
    mfg_date = models.DateField(null=True, blank=True)
    working_standard_qty = models.CharField(max_length=100, null=True, blank=True)
    exp_date = models.DateField(null=True, blank=True)
    unknown_sample_qty = models.CharField(max_length=100, null=True, blank=True)
    analysis_date = models.DateField(null=True, blank=True)
    temp_rh = models.CharField(max_length=100, null=True, blank=True)
    result_submission_date = models.DateField(null=True, blank=True)
    source_of_material = models.CharField(max_length=255, null=True, blank=True)
    
    remarks = models.TextField(null=True, blank=True)
    state_deviation = models.TextField(null=True, blank=True)
    interpretation_of_result = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Eval PT Samples (1.01D)"
        verbose_name_plural = "Eval PT Samples (1.01D)"

class PTSampleTestRow(models.Model):
    evaluation = models.ForeignKey(CompetencyEvalPTSample, on_delete=models.CASCADE, related_name='tests')
    test_description = models.CharField(max_length=255)
    assigned_value = models.CharField(max_length=100, null=True, blank=True)
    report_value = models.CharField(max_length=100, null=True, blank=True)
    z_score = models.CharField(max_length=100, null=True, blank=True)
    nmt_2_0 = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)


GRADING_CHOICES = [
    ('E', 'Exceptional'),
    ('HC', 'Highly Competent'),
    ('C', 'Competent'),
    ('AC', 'Approaching Competence'),
    ('ND', 'Needs Development'),
]

# QCL-FRM-1.01E Grading Matrix Equipment
class GradingMatrixEquipment(ISOApprovalModel):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    remarks = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Grading Matrix Equipment (1.01E)"
        verbose_name_plural = "Grading Matrix Equipment (1.01E)"

class GradingMatrixEquipmentRow(models.Model):
    matrix = models.ForeignKey(GradingMatrixEquipment, on_delete=models.CASCADE, related_name='rows')
    equipment_instrument = models.CharField(max_length=255)
    level_1 = models.CharField(max_length=50, null=True, blank=True)
    level_2 = models.CharField(max_length=50, null=True, blank=True)


# QCL-FRM-1.01F Grading Matrix Product
class GradingMatrixProduct(ISOApprovalModel):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    dosage_form = models.CharField(max_length=100, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    batch_no = models.CharField(max_length=100, null=True, blank=True)
    mfg_date = models.DateField(null=True, blank=True)
    exp_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Grading Matrix Product (1.01F)"
        verbose_name_plural = "Grading Matrix Product (1.01F)"

class GradingMatrixProductRow(models.Model):
    matrix = models.ForeignKey(GradingMatrixProduct, on_delete=models.CASCADE, related_name='rows')
    tests = models.CharField(max_length=255)
    methodology = models.CharField(max_length=255, null=True, blank=True)
    level_1 = models.CharField(max_length=50, null=True, blank=True)
    level_2 = models.CharField(max_length=50, null=True, blank=True)


# QCL-FRM-1.01G Grading Matrix Document
class GradingMatrixDocument(ISOApprovalModel):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    remarks = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Grading Matrix Document (1.01G)"
        verbose_name_plural = "Grading Matrix Document (1.01G)"

class GradingMatrixDocumentRow(models.Model):
    matrix = models.ForeignKey(GradingMatrixDocument, on_delete=models.CASCADE, related_name='rows')
    document_title = models.CharField(max_length=255)
    level_1 = models.CharField(max_length=50, null=True, blank=True)
    level_2 = models.CharField(max_length=50, null=True, blank=True)


# QCL-FRM-1.02 List of Authorized Analyst / Staff
class AuthorizedAnalystList(ISOApprovalModel):
    revision_number = models.CharField(max_length=20)
    date_issued = models.DateField()
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    file_attachment = models.FileField(upload_to='iso_personnel/', blank=True, null=True)
    
    class Meta:
        verbose_name = "List of Authorized Analysts (1.02)"
        verbose_name_plural = "List of Authorized Analysts (1.02)"

# QCL-FRM-1.03 List of Technical Personnel
class TechnicalPersonnelList(ISOApprovalModel):
    revision_number = models.CharField(max_length=20)
    date_issued = models.DateField()
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    file_attachment = models.FileField(upload_to='iso_personnel/', blank=True, null=True)
    
    class Meta:
        verbose_name = "List of Technical Personnel (1.03)"
        verbose_name_plural = "List of Technical Personnel (1.03)"

from django.db import models
from django.conf import settings
from .approval_utils import ISOApprovalModel

# QCL-FRM-2.02 Training Need Assessment Form
class TrainingNeedAssessment(ISOApprovalModel):
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
class AnnualTrainingPlan(ISOApprovalModel):
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
class TrainingAttendanceSheet(ISOApprovalModel):
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
class TrainingEvaluation(ISOApprovalModel):
    training = models.ForeignKey(TrainingAttendanceSheet, on_delete=models.CASCADE)
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    evaluation_date = models.DateField(null=True, blank=True)
    training_description = models.CharField(max_length=255, null=True, blank=True)
    trainer_institute = models.CharField(max_length=255, null=True, blank=True)
    
    mode_oral = models.BooleanField(default=False)
    mode_written = models.BooleanField(default=False)
    mode_practical = models.BooleanField(default=False)
    
    weightage_oral = models.IntegerField(null=True, blank=True)
    total_marks_oral = models.IntegerField(null=True, blank=True)
    obtained_marks_oral = models.IntegerField(null=True, blank=True)
    percentage_oral = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    weightage_written = models.IntegerField(null=True, blank=True)
    total_marks_written = models.IntegerField(null=True, blank=True)
    obtained_marks_written = models.IntegerField(null=True, blank=True)
    percentage_written = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    weightage_practical = models.IntegerField(null=True, blank=True)
    total_marks_practical = models.IntegerField(null=True, blank=True)
    obtained_marks_practical = models.IntegerField(null=True, blank=True)
    percentage_practical = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    total_obtained_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    final_remarks = models.CharField(max_length=50, choices=[
        ('OUTSTANDING', 'Out Standing'),
        ('SATISFACTORY', 'Satisfactory'),
        ('CONDITIONAL', 'Conditional'),
        ('UNSATISFACTORY', 'Unsatisfactory')
    ], null=True, blank=True)
    
    class Meta:
        verbose_name = "Training Evaluation (2.05)"
        verbose_name_plural = "Training Evaluations (2.05)"


# QCL-FRM-2.07 Training Feedback Form
class TrainingFeedback(ISOApprovalModel):
    training = models.ForeignKey(TrainingAttendanceSheet, on_delete=models.CASCADE)
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    location = models.CharField(max_length=255, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    topic = models.CharField(max_length=255, null=True, blank=True)
    trainer_institute = models.CharField(max_length=255, null=True, blank=True)
    
    # Course
    expectations_met = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    speed_rate = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    practical_application = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    job_effect = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    focus_structure = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    
    # Process
    adequate_for_position = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    methods_effective = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    materials_clear = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    enough_resources = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    timely_manner = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    
    # Structure
    information_usefulness = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    structure_usefulness = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    pace_usefulness = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    schedule_convenience = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    materials_usefulness = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    appropriate_for_experience = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    
    # About Trainer/Mentor
    trainer_knowledgeable = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    concepts_clear = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    handling_questions = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    overall_facilitation = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    
    # Overall
    overall_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    
    class Meta:
        verbose_name = "Training Feedback (2.07)"
        verbose_name_plural = "Training Feedbacks (2.07)"


# QCL-FRM-2.08 Individual Training Record
class IndividualTrainingRecord(ISOApprovalModel):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    training_title = models.CharField(max_length=255)
    date_completed = models.DateField()
    internal_external = models.CharField(max_length=50, choices=[('INTERNAL', 'Internal'), ('EXTERNAL', 'External')], null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Individual Training Record (2.08)"
        verbose_name_plural = "Individual Training Records (2.08)"


# QCL-FRM-2.09 Orientation Plan
class OrientationPlan(ISOApprovalModel):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Orientation Plan (2.09)"
        verbose_name_plural = "Orientation Plans (2.09)"

class OrientationPlanTopic(models.Model):
    plan = models.ForeignKey(OrientationPlan, on_delete=models.CASCADE, related_name='topics')
    detail = models.CharField(max_length=255)
    responsibility = models.CharField(max_length=100)
    checked = models.BooleanField(default=False)


# QCL-FRM-2.10 Competence Reassessment form
class CompetenceReassessment(ISOApprovalModel):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    reason_for_reassessment = models.TextField()
    outcome = models.CharField(max_length=255)
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = "Competence Reassessment (2.10)"
        verbose_name_plural = "Competence Reassessments (2.10)"

# QCL-FRM-2.12 Trainer Evaluation Form
class TrainerEvaluation(ISOApprovalModel):
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluated_as_trainer')
    topic = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField()
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    
    # 17 Criteria
    objectives_clear = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    knowledge_iso17025 = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    clarity_concepts = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    delivery_skills = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    address_questions = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    engagement = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    materials_tools = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    relevance_content = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    topics_relevant = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    organized = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    materials_helpful = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    useful_in_work = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    well_prepared = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    knowledgeable_topics = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    objectives_met = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    time_sufficient = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    overall_effectiveness = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    
    # Feedback
    strengths_content_delivery = models.TextField(null=True, blank=True)
    engagement_interaction = models.TextField(null=True, blank=True)
    practical_applications = models.TextField(null=True, blank=True)
    
    key_strengths = models.TextField(null=True, blank=True)
    areas_for_improvement = models.TextField(null=True, blank=True)
    suggestions_for_development = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Trainer Evaluation (2.12)"
        verbose_name_plural = "Trainer Evaluations (2.12)"



class CompetencyMonitoring(ISOApprovalModel):
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    main_functions = models.CharField(max_length=255, null=True, blank=True)
    
    # Rows for the table (Score 1-4)
    score_education = models.IntegerField(null=True, blank=True)
    remarks_education = models.TextField(null=True, blank=True)
    
    score_qualification = models.IntegerField(null=True, blank=True)
    remarks_qualification = models.TextField(null=True, blank=True)
    
    score_experience = models.IntegerField(null=True, blank=True)
    remarks_experience = models.TextField(null=True, blank=True)
    
    score_training = models.IntegerField(null=True, blank=True)
    remarks_training = models.TextField(null=True, blank=True)
    
    score_technical_knowledge = models.IntegerField(null=True, blank=True)
    remarks_technical_knowledge = models.TextField(null=True, blank=True)
    
    score_skills = models.IntegerField(null=True, blank=True)
    remarks_skills = models.TextField(null=True, blank=True)
    
    score_testing_activities = models.IntegerField(null=True, blank=True)
    remarks_testing_activities = models.TextField(null=True, blank=True)
    
    score_continuous_education = models.IntegerField(null=True, blank=True)
    remarks_continuous_education = models.TextField(null=True, blank=True)
    
    overall_score = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Competency Monitoring (1.04)"
        verbose_name_plural = "Competency Monitoring (1.04)"

# QCL-FRM-2.06 Authorized Personnel List
class AuthorizedPersonnelList_2_06(ISOApprovalModel):
    date_issued = models.DateField()
    revision_number = models.CharField(max_length=50)
    file_attachment = models.FileField(upload_to='master_lists/2_06/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Authorized Personnel List (2.06)"
        verbose_name_plural = "Authorized Personnel Lists (2.06)"

# QCL-FRM-2.11 Orientation Training Plan for Newly Inducted Staff
class NewInductionOrientation_2_11(ISOApprovalModel):
    candidate_name = models.CharField(max_length=255)
    joining_date = models.DateField(null=True, blank=True)
    orientation_started_from = models.DateField(null=True, blank=True)
    probation_period = models.CharField(max_length=100, null=True, blank=True)
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    approval_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "New Induction Orientation (2.11)"
        verbose_name_plural = "New Induction Orientations (2.11)"

class InductionOrientationItem(models.Model):
    orientation = models.ForeignKey(NewInductionOrientation_2_11, on_delete=models.CASCADE, related_name='items')
    responsibility = models.CharField(max_length=255)
    trainer = models.CharField(max_length=255)
    training_duration = models.CharField(max_length=100)
from django.db import models
from django.conf import settings
# Use existing ISOApprovalModel from the same file

# ==========================================
# LSP-03 Environmental Conditions
# ==========================================

class EnvironmentalMonitoring_3_01(ISOApprovalModel):
    month = models.CharField(max_length=50)
    year = models.IntegerField()
    location = models.CharField(max_length=255, verbose_name="Location / Warehouse")
    temperature_range = models.CharField(max_length=100, default="25 ±10 °C")
    humidity_range = models.CharField(max_length=100, default="50% RH ±20 RH")

    class Meta:
        verbose_name = "Environmental Monitoring (3.01)"
        verbose_name_plural = "Environmental Monitoring (3.01)"

class EnvironmentalMonitoringItem(models.Model):
    monitoring = models.ForeignKey(EnvironmentalMonitoring_3_01, on_delete=models.CASCADE, related_name="items")
    date = models.DateField()
    parameter = models.CharField(max_length=100, default="Temperature / Humidity")
    day_shift_11am = models.CharField(max_length=50, blank=True, null=True)
    day_shift_3pm = models.CharField(max_length=50, blank=True, null=True)
    day_recorded_by = models.CharField(max_length=100, blank=True, null=True)
    night_shift_11pm = models.CharField(max_length=50, blank=True, null=True)
    daily_average = models.CharField(max_length=50, blank=True, null=True)
    night_recorded_by = models.CharField(max_length=100, blank=True, null=True)
    checked_by = models.CharField(max_length=100, blank=True, null=True)

class HumidityControlChart_3_02(ISOApprovalModel):
    month = models.CharField(max_length=50)
    year = models.IntegerField()
    location = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Humidity Control Chart (3.02)"
        verbose_name_plural = "Humidity Control Charts (3.02)"

class HumidityControlItem(models.Model):
    chart = models.ForeignKey(HumidityControlChart_3_02, on_delete=models.CASCADE, related_name="items")
    date = models.DateField()
    reading = models.FloatField(null=True, blank=True)
    variance = models.FloatField(null=True, blank=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)

class TemperatureControlChart_3_03(ISOApprovalModel):
    month = models.CharField(max_length=50)
    year = models.IntegerField()
    location = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Temperature Control Chart (3.03)"
        verbose_name_plural = "Temperature Control Charts (3.03)"

class TemperatureControlItem(models.Model):
    chart = models.ForeignKey(TemperatureControlChart_3_03, on_delete=models.CASCADE, related_name="items")
    date = models.DateField()
    reading = models.FloatField(null=True, blank=True)
    variance = models.FloatField(null=True, blank=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)

# ==========================================
# LSP-04 Equipment Control
# ==========================================

class CorrectiveActionRequest_4_01(ISOApprovalModel):
    month = models.CharField(max_length=50)
    department = models.CharField(max_length=150, default="QC Lab")
    car_no = models.CharField(max_length=100)
    initiated_on = models.DateField()
    initiated_by = models.CharField(max_length=150)
    
    DUE_TO_CHOICES = [
        ('NC', 'NC'),
        ('Complaint', 'Complaint'),
        ('Accident/Incident', 'Accident/Incident'),
        ('Audit NC', 'Audit NC'),
        ('Suggestion/Improvement', 'Suggestion/Improvement'),
        ('Technical Fault', 'Technical Fault'),
        ('Others', 'Others'),
    ]
    initiated_due_to = models.CharField(max_length=50, choices=DUE_TO_CHOICES)
    description = models.TextField()
    
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    marked_to = models.CharField(max_length=150, blank=True, null=True)
    date_marked = models.DateField(blank=True, null=True)
    
    root_cause_analysis = models.TextField(blank=True, null=True)
    proposed_action = models.TextField(blank=True, null=True)
    target_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Corrective Action Request (4.01)"
        verbose_name_plural = "Corrective Action Requests (4.01)"

class MasterListEquipment_4_02(ISOApprovalModel):
    lab_name = models.CharField(max_length=255, default="Quality Control Laboratory")
    
    class Meta:
        verbose_name = "Master List of Equipments (4.02)"
        verbose_name_plural = "Master List of Equipments (4.02)"

class MasterListEquipmentItem(models.Model):
    master_list = models.ForeignKey(MasterListEquipment_4_02, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    identification_no = models.CharField(max_length=100)
    operating_range = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    calibration_certificate_no = models.CharField(max_length=150, blank=True, null=True)
    calibration_certificate_date = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)

class EquipmentMaintenanceRecord_4_03(ISOApprovalModel):
    for_the_year = models.CharField(max_length=50, help_text="e.g., 2024-2025")
    
    class Meta:
        verbose_name = "Equipment Maintenance Record (4.03)"
        verbose_name_plural = "Equipment Maintenance Records (4.03)"

class MaintenanceRecordItem(models.Model):
    record = models.ForeignKey(EquipmentMaintenanceRecord_4_03, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    identification_no = models.CharField(max_length=100)
    make_model_serial = models.CharField(max_length=255)
    location_and_manual = models.CharField(max_length=255)
    frequency = models.CharField(max_length=100)
    maintenance_date = models.DateField()
    parts_repaired_replaced = models.CharField(max_length=255, blank=True, null=True)
    maintenance_by = models.CharField(max_length=150)

class CalibrationProgram_4_04(ISOApprovalModel):
    year = models.CharField(max_length=50, help_text="e.g., 2024")
    
    class Meta:
        verbose_name = "Calibration Program (4.04)"
        verbose_name_plural = "Calibration Programs (4.04)"

class CalibrationProgramItem(models.Model):
    program = models.ForeignKey(CalibrationProgram_4_04, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    identification_no = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    frequency = models.CharField(max_length=100)
    schedule_month = models.CharField(max_length=100)
    remarks = models.CharField(max_length=255, blank=True, null=True)
from django.db import models
from django.conf import settings

# ==========================================
# LSP-05 Metrological Traceability
# ==========================================

class CRMList_5_01(ISOApprovalModel):
    month = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "CRM List (5.01)"
        verbose_name_plural = "CRM Lists (5.01)"

class CRMListItem(models.Model):
    crm_list = models.ForeignKey(CRMList_5_01, on_delete=models.CASCADE, related_name="items")
    analyte = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    cat_no = models.CharField(max_length=150, blank=True, null=True)
    lot_no = models.CharField(max_length=150, blank=True, null=True)
    traceability = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.CharField(max_length=100)
    acquisition_date = models.DateField(blank=True, null=True)
    use_by_date = models.DateField(blank=True, null=True)

# ==========================================
# LSP-06 Procedure for Provided Services
# ==========================================

class SupplierSelection_6_01(ISOApprovalModel):
    selection_date = models.DateField(blank=True, null=True)
    form_no = models.CharField(max_length=100, blank=True, null=True)
    name_of_supplier = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=150, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    requirements_from_supplier = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Supplier Selection Form (6.01)"
        verbose_name_plural = "Supplier Selection Forms (6.01)"

class SupplierSelectionCriteria(models.Model):
    selection = models.ForeignKey(SupplierSelection_6_01, on_delete=models.CASCADE, related_name="items")
    criteria = models.CharField(max_length=255)
    status_against_criteria = models.CharField(max_length=255)

class ApprovedSupplierServiceProvider_6_02(ISOApprovalModel):
    period = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Approved Supplier Service Provider (6.02)"
        verbose_name_plural = "Approved Supplier Service Providers (6.02)"

class ApprovedSupplierItem(models.Model):
    provider_list = models.ForeignKey(ApprovedSupplierServiceProvider_6_02, on_delete=models.CASCADE, related_name="items")
    name_of_supplier = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=255)
    product_service = models.CharField(max_length=255)

class ExternalProviderEvaluation_6_03(ISOApprovalModel):
    supplier_name = models.CharField(max_length=255)
    evaluation_date = models.DateField()
    overall_rating = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "External Provider Evaluation (6.03)"
        verbose_name_plural = "External Provider Evaluations (6.03)"

class ExternalProviderEvaluationCriteria(models.Model):
    evaluation = models.ForeignKey(ExternalProviderEvaluation_6_03, on_delete=models.CASCADE, related_name="items")
    criteria = models.CharField(max_length=255)
    score_or_status = models.CharField(max_length=100)

class SupplierPerformanceMonitoring_6_04(ISOApprovalModel):
    period = models.CharField(max_length=100)
    assessed_by = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Supplier Performance Monitoring (6.04)"
        verbose_name_plural = "Supplier Performance Monitoring (6.04)"

class SupplierPerformanceItem(models.Model):
    monitoring = models.ForeignKey(SupplierPerformanceMonitoring_6_04, on_delete=models.CASCADE, related_name="items")
    supplier_name = models.CharField(max_length=255)
    quality_rating = models.CharField(max_length=50, blank=True, null=True)
    assessment_rating = models.CharField(max_length=50, blank=True, null=True)
    price_rate = models.CharField(max_length=50, blank=True, null=True)
    market_reputation = models.CharField(max_length=50, blank=True, null=True)
    overall_rating = models.CharField(max_length=50, blank=True, null=True)
    certification_rating = models.CharField(max_length=50, blank=True, null=True)

class ComparativeStatement_6_05(ISOApprovalModel):
    item_name = models.CharField(max_length=255)
    statement_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Comparative Statement (6.05)"
        verbose_name_plural = "Comparative Statements (6.05)"

class ComparativeStatementItem_6_05(models.Model):
    statement = models.ForeignKey(ComparativeStatement_6_05, on_delete=models.CASCADE, related_name="items")
    supplier_name = models.CharField(max_length=255)
    rate_rs = models.CharField(max_length=100, blank=True, null=True)
    items = models.CharField(max_length=100, blank=True, null=True)
    quality = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    time_delivery = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)

class SupplierEvaluationPlan_6_06(ISOApprovalModel):
    for_the_year = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Supplier Evaluation Plan (6.06)"
        verbose_name_plural = "Supplier Evaluation Plans (6.06)"

class SupplierEvaluationPlanItem_6_06(models.Model):
    plan = models.ForeignKey(SupplierEvaluationPlan_6_06, on_delete=models.CASCADE, related_name="items")
    name_of_supplier = models.CharField(max_length=255)
    frequency = models.CharField(max_length=100)
    evaluation_date = models.DateField(blank=True, null=True)
    next_eval_1 = models.DateField(blank=True, null=True)
    next_eval_2 = models.DateField(blank=True, null=True)
    next_eval_3 = models.DateField(blank=True, null=True)
    next_eval_4 = models.DateField(blank=True, null=True)
    responsibility = models.CharField(max_length=150, blank=True, null=True)
    records = models.CharField(max_length=150, blank=True, null=True)

class StorePurchaseDemand_6_07(ISOApprovalModel):
    demand_date = models.DateField(blank=True, null=True)
    intender = models.CharField(max_length=150, blank=True, null=True)
    store_keeper = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Store Purchase Demand (6.07)"
        verbose_name_plural = "Store Purchase Demands (6.07)"

class StorePurchaseDemandItem(models.Model):
    demand = models.ForeignKey(StorePurchaseDemand_6_07, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=255)
    model = models.CharField(max_length=150, blank=True, null=True)
    brand = models.CharField(max_length=150, blank=True, null=True)
    quality = models.CharField(max_length=100, blank=True, null=True)
    material_unit = models.CharField(max_length=50, blank=True, null=True)
    quantity_required = models.CharField(max_length=50, blank=True, null=True)
    stock_in_hand = models.CharField(max_length=50, blank=True, null=True)
    net_purchase_required = models.CharField(max_length=50, blank=True, null=True)
    concentration = models.CharField(max_length=100, blank=True, null=True)
    purpose_of_purchase = models.CharField(max_length=255, blank=True, null=True)

class ProductsServicesInspection_6_08(ISOApprovalModel):
    TYPE_CHOICES = [('Products', 'Products'), ('Services', 'Services')]
    STATUS_CHOICES = [('Newly engaged', 'Newly engaged'), ('Pre-existing', 'Pre-existing')]

    type_of_purchase = models.CharField(max_length=50, choices=TYPE_CHOICES)
    products_services = models.CharField(max_length=255)
    external_provider = models.CharField(max_length=255)
    provider_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    gate_pass_no = models.CharField(max_length=100, blank=True, null=True)
    pr_po_no = models.CharField(max_length=100, blank=True, null=True)
    invoice_no = models.CharField(max_length=100, blank=True, null=True)
    date_of_receipt = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Products Services Inspection (6.08)"
        verbose_name_plural = "Products Services Inspections (6.08)"

class ProductsServicesInspectionItem(models.Model):
    inspection = models.ForeignKey(ProductsServicesInspection_6_08, on_delete=models.CASCADE, related_name="items")
    requirements = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255, blank=True, null=True)

from django.db import models
from django.conf import settings

# ==========================================
# LSP-07 Control of Documents
# ==========================================

class MasterListDocument_7_01(ISOApprovalModel):
    # This acts as the container for the master list
    description = models.CharField(max_length=255, default="Master List of Documents")

    class Meta:
        verbose_name = "Master List of Document (7.01)"
        verbose_name_plural = "Master List of Documents (7.01)"

class MasterListDocumentItem(models.Model):
    master_list = models.ForeignKey(MasterListDocument_7_01, on_delete=models.CASCADE, related_name="items")
    doc_code = models.CharField(max_length=150)
    document_title = models.CharField(max_length=255)
    file_code = models.CharField(max_length=150, blank=True, null=True)
    file_location = models.CharField(max_length=255, blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    rev_no = models.CharField(max_length=50, blank=True, null=True)
    keeper_1 = models.CharField(max_length=150, blank=True, null=True)
    keeper_2 = models.CharField(max_length=150, blank=True, null=True)
    keeper_3 = models.CharField(max_length=150, blank=True, null=True)


class DocumentChangeRequest_7_02(ISOApprovalModel):
    # Section A
    dcr_no = models.CharField(max_length=100)
    dcr_date = models.DateField()
    request_raised_by = models.CharField(max_length=150)
    section = models.CharField(max_length=150)
    document_title = models.CharField(max_length=255)
    
    DOC_STATUS_CHOICES = [('NEW', 'NEW'), ('EXISTING', 'EXISTING')]
    document_status = models.CharField(max_length=50, choices=DOC_STATUS_CHOICES)
    
    REASON_CHOICES = [
        ('New Process Documentation', 'New Process Documentation'),
        ('New Form Documentation', 'New Form Documentation'),
        ('Addition in Document', 'Addition in Document'),
        ('Correction in Document', 'Correction in Document'),
        ('Deletion within Document', 'Deletion within Document'),
        ('Modification in Document', 'Modification in Document')
    ]
    reason = models.CharField(max_length=150, choices=REASON_CHOICES)

    # Section B
    description_of_requirement = models.TextField(blank=True, null=True)
    effected_sections = models.TextField(blank=True, null=True, help_text="Not Applicable on New Documents")

    # Section C
    review_by = models.CharField(max_length=150, blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)
    
    REVIEW_STATUS_CHOICES = [
        ('Draft Reviewed', 'Draft Reviewed'),
        ('Draft Rejected', 'Draft Rejected'),
        ('Draft Revision Suggested', 'Draft Revision Suggested')
    ]
    review_status = models.CharField(max_length=100, choices=REVIEW_STATUS_CHOICES, blank=True, null=True)
    
    REJECTION_REASON_CHOICES = [
        ('Conflict with Policy', 'Conflict with Policy'),
        ('Conflict with Procedure', 'Conflict with Procedure'),
        ('Conflict with Client Requirement', 'Conflict with Client Requirement'),
        ('Conflict with Regulation', 'Conflict with Regulation'),
        ('Incorrect Draft', 'Incorrect Draft'),
        ('Draft Does not reflect "Description of Requirement"', 'Draft Does not reflect "Description of Requirement"')
    ]
    reason_for_rejection = models.CharField(max_length=150, choices=REJECTION_REASON_CHOICES, blank=True, null=True)
    
    final_remarks = models.TextField(blank=True, null=True)
    submitted_for_final_approval_on = models.DateField(blank=True, null=True)
    
    # We already have approved_by from ISOApprovalModel, but adding text fields as requested by form
    approved_by_name = models.CharField(max_length=150, blank=True, null=True)
    approved_designation = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Document Change Request (7.02)"
        verbose_name_plural = "Document Change Requests (7.02)"
from django.db import models
from django.conf import settings

# ==========================================
# LSP-08 Risk and Opportunities
# ==========================================

class RiskManagementSheet_8_01(ISOApprovalModel):
    last_updated_on = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Risk Management Sheet (8.01)"
        verbose_name_plural = "Risk Management Sheets (8.01)"

class RiskManagementItem(models.Model):
    sheet = models.ForeignKey(RiskManagementSheet_8_01, on_delete=models.CASCADE, related_name="items")
    risk = models.CharField(max_length=255)
    o = models.IntegerField(verbose_name="Occurrence (O)")
    s = models.IntegerField(verbose_name="Severity (S)")
    risk_rating = models.IntegerField()
    risk_treatment = models.CharField(max_length=255)
    responsibility = models.CharField(max_length=150)
    target_date = models.DateField(blank=True, null=True)
    actual_date_of_completion = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    risk_revision_sn = models.CharField(max_length=50, blank=True, null=True)


class OpportunityAssessment_8_02(ISOApprovalModel):
    review_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Opportunity Assessment (8.02)"
        verbose_name_plural = "Opportunity Assessments (8.02)"

class OpportunityAssessmentItem(models.Model):
    assessment = models.ForeignKey(OpportunityAssessment_8_02, on_delete=models.CASCADE, related_name="items")
    area_activity = models.CharField(max_length=255)
    concern = models.CharField(max_length=255)
    opportunities = models.TextField()
    risks = models.TextField()
    risk_action = models.TextField()


# ==========================================
# LSP-09 Corrective Actions and Improvements
# ==========================================

class CorrectiveActionRequest_9_01(ISOApprovalModel):
    initiated_by = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    car_no = models.CharField(max_length=100)
    designation = models.CharField(max_length=150, blank=True, null=True)
    car_initiated_date = models.DateField()
    nc_no = models.CharField(max_length=100)
    
    INITIATED_DUE_TO_CHOICES = [
        ('PNAC Assessment', 'PNAC Assessment'),
        ('Complaint', 'Complaint'),
        ('Accident/Incident', 'Accident/Incident'),
        ('Internal Audit', 'Internal Audit'),
        ('Suggestion/Improvement', 'Suggestion/Improvement'),
        ('Technical Fault', 'Technical Fault'),
        ('Others', 'Others')
    ]
    initiated_due_to = models.CharField(max_length=150, choices=INITIATED_DUE_TO_CHOICES)
    description = models.TextField()
    
    PRIORITY_CHOICES = [('Urgent', 'Urgent'), ('Normal', 'Normal'), ('Non-significance', 'Non-significance')]
    significance_priority_level = models.CharField(max_length=50, choices=PRIORITY_CHOICES, blank=True, null=True)
    
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    
    assigned_to = models.CharField(max_length=150, blank=True, null=True)
    assigned_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Corrective Action Request (9.01)"
        verbose_name_plural = "Corrective Action Requests (9.01)"


class CorrectiveActionsRequestLog_9_02(ISOApprovalModel):
    sheet_no = models.CharField(max_length=50)
    year = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Corrective Actions Request Log (9.02)"
        verbose_name_plural = "Corrective Actions Request Logs (9.02)"

class CorrectiveActionsLogItem(models.Model):
    log = models.ForeignKey(CorrectiveActionsRequestLog_9_02, on_delete=models.CASCADE, related_name="items")
    car_no = models.CharField(max_length=100)
    types_of_request = models.CharField(max_length=255)
    initiator_name = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    target_date = models.DateField(blank=True, null=True)
    closing_date = models.DateField(blank=True, null=True)


class RootCauseAnalysisForm_9_04(ISOApprovalModel):
    non_conformance_description = models.TextField()
    rca_team_members = models.CharField(max_length=255)
    rca_team_lead = models.CharField(max_length=150)
    rca_start_date = models.DateField()
    submission_date = models.DateField()
    
    cause_and_effect_diagram = models.BooleanField(default=False)
    five_why_analysis = models.BooleanField(default=False)
    w_2h_5w2h = models.BooleanField(default=False, verbose_name="3W2H / 5W2H")

    class Meta:
        verbose_name = "Root Cause Analysis Form (9.04)"
        verbose_name_plural = "Root Cause Analysis Forms (9.04)"

from django.db import models
from django.conf import settings

# ==========================================
# LSP-10 Internal Audit
# ==========================================

class AuditNotification_10_01(ISOApprovalModel):
    date = models.DateField()
    to_person = models.CharField(max_length=150)
    from_person = models.CharField(max_length=150)
    cc_aqcm = models.CharField(max_length=150, blank=True, null=True)
    
    audit_type_scheduled = models.BooleanField(default=False)
    audit_type_rescheduled = models.BooleanField(default=False)
    audit_type_follow_up = models.BooleanField(default=False)
    
    scope_management_system = models.BooleanField(default=False)
    scope_customer_complaints = models.BooleanField(default=False)
    scope_implementation = models.BooleanField(default=False)
    
    audit_schedule_held_on = models.CharField(max_length=255, blank=True, null=True)
    audit_duration = models.CharField(max_length=100, blank=True, null=True)
    audit_date = models.DateField(blank=True, null=True)
    audit_time = models.CharField(max_length=100, blank=True, null=True)
    lead_auditor = models.CharField(max_length=150, blank=True, null=True)
    members = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Audit Notification (10.01)"
        verbose_name_plural = "Audit Notifications (10.01)"


class AuditSchedule_10_02(ISOApprovalModel):
    for_the_year = models.CharField(max_length=50)
    audit_type = models.CharField(max_length=100, choices=[('Scheduled', 'Scheduled'), ('Un-Scheduled', 'Un-Scheduled')])

    class Meta:
        verbose_name = "Audit Schedule (10.02)"
        verbose_name_plural = "Audit Schedules (10.02)"

class AuditScheduleItem(models.Model):
    schedule = models.ForeignKey(AuditSchedule_10_02, on_delete=models.CASCADE, related_name="items")
    audit_no = models.CharField(max_length=50)
    schedule_date = models.DateField(blank=True, null=True)
    actual_date = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)

class AuditScheduleDeptItem(models.Model):
    schedule = models.ForeignKey(AuditSchedule_10_02, on_delete=models.CASCADE, related_name="dept_items")
    dept_section = models.CharField(max_length=150)
    date_time_from = models.CharField(max_length=100)
    date_time_to = models.CharField(max_length=100)
    auditors = models.CharField(max_length=255)
    auditee = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255, blank=True, null=True)


class MRMSchedule_10_03(ISOApprovalModel):
    for_the_year = models.CharField(max_length=50)

    class Meta:
        verbose_name = "MRM Schedule (10.03)"
        verbose_name_plural = "MRM Schedules (10.03)"

class MRMScheduleItem(models.Model):
    schedule = models.ForeignKey(MRMSchedule_10_03, on_delete=models.CASCADE, related_name="items")
    meeting_no = models.CharField(max_length=50)
    plan_date = models.DateField(blank=True, null=True)
    actual_date = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)


class TrainedAuditorsList_10_04(ISOApprovalModel):
    date = models.DateField()

    class Meta:
        verbose_name = "Trained Auditors List (10.04)"
        verbose_name_plural = "Trained Auditors Lists (10.04)"

class TrainedAuditorItem(models.Model):
    auditors_list = models.ForeignKey(TrainedAuditorsList_10_04, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    remarks = models.CharField(max_length=255, blank=True, null=True)


class AuditorCompetence_10_05(ISOApprovalModel):
    auditor_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    division_name = models.CharField(max_length=150)
    working_experience = models.CharField(max_length=255)
    trainings = models.TextField()
    education = models.CharField(max_length=255)
    job_knowledge = models.TextField()
    impartiality_and_confidentiality = models.TextField()
    skills_scope = models.TextField()
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Auditor Competence (10.05)"
        verbose_name_plural = "Auditor Competences (10.05)"


class ConfidentialAgreementAuditors_10_06(ISOApprovalModel):
    mr_name = models.CharField(max_length=150)
    working_as = models.CharField(max_length=150)
    date_of_agreement = models.DateField()
    laboratory_name = models.CharField(max_length=255, default="Vital Agri Nutrients Quality Control Lab")

    class Meta:
        verbose_name = "Confidential Agreement Auditors (10.06)"
        verbose_name_plural = "Confidential Agreement Auditors (10.06)"


class ImpartialityForm_10_07(ISOApprovalModel):
    mr_name = models.CharField(max_length=150)
    working_as = models.CharField(max_length=150)
    date_of_agreement = models.DateField()
    laboratory_name = models.CharField(max_length=255, default="Vital Agri Nutrients Quality Control Lab")

    class Meta:
        verbose_name = "Impartiality form (10.07)"
        verbose_name_plural = "Impartiality forms (10.07)"


class InternalAuditForm_10_08(ISOApprovalModel):
    audit_location = models.CharField(max_length=255)
    department = models.CharField(max_length=150)
    team_leader = models.CharField(max_length=150)
    team_member = models.CharField(max_length=150)
    date_of_audit = models.DateField()
    general_observations = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    results_findings = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Internal Audit Form (10.08)"
        verbose_name_plural = "Internal Audit Forms (10.08)"


class InternalAuditCheckList_10_09(ISOApprovalModel):
    auditor_name = models.CharField(max_length=150)
    clauses_covered = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    standard_guide = models.CharField(max_length=255)
    manager_represented = models.CharField(max_length=150)
    date_of_audit = models.DateField()
    report_to_be = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Internal Audit Check List (10.09)"
        verbose_name_plural = "Internal Audit Check Lists (10.09)"

class InternalAuditCheckListItem(models.Model):
    checklist = models.ForeignKey(InternalAuditCheckList_10_09, on_delete=models.CASCADE, related_name="items")
    question = models.TextField()
    status = models.CharField(max_length=50) # Yes/No/NA
    remarks = models.TextField(blank=True, null=True)


class AuditReport_10_10(ISOApprovalModel):
    date = models.DateField()
    audit_number = models.CharField(max_length=100)
    audit_type = models.CharField(max_length=100, choices=[('Scheduled', 'Scheduled'), ('Unscheduled', 'Unscheduled')])
    department_section = models.CharField(max_length=150, default="QCL")
    
    observation_count = models.IntegerField(default=0)
    minor_count = models.IntegerField(default=0)
    major_count = models.IntegerField(default=0)
    
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Audit Report (10.10)"
        verbose_name_plural = "Audit Reports (10.10)"


# ==========================================
# LSP-11 Managerial Meetings
# ==========================================

class MRMSchedule_11_01(ISOApprovalModel):
    for_the_year = models.CharField(max_length=50)

    class Meta:
        verbose_name = "MRM Schedule (11.01)"
        verbose_name_plural = "MRM Schedules (11.01)"

class MRMScheduleItem_11_01(models.Model):
    schedule = models.ForeignKey(MRMSchedule_11_01, on_delete=models.CASCADE, related_name="items")
    meeting_no = models.CharField(max_length=50)
    plan_date = models.DateField(blank=True, null=True)
    actual_date = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)


class MRMNotice_11_02(ISOApprovalModel):
    date = models.DateField()
    from_person = models.CharField(max_length=150)
    to_person = models.CharField(max_length=150)
    sub = models.CharField(max_length=255)
    mrm_no = models.CharField(max_length=50)
    held_on_date = models.DateField()
    time = models.CharField(max_length=100)
    location = models.CharField(max_length=255, default="Chief Executive Office")

    class Meta:
        verbose_name = "MRM Notice (11.02)"
        verbose_name_plural = "MRM Notices (11.02)"

class MRMNoticeParticipant(models.Model):
    notice = models.ForeignKey(MRMNotice_11_02, on_delete=models.CASCADE, related_name="items")
    participant_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)


class MRMAgenda_11_03(ISOApprovalModel):
    mrm_date = models.DateField()
    mrm_time = models.CharField(max_length=100)
    mrm_no = models.CharField(max_length=50)

    class Meta:
        verbose_name = "MRM Agenda (11.03)"
        verbose_name_plural = "MRM Agendas (11.03)"

class MRMAgendaItem(models.Model):
    agenda = models.ForeignKey(MRMAgenda_11_03, on_delete=models.CASCADE, related_name="items")
    agenda_point = models.CharField(max_length=255)


class MRMForm_11_04(ISOApprovalModel):
    held_on = models.DateField()
    mrm_no = models.CharField(max_length=50)

    class Meta:
        verbose_name = "MRM Form (11.04)"
        verbose_name_plural = "MRM Forms (11.04)"

class MRMFormItem(models.Model):
    form = models.ForeignKey(MRMForm_11_04, on_delete=models.CASCADE, related_name="items")
    agenda_point = models.CharField(max_length=255)
    action_taken = models.CharField(max_length=255)
    responsibility = models.CharField(max_length=150)
    target_date = models.DateField(blank=True, null=True)
    follow_up_by = models.CharField(max_length=150)

from django.db import models
from django.conf import settings

# ==========================================
# LSP-12 Procedure for review of requests
# ==========================================

class AnalysisRequest_12_01(ISOApprovalModel):
    serial_no = models.CharField(max_length=100)
    lab_id = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=50)
    
    customer_name = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    address = models.TextField()
    contact = models.CharField(max_length=100)
    email = models.EmailField()
    cell_no = models.CharField(max_length=50)
    
    sample_id_batch = models.CharField(max_length=150)
    sample_type_name = models.CharField(max_length=150)
    total_weight = models.CharField(max_length=100)
    
    sample_condition = models.CharField(max_length=50, choices=[('Acceptable', 'Acceptable'), ('Non acceptable', 'Non acceptable')])
    uncertainty_required = models.BooleanField(default=False)
    number_of_samples = models.IntegerField(default=1)
    sample_packing_condition = models.CharField(max_length=150)
    
    priority = models.CharField(max_length=50, choices=[('Normal', 'Normal'), ('Urgent', 'Urgent')])
    test_method = models.CharField(max_length=150, blank=True, null=True)
    
    remarks_ok = models.BooleanField(default=False)
    specified_environmental_conditions = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Analysis Request (12.01)"
        verbose_name_plural = "Analysis Requests (12.01)"


class ReleaseSlip_12_02(ISOApprovalModel):
    qc_no = models.CharField(max_length=100)
    sr_no = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=50)
    product_name = models.CharField(max_length=150)
    batch_lot_no = models.CharField(max_length=100)
    mfg_date = models.CharField(max_length=100, blank=True, null=True)
    exp_date = models.CharField(max_length=100, blank=True, null=True)
    total_quantity = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Release Slip (12.02)"
        verbose_name_plural = "Release Slips (12.02)"

class ReleaseSlipActiveIngredient(models.Model):
    slip = models.ForeignKey(ReleaseSlip_12_02, on_delete=models.CASCADE, related_name="active_ingredients")
    parameter = models.CharField(max_length=150)
    standard = models.CharField(max_length=150)
    actual_result = models.CharField(max_length=150)

class ReleaseSlipPhysicalTest(models.Model):
    slip = models.ForeignKey(ReleaseSlip_12_02, on_delete=models.CASCADE, related_name="physical_tests")
    parameter = models.CharField(max_length=150)
    standard = models.CharField(max_length=150)
    actual_result = models.CharField(max_length=150)


class AnalysisReport_12_03(ISOApprovalModel):
    REPORT_TYPES = [('Raw Material', 'Raw Material'), ('Batch Analysis', 'Batch Analysis'), ('Outside Sample', 'Outside Sample')]
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    
    issue_date = models.DateField(blank=True, null=True)
    issue_status = models.CharField(max_length=100, blank=True, null=True)
    
    item_name = models.CharField(max_length=150)
    standard_reference = models.CharField(max_length=150, blank=True, null=True)
    source = models.CharField(max_length=150, default="Vital Agri Nutrients (Pvt) Ltd")
    company = models.CharField(max_length=150, blank=True, null=True)
    
    batch_no = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    mfg_date = models.CharField(max_length=100, blank=True, null=True)
    exp_date = models.CharField(max_length=100, blank=True, null=True)
    
    qc_no = models.CharField(max_length=100)
    receiving_date = models.DateField(blank=True, null=True)
    sampled_received_by = models.CharField(max_length=150)
    sample_quantity = models.CharField(max_length=100)
    
    analysis_time = models.CharField(max_length=100, blank=True, null=True)
    date_of_test = models.DateField(blank=True, null=True)
    temperature = models.CharField(max_length=50, blank=True, null=True)
    humidity = models.CharField(max_length=50, blank=True, null=True)
    
    physical_status = models.CharField(max_length=150, blank=True, null=True)
    color = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Analysis Report (12.03)"
        verbose_name_plural = "Analysis Reports (12.03)"

class AnalysisReportTest(models.Model):
    report = models.ForeignKey(AnalysisReport_12_03, on_delete=models.CASCADE, related_name="tests")
    test_name = models.CharField(max_length=150)
    specs = models.CharField(max_length=150)
    results = models.CharField(max_length=150)
    methods = models.CharField(max_length=150)
    mu = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.CharField(max_length=150, blank=True, null=True)


class LabContract_12_05(ISOApprovalModel):
    effective_date = models.DateField()
    validity = models.CharField(max_length=100, default="two years")

    class Meta:
        verbose_name = "LAB Contract (12.05)"
        verbose_name_plural = "LAB Contracts (12.05)"


# ==========================================
# LSP-13 Uncertainty
# ==========================================

class EstimationOfUncertainty_13_01(ISOApprovalModel):
    parameter = models.CharField(max_length=150)
    equipment_used = models.CharField(max_length=150)
    calculated_mu = models.CharField(max_length=100)
    evaluation_date = models.DateField()

    class Meta:
        verbose_name = "Estimation of Uncertainty (13.01)"
        verbose_name_plural = "Estimations of Uncertainty (13.01)"


class DecisionRule_13_02(ISOApprovalModel):
    active_range = models.CharField(max_length=150, default="Upto 2.5 | 2.5-10 | 10-25 | 25-50 | >50")
    fad_tolerances = models.CharField(max_length=150, default="0.15 | 0.1 | 0.06 | 0.05 | 0.03")

    class Meta:
        verbose_name = "Decision Rule (13.02)"
        verbose_name_plural = "Decision Rules (13.02)"

class DecisionRuleItem(models.Model):
    rule = models.ForeignKey(DecisionRule_13_02, on_delete=models.CASCADE, related_name="items")
    test_parameter = models.CharField(max_length=150)
    active_ingredient = models.CharField(max_length=150)
    fad_lower_limit = models.CharField(max_length=100)
    fad_upper_limit = models.CharField(max_length=100)
    qc_lab_mu = models.CharField(max_length=100)
    qc_lower_limit = models.CharField(max_length=100)
    qc_upper_limit = models.CharField(max_length=100)


# ==========================================
# LSP-14 Procedure for Non Conformence
# ==========================================

class NonConformanceForm_14_01(ISOApprovalModel):
    description = models.TextField()
    SOURCE_CHOICES = [
        ('Audit NC', 'Audit NC'), ('Laboratory Activities', 'Laboratory Activities'),
        ('Suggestion', 'Suggestion'), ('PT/ILC', 'PT/ILC'), ('Complaint', 'Complaint'),
        ('Customer Feedback', 'Customer Feedback'), ('Risk Assessment', 'Risk Assessment'),
        ('Any Other', 'Any Other')
    ]
    source = models.CharField(max_length=150, choices=SOURCE_CHOICES)
    initiated_by = models.CharField(max_length=150)
    date = models.DateField()
    nc_no = models.CharField(max_length=100)
    
    impact_on_previous_result = models.BooleanField(default=False)
    
    RISK_LEVELS = [('Very Low', 'Very Low'), ('Low', 'Low'), ('Moderate', 'Moderate'), ('High', 'High'), ('Very High', 'Very High')]
    level_of_risk = models.CharField(max_length=50, choices=RISK_LEVELS)
    
    NC_TYPES = [('Essential', 'Essential'), ('Minor Non- Essential', 'Minor Non- Essential')]
    nc_type = models.CharField(max_length=50, choices=NC_TYPES)
    
    acceptance = models.CharField(max_length=50, choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected')])

    class Meta:
        verbose_name = "Non-Conformance Form (14.01)"
        verbose_name_plural = "Non-Conformance Forms (14.01)"


class NonConformanceLog_14_02(ISOApprovalModel):
    log_name = models.CharField(max_length=150, default="Non Conformance Log")

    class Meta:
        verbose_name = "Non Conformance Log (14.02)"
        verbose_name_plural = "Non Conformance Logs (14.02)"

class NonConformanceLogItem(models.Model):
    log = models.ForeignKey(NonConformanceLog_14_02, on_delete=models.CASCADE, related_name="items")
    nc_no = models.CharField(max_length=100)
    date = models.DateField()
    non_conformance_description = models.TextField()
    source = models.CharField(max_length=150)
    initiated_by = models.CharField(max_length=150)


# ==========================================
# LSP-15 Complaints Handling
# ==========================================

class ComplaintRegistration_15_01(ISOApprovalModel):
    customer_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    contact_no = models.CharField(max_length=100)
    company_name = models.CharField(max_length=150)
    date_of_registration = models.DateField()
    id_of_complaint = models.CharField(max_length=100)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    
    complaint_received_by = models.CharField(max_length=150)
    received_by_designation = models.CharField(max_length=150)
    date_of_complaint_receive = models.DateField()
    
    complaint_nature = models.CharField(max_length=50, choices=[('Acceptable', 'Acceptable'), ('Rejected', 'Rejected')])
    complaint_details = models.TextField()
    corrective_action_person = models.CharField(max_length=150)
    complaint_close_expected_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Complaint Registration (15.01)"
        verbose_name_plural = "Complaint Registrations (15.01)"


class CustomerComplaintLogSheet_15_02(ISOApprovalModel):
    month_year = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Customer Complaint Log Sheet (15.02)"
        verbose_name_plural = "Customer Complaint Log Sheets (15.02)"

class ComplaintLogItem(models.Model):
    log_sheet = models.ForeignKey(CustomerComplaintLogSheet_15_02, on_delete=models.CASCADE, related_name="items")
    date = models.DateField()
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=100)
    nature_of_complaint = models.CharField(max_length=255)
    employee_receiving = models.CharField(max_length=150)
    remarks = models.CharField(max_length=255, blank=True, null=True)


class CustomerAgreement_15_03(ISOApprovalModel):
    dear_name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Customer Agreement (15.03)"
        verbose_name_plural = "Customer Agreements (15.03)"

class CustomerAgreementItem(models.Model):
    agreement = models.ForeignKey(CustomerAgreement_15_03, on_delete=models.CASCADE, related_name="items")
    equipment_name = models.CharField(max_length=150)
    qty = models.CharField(max_length=50)
    company_origin = models.CharField(max_length=150)
    test_performed = models.CharField(max_length=150)
    approx_rep_time = models.CharField(max_length=100)
    ac_na = models.CharField(max_length=50)


class ComplaintOutcomeLetter_15_04(ISOApprovalModel):
    customer_name = models.CharField(max_length=150)
    customer_address = models.TextField()
    dear_name = models.CharField(max_length=150)
    
    letter_body = models.TextField(default="At Vital Agri Nutrients Quality Control Lab we value all of customers and strive to resolve all customer complaints to the satisfaction of our customers.\nWe admit that there was a mistake. We apologize for that. Please contact us because we have made a mistake.")

    class Meta:
        verbose_name = "Complaint Outcome Letter (15.04)"
        verbose_name_plural = "Complaint Outcome Letters (15.04)"
