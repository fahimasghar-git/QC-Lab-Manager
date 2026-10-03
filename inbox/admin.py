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
