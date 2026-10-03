from django.db import models
from samples.models import Sample
from testing.models import TestResult

class PendingApproval(Sample):
    class Meta:
        proxy = True
        app_label = 'inbox'
        verbose_name = 'Pending QCM Approval'
        verbose_name_plural = 'Pending QCM Approvals'

class PendingVerification(Sample):
    class Meta:
        proxy = True
        app_label = 'inbox'
        verbose_name = 'Pending AQCM Review'
        verbose_name_plural = 'Pending AQCM Reviews'

class MyAssignedTest(TestResult):
    class Meta:
        proxy = True
        app_label = 'inbox'
        verbose_name = 'My Assigned Test'
        verbose_name_plural = 'My Assigned Tests'


from management.models import Document, NonConformance, InternalAudit
from resources.models import CompetencyRecord, Supplier, PurchaseRequest, EquipmentMaintenance

# QCM Approvals
class PendingDocumentApproval(Document):
    class Meta:
        proxy = True
        app_label = 'inbox'
        verbose_name = 'Pending QCM Approval (Documents)'
        verbose_name_plural = 'Pending QCM Approvals (Documents)'

class PendingNCApproval(NonConformance):
    class Meta:
        proxy = True
        app_label = 'inbox'
        verbose_name = 'Pending QCM Approval (Non-Conformances)'
        verbose_name_plural = 'Pending QCM Approvals (Non-Conformances)'

class PendingAuditApproval(InternalAudit):
    class Meta:
        proxy = True
        app_label = 'inbox'
        verbose_name = 'Pending QCM Approval (Audits)'
        verbose_name_plural = 'Pending QCM Approvals (Audits)'

class PendingCompetencyApproval(CompetencyRecord):
    class Meta:
        proxy = True
        app_label = 'inbox'
        verbose_name = 'Pending QCM Approval (Competency)'
        verbose_name_plural = 'Pending QCM Approvals (Competency)'

class PendingSupplierApproval(Supplier):
    class Meta:
        proxy = True
        app_label = 'inbox'
        verbose_name = 'Pending QCM Approval (Suppliers)'
        verbose_name_plural = 'Pending QCM Approvals (Suppliers)'

class PendingPRApproval(PurchaseRequest):
    class Meta:
        proxy = True
        app_label = 'inbox'
        verbose_name = 'Pending QCM Approval (Purchase Requests)'
        verbose_name_plural = 'Pending QCM Approvals (Purchase Requests)'

