from django.contrib import messages
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.admin import TabularInline, StackedInline
from simple_history.admin import SimpleHistoryAdmin
from django.utils import timezone
from .models import Parameter, TestMethod, TestResult

@admin.register(Parameter)
class ParameterAdmin(ModelAdmin):
    list_display = ('name', 'default_unit')

@admin.register(TestMethod)
class TestMethodAdmin(ModelAdmin):
    list_display = ('name', 'is_accredited')
    list_filter = ('is_accredited',)


@admin.action(description='▶️ Submit Result for AQCM Verification')
def submit_test_for_verification(modeladmin, request, queryset):
    from django.utils import timezone
    updated = queryset.filter(status__in=['ASSIGNED', 'IN_PROGRESS']).update(status='PENDING_VERIFICATION', tested_at=timezone.now(), analyst=request.user)
    modeladmin.message_user(request, f"{updated} test(s) submitted to AQCM for verification.", messages.SUCCESS)

@admin.action(description='✔️ Verify Test Result (AQCM)')
def verify_test_result(modeladmin, request, queryset):
    from django.utils import timezone
    updated = queryset.filter(status='PENDING_VERIFICATION').update(status='VERIFIED', reviewed_by=request.user, reviewed_at=timezone.now())
    modeladmin.message_user(request, f"{updated} test(s) verified.", messages.SUCCESS)

@admin.register(TestResult)
class TestResultAdmin(ModelAdmin, SimpleHistoryAdmin):

    list_display = ('id', 'sample', 'result_type', 'parameter', 'assigned_to', 'result_value', 'unit', 'status', 'analyst')
    list_editable = ('assigned_to', 'status')
    actions = [submit_test_for_verification, verify_test_result]
    list_filter = ('result_type', 'status', 'parameter', 'method')
    search_fields = ('sample__sample_id', 'parameter__name')
    readonly_fields = ('tested_at', 'reviewed_at', 'get_qc_metrics')
    
    fieldsets = (
        ('Test Information', {
            'fields': ('sample', 'parameter', 'method', 'result_type')
        }),
        ('QC Specific Fields', {
            'fields': ('parent_result', 'target_value', 'get_qc_metrics'),
            'classes': ('collapse',),
            'description': 'Used only for Blanks, Duplicates, and CRMs.'
        }),
        ('Results', {
            'fields': ('result_value', 'unit', 'measurement_uncertainty', 'equipment_used', 'reagents_used', 'remarks')
        }),
        ('Traceability & Workflow', {
            'fields': ('analyst', 'tested_at', 'status', 'reviewed_by', 'reviewed_at')
        }),
    )
    
    def get_qc_metrics(self, obj):
        if obj.result_type == 'CRM' and obj.qc_recovery_percentage is not None:
            return f"Recovery: {obj.qc_recovery_percentage}%"
        elif obj.result_type == 'DUPLICATE' and obj.qc_rpd is not None:
            return f"RPD: {obj.qc_rpd}%"
        return "N/A"
    get_qc_metrics.short_description = "QC Metrics"

    def save_model(self, request, obj, form, change):
        # Auto-assign the analyst if it's a new record and analyst isn't set
        if not obj.pk and not hasattr(obj, 'analyst_id') or obj.analyst is None:
            obj.analyst = request.user
            
        # If status changes to APPROVED and reviewed_by is not set, set it to current user
        if obj.status == 'APPROVED' and obj.reviewed_by is None:
            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()
            
        super().save_model(request, obj, form, change)




