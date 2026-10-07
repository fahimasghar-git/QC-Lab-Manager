from django.db import models
from simple_history.models import HistoricalRecords

from django.conf import settings
from testing.models import TestResult

class Document(models.Model):
    history = HistoricalRecords()

    STATUS_CHOICES = [
        ('DRAFT', 'Draft (Under Review)'),
        ('ACTIVE', 'Active / Approved for Use'),
        ('OBSOLETE', 'Obsolete (Do Not Use)'),
    ]

    DOC_TYPES = [
        ('SOP', 'Standard Operating Procedure'),
        ('POLICY', 'Quality Policy'),
        ('FORM', 'Form / Template'),
        ('MANUAL', 'Quality Manual'),
    ]

    document_id = models.CharField(max_length=50, unique=True, help_text="e.g., SOP-CHEM-01")
    title = models.CharField(max_length=200)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES, default='SOP')
    
    version = models.CharField(max_length=20, help_text="e.g., v1.0")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    file = models.FileField(upload_to='documents/', help_text="Upload PDF version of the document")
    
    issue_date = models.DateField(blank=True, null=True)
    next_review_date = models.DateField(blank=True, null=True, help_text="ISO 17025 requires periodic review of documents")
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='authored_docs')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='approved_docs', blank=True, null=True)



    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_documents', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_documents', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    doc_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    class Meta:
        verbose_name = 'Document (QCL-FRM-7.01)'
        verbose_name_plural = 'Documents (QCL-FRM-7.01)'

    def __str__(self):
        return f"{self.document_id} - {self.title} ({self.version})"

class NonConformance(models.Model):
    history = HistoricalRecords()

    STATUS_CHOICES = [
        ('OPEN', 'Open - Investigation Pending'),
        ('INVESTIGATING', 'Under Investigation (RCA)'),
        ('CAPA_IMPLEMENTED', 'CAPA Implemented - Monitoring'),
        ('CLOSED', 'Closed'),
    ]
    
    nc_id = models.CharField(max_length=50, unique=True, help_text="e.g., NC-2026-001")
    # QCL-FRM-14.01 Fields
    NC_SOURCE_CHOICES = [
        ('AUDIT', 'Audit NC'),
        ('LAB', 'Laboratory Activities'),
        ('SUGGESTION', 'Suggestion'),
        ('PT_ILC', 'PT/ILC'),
        ('COMPLAINT', 'Complaint'),
        ('FEEDBACK', 'Customer Feedback'),
        ('RISK', 'Risk Assessment'),
        ('OTHER', 'Any Other'),
    ]
    source = models.CharField(max_length=20, choices=NC_SOURCE_CHOICES, default='LAB')
    
    impact_on_previous_result = models.BooleanField(default=False)
    
    RISK_LEVEL_CHOICES = [
        ('VERY_LOW', 'Very Low'),
        ('LOW', 'Low'),
        ('MODERATE', 'Moderate'),
        ('HIGH', 'High'),
        ('VERY_HIGH', 'Very High'),
    ]
    level_of_risk = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='MODERATE')
    
    nc_type = models.CharField(max_length=30, choices=[('ESSENTIAL', 'Essential'), ('MINOR', 'Minor Non-Essential')], default='ESSENTIAL')
    
    acceptance_status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING')
    
    withhold_reports = models.BooleanField(default=False)
    halt_work = models.BooleanField(default=False)
    recall_work = models.BooleanField(default=False)
    
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_ncs', help_text="AQCM")
    evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluated_ncs', help_text="QCM")

    
    date_identified = models.DateField(auto_now_add=True)
    
    description = models.TextField(help_text="Detailed description of the non-conforming work or issue")
    identified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='identified_ncs')
    
    related_test = models.ForeignKey(TestResult, on_delete=models.SET_NULL, blank=True, null=True, help_text="Link to specific test result if applicable")
    
    # Root Cause Analysis (RCA) and CAPA
    root_cause_analysis = models.TextField(blank=True, null=True, help_text="General RCA / Summary")
    
    # 14.03 Root Cause Analysis (4M) Fields
    rca_man = models.TextField(blank=True, null=True, verbose_name="Man / Personnel")
    rca_method = models.TextField(blank=True, null=True, verbose_name="Method / Procedure")
    rca_machine = models.TextField(blank=True, null=True, verbose_name="Machine / Equipment")
    rca_material = models.TextField(blank=True, null=True, verbose_name="Material / Environment")
    similar_non_conformance = models.BooleanField(default=False, verbose_name="Similar Non-Conformance exist?")
    rca_carried_out_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rca_carried_out', on_delete=models.RESTRICT, null=True, blank=True)

    corrective_action = models.TextField(blank=True, null=True, help_text="Action taken to eliminate the cause")
    preventive_action = models.TextField(blank=True, null=True, help_text="Action taken to prevent recurrence")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    closed_date = models.DateField(blank=True, null=True)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='closed_ncs', blank=True, null=True)



    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_ncs', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_ncs', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'NonConformance (QCL-FRM-14.01)'
        verbose_name_plural = 'NonConformances (QCL-FRM-14.01)'

    def __str__(self):
        return f"{self.nc_id} - {self.get_status_display()}"

