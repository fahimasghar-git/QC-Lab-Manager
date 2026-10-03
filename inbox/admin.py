from django.contrib import admin
from .models import PendingApproval, PendingVerification, MyAssignedTest
from samples.admin import SampleAdmin
from testing.admin import TestResultAdmin

@admin.register(PendingApproval)
class PendingApprovalAdmin(SampleAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='PENDING_APPROVAL')

@admin.register(PendingVerification)
class PendingVerificationAdmin(SampleAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='PENDING_VERIFICATION')

@admin.register(MyAssignedTest)
class MyAssignedTestAdmin(TestResultAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(analyst=request.user, status__in=['ASSIGNED', 'IN_PROGRESS'])


from .models import (
    PendingDocumentApproval, PendingNCApproval, PendingAuditApproval, 
    PendingCompetencyApproval, PendingSupplierApproval, PendingPRApproval
)
from management.admin import DocumentAdmin, NonConformanceAdmin, InternalAuditAdmin
from resources.admin import CompetencyRecordAdmin, SupplierAdmin, PurchaseRequestAdmin

def get_approval_qs(self, request):
    return super(self.__class__, self).get_queryset(request).filter(status='PENDING_APPROVAL')

@admin.register(PendingDocumentApproval)
class PendingDocumentApprovalAdmin(DocumentAdmin):
    def get_queryset(self, request): return get_approval_qs(self, request)

@admin.register(PendingNCApproval)
class PendingNCApprovalAdmin(NonConformanceAdmin):
    def get_queryset(self, request): return get_approval_qs(self, request)

@admin.register(PendingAuditApproval)
class PendingAuditApprovalAdmin(InternalAuditAdmin):
    def get_queryset(self, request): return get_approval_qs(self, request)

@admin.register(PendingCompetencyApproval)
class PendingCompetencyApprovalAdmin(CompetencyRecordAdmin):
    def get_queryset(self, request): return get_approval_qs(self, request)

@admin.register(PendingSupplierApproval)
class PendingSupplierApprovalAdmin(SupplierAdmin):
    def get_queryset(self, request): return get_approval_qs(self, request)

@admin.register(PendingPRApproval)
class PendingPRApprovalAdmin(PurchaseRequestAdmin):
    def get_queryset(self, request): return get_approval_qs(self, request)