class RecordArchive(models.Model):
    history = HistoricalRecords()

    record_id = models.CharField(max_length=100, help_text="e.g., CoA-FERT-0001")
    record_type = models.CharField(max_length=50, default="Certificate of Analysis")
    
    file = models.FileField(upload_to='archives/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    archived_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    retention_date = models.DateField(help_text="Date until which this record must be retained (e.g., 5 years)")
    
    def __str__(self):
        return f"{self.record_id} ({self.created_at.date()})"

class InternalAudit(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )
    
    audit_id = models.CharField(max_length=50, unique=True, help_text="e.g., AUDIT-2026-01")
    scope = models.CharField(max_length=255, help_text="e.g., Chemistry Lab Methods & Equipment")
    scheduled_date = models.DateField()
    completion_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    
    lead_auditor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    summary_report = models.TextField(blank=True, null=True)

    history = HistoricalRecords()



    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_archives', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_archives', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_archives', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')


    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_audits', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_audits', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_audits', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    class Meta:
        verbose_name = 'InternalAudit (QCL-FRM-10.10)'
        verbose_name_plural = 'InternalAudits (QCL-FRM-10.10)'

    def __str__(self):
        return f"{self.audit_id} - {self.scope}"

class AuditFinding(models.Model):
    SEVERITY_CHOICES = (
        ('OBSERVATION', 'Observation'),
        ('MINOR', 'Minor Non-Conformance'),
        ('MAJOR', 'Major Non-Conformance'),
    )
    
    audit = models.ForeignKey(InternalAudit, related_name='findings', on_delete=models.CASCADE)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    clause_reference = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., ISO 17025: 6.4.2")
    
    # Direct linkage to CAPA as required by 8.8.2
    linked_nc = models.OneToOneField(NonConformance, on_delete=models.SET_NULL, null=True, blank=True, help_text="Linked CAPA for this finding.")
    
    history = HistoricalRecords()


    class Meta:
        verbose_name = 'AuditFinding (QCL-FRM-10.09)'
        verbose_name_plural = 'AuditFindings (QCL-FRM-10.09)'

    def __str__(self):
        return f"Finding for {self.audit.audit_id}: {self.get_severity_display()}"

class Risk(models.Model):
    RISK_TYPE_CHOICES = (
        ('RISK', 'Risk (Threat)'),
        ('OPPORTUNITY', 'Opportunity'),
    )
    STATUS_CHOICES = (
        ('OPEN', 'Open/Active'),
        ('MITIGATED', 'Mitigated/Closed'),
    )
    
    description = models.CharField(max_length=255)
    risk_type = models.CharField(max_length=20, choices=RISK_TYPE_CHOICES, default='RISK')
    
    # Simple 1-5 matrix
    likelihood = models.PositiveIntegerField(default=3, help_text="1 (Rare) to 5 (Almost Certain)")
    impact = models.PositiveIntegerField(default=3, help_text="1 (Negligible) to 5 (Severe)")
    
    mitigation_plan = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    
    identified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    date_identified = models.DateField(auto_now_add=True)
    
    history = HistoricalRecords()

    @property
    def risk_score(self):
        return self.likelihood * self.impact



    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_risks', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_risks', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_risks', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Risk (QCL-FRM-8.01)'
        verbose_name_plural = 'Risks (QCL-FRM-8.01)'

    def __str__(self):
        return f"{self.get_risk_type_display()}: {self.description[:30]} (Score: {self.risk_score})"

class ManagementReview(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
    )
    
    meeting_date = models.DateField()
    chairperson = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    attendees_list = models.TextField(help_text="List of management attendees")
    
    # ISO 17025 Clause 8.9 requires specific inputs and outputs
    inputs_discussion = models.TextField(help_text="Discussion on internal/external changes, customer feedback, previous action items, etc.")
    outputs_and_decisions = models.TextField(blank=True, null=True, help_text="Decisions related to QMS effectiveness, resources needed, and improvement actions.")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    
    history = HistoricalRecords()

    def __str__(self):
        return f"Management Review - {self.meeting_date}"



# QCL-FRM-17.14 Lab Cleaning Inspection Sheet
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        verbose_name = 'Management Review (QCL-FRM-9.01)'
        verbose_name_plural = 'Management Review (QCL-FRM-9.01)s'

class LabCleaningInspection(models.Model):
    history = HistoricalRecords()
    section_area = models.CharField(max_length=150, help_text="e.g. Sample Prep Room")
    month_year = models.CharField(max_length=50, help_text="e.g. October 2026")
    
    # Weekly/Monthly Tasks
    lights_acs_cleaned = models.BooleanField(default=False, verbose_name="Cleaning Of Lights and AC's (Monthly)")
    overall_spray = models.BooleanField(default=False, verbose_name="Overall Cleaning and Spray in Lab (Monthly)")
    racks_cabinets = models.BooleanField(default=False, verbose_name="Cleaning of Racks, Cabinets and Fumehood (Weekly)")
    
    def __str__(self):
        return f"{self.section_area} - {self.month_year}"

    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_cleanings', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_cleanings', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_cleanings', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES_SIG = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES_SIG, default='DRAFT')


    class Meta:
        verbose_name = 'Lab Cleaning Inspection (QCL-FRM-17.14)'
        verbose_name_plural = 'Lab Cleaning Inspection (QCL-FRM-17.14)s'

class LabCleaningDailyRecord(models.Model):
    inspection = models.ForeignKey(LabCleaningInspection, on_delete=models.CASCADE, related_name='daily_records')
    date = models.DateField()
    floor_sinks_taps = models.BooleanField(default=False, verbose_name="Floor, Sanitary Sinks and Taps")
    bench_top_shelves = models.BooleanField(default=False, verbose_name="Bench Top/Shelves")
    equipment = models.BooleanField(default=False, verbose_name="Equipment")
    checked_by = models.CharField(max_length=50, blank=True, null=True)
    verified_by = models.CharField(max_length=50, blank=True, null=True)

# QCL-FRM-20.01 Master List of Records
class MasterListRecord(models.Model):
    history = HistoricalRecords()
    title = models.CharField(max_length=200, verbose_name="Record Title")
    code = models.CharField(max_length=100, verbose_name="Record Code")
    revision_no = models.CharField(max_length=50, verbose_name="Revision No.")
    file_code = models.CharField(max_length=100, verbose_name="File code")
    location = models.CharField(max_length=200, verbose_name="File Location")
    retention_period = models.CharField(max_length=100, verbose_name="Retention Period")
    remarks = models.TextField(blank=True, null=True)
    # Digital Signatures
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)s_prepared", on_delete=models.RESTRICT, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)s_reviewed", on_delete=models.RESTRICT, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)s_approved", on_delete=models.RESTRICT, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    
    def __str__(self):
        return self.title

# QCL-FRM-20.02 Master List of Files and Folders
    class Meta:
        verbose_name = 'Master List of Records (QCL-FRM-20.01)'
        verbose_name_plural = 'Master List of Records (QCL-FRM-20.01)s'

class MasterListFileFolder(models.Model):
    history = HistoricalRecords()
    file_code = models.CharField(max_length=100, verbose_name="File code")
    title = models.CharField(max_length=200, verbose_name="Title of File/Folder/Register")
    volume = models.CharField(max_length=50, verbose_name="Volume")
    keeper = models.CharField(max_length=100, verbose_name="Keeper")
    location = models.CharField(max_length=200, verbose_name="Location")
    folder_status = models.CharField(max_length=50, verbose_name="Status", default="Active")
    # Digital Signatures
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)s_prepared", on_delete=models.RESTRICT, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)s_reviewed", on_delete=models.RESTRICT, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)s_approved", on_delete=models.RESTRICT, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    
    def __str__(self):
        return self.title

# QCL-FRM-21.01 Customer Feedback Form
    class Meta:
        verbose_name = 'Master List of Files (QCL-FRM-20.02)'
        verbose_name_plural = 'Master List of Files (QCL-FRM-20.02)s'

class CustomerFeedback(models.Model):
    history = HistoricalRecords()
    customer_name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    
    SCORE_CHOICES = [(4, 'Excellent A+ (4)'), (3, 'V. Good A (3)'), (2, 'Good B (2)'), (1, 'Poor C (1)')]
    
    q1_delivery_time = models.IntegerField(choices=SCORE_CHOICES, default=4, verbose_name="1. How do you estimate time of delivery of our laboratory reports?")
    q2_politeness = models.IntegerField(choices=SCORE_CHOICES, default=4, verbose_name="2. How do you estimate politeness of our laboratory staff?")
    q3_accuracy = models.IntegerField(choices=SCORE_CHOICES, default=4, verbose_name="3. How do you estimate accuracy of contents of our Laboratory reports?")
    q4_response = models.IntegerField(choices=SCORE_CHOICES, default=4, verbose_name="4. How do you rate our response to your complaints & feedbacks?")
    q5_satisfaction = models.IntegerField(choices=SCORE_CHOICES, default=4, verbose_name="5. Rating of your overall satisfaction level?")
    q6_knowledge = models.IntegerField(choices=SCORE_CHOICES, default=4, verbose_name="6. How do you estimate knowledge of our laboratory analyst?")
    
    comments = models.TextField(blank=True, null=True, verbose_name="Any specific comments / complaint / suggestion or feedback you would like to add:")
    
    @property
    def total_score(self):
        return self.q1_delivery_time + self.q2_politeness + self.q3_accuracy + self.q4_response + self.q5_satisfaction + self.q6_knowledge
        
    @property
    def percentage(self):
        return round((self.total_score / 24.0) * 100, 2)
        
    def __str__(self):
        return f"Feedback - {self.customer_name} ({self.date})"

    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_feedbacks', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewed_feedbacks', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_feedbacks', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES_SIG = [('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES_SIG, default='DRAFT')


    class Meta:
        verbose_name = 'Customer Feedback (QCL-FRM-21.01)'
        verbose_name_plural = 'Customer Feedback (QCL-FRM-21.01)s'

class LabCleaningInspection_Update(models.Model):
    class Meta:
        managed = False

class ISODocument(models.Model):
    DOCUMENT_TYPES = [
        ('LSP', 'Laboratory Standard Procedure (LSP)'),
        ('FRM', 'Form (FRM)'),
        ('POL', 'Policy (POL)'),
        ('MAN', 'Manual (LSM)'),
        ('OTHER', 'Other')
    ]
    
    doc_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES, default='LSP')
    document_code = models.CharField(max_length=50, unique=True, help_text="e.g., QCL-LSP-01")
    title = models.CharField(max_length=255)
    revision_number = models.CharField(max_length=20, default="00")
    issue_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to='iso_documents/', null=True, blank=True)
    
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('OBSOLETE', 'Obsolete')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="iso_docs_prepared", on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="iso_docs_reviewed", on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="iso_docs_approved", on_delete=models.SET_NULL, null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "ISO Document (LSP/POL/FRM)"
        verbose_name_plural = "ISO Documents Database"
        ordering = ['doc_type', 'document_code']

    def __str__(self):
        return f"{self.document_code} - {self.title}"
