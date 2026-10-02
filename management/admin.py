from lims_core.admin_mixins import DigitalSignatureMixin
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.contrib import admin
from django.shortcuts import render
from unfold.admin import ModelAdmin
from unfold.admin import TabularInline, StackedInline
from simple_history.admin import SimpleHistoryAdmin
from .models import Document, NonConformance, RecordArchive
from django.utils import timezone



@admin.register(RecordArchive)
class RecordArchiveAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('record_id', 'record_type', 'created_at', 'archived_by', 'retention_date')
    list_filter = ('record_type', 'created_at', 'retention_date')
    search_fields = ('record_id',)
    readonly_fields = ('record_id', 'record_type', 'file', 'created_at', 'archived_by', 'retention_date')
    
    # We generally don't want people manually adding to the archive from the admin UI,
    # it should be automated by the CoA generation.
    def has_add_permission(self, request):
        return False

@admin.register(Document)
class DocumentAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('document_id', 'title', 'version', 'status', 'issue_date', 'next_review_date')
    list_filter = ('status', 'doc_type', 'next_review_date')
    search_fields = ('document_id', 'title')
    readonly_fields = ('author',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        
        # If status changed to ACTIVE and it wasn't before, log the approver
        if obj.status == 'ACTIVE' and not obj.approved_by:
            obj.approved_by = request.user
            if not obj.issue_date:
                obj.issue_date = timezone.now().date()
                
        super().save_model(request, obj, form, change)

    @admin.action(description='🖨️ Print Non-Conformance Form (QCL-FRM-14.01)')

    @admin.action(description='Print Non-Conformance Log (QCL-FRM-14.02)')
    def print_non_conformance_log(self, request, queryset):
        # usually 14.02 is a log of all NCs, but we'll print what is selected
        html_string = render_to_string('management/non_conformance_log.html', {'ncs': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-14.02_NC_Log.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

    @admin.action(description='Print Root Cause Analysis Form (QCL-FRM-14.03)')
    def print_root_cause_analysis(self, request, queryset):
        html_string = render_to_string('management/root_cause_analysis_form.html', {'ncs': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-14.03_RCA.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

    def print_non_conformance(self, request, queryset):
        html_string = render_to_string('management/non_conformance_form.html', {'ncs': queryset, 'request': request})
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-14.01_Non_Conformance.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response



@admin.register(NonConformance)
class NonConformanceAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('nc_id', 'date_identified', 'status', 'identified_by')
    list_filter = ('status', 'date_identified')
    search_fields = ('nc_id', 'description', 'root_cause_analysis')
    readonly_fields = ('identified_by', 'date_identified', 'closed_date', 'closed_by')
    actions = ['print_non_conformance', 'print_non_conformance_log', 'print_root_cause_analysis']
    
    fieldsets = (
        ('Identification & Source', {
            'fields': ('nc_id', 'date_identified', 'source', 'description', 'identified_by', 'related_test', 'status')
        }),
        ('Review & Risk Assessment', {
            'fields': (
                'impact_on_previous_result', 'level_of_risk', 'nc_type',
                'acceptance_status', 'withhold_reports', 'halt_work', 'recall_work',
                'reviewed_by', 'evaluated_by'
            )
        }),
        ('Root Cause Analysis & CAPA', {
            'fields': (
                'root_cause_analysis', 'rca_man', 'rca_method', 'rca_machine', 'rca_material',
                'similar_non_conformance', 'rca_carried_out_by',
                'corrective_action', 'preventive_action'
            )
        }),
        ('Closure', {
            'fields': ('closed_by', 'closed_date')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.identified_by = request.user
        
        if obj.status == 'CLOSED' and not obj.closed_by:
            obj.closed_by = request.user
            obj.closed_date = timezone.now().date()
            
        super().save_model(request, obj, form, change)

    @admin.action(description='🖨️ Print Non-Conformance Form (QCL-FRM-14.01)')

    @admin.action(description='Print Non-Conformance Log (QCL-FRM-14.02)')
    def print_non_conformance_log(self, request, queryset):
        # usually 14.02 is a log of all NCs, but we'll print what is selected
        html_string = render_to_string('management/non_conformance_log.html', {'ncs': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-14.02_NC_Log.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

    @admin.action(description='Print Root Cause Analysis Form (QCL-FRM-14.03)')
    def print_root_cause_analysis(self, request, queryset):
        html_string = render_to_string('management/root_cause_analysis_form.html', {'ncs': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-14.03_RCA.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

    def print_non_conformance(self, request, queryset):
        html_string = render_to_string('management/non_conformance_form.html', {'ncs': queryset, 'request': request})
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-14.01_Non_Conformance.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response



from .models import InternalAudit, AuditFinding

class AuditFindingInline(TabularInline):
    model = AuditFinding
    extra = 1

@admin.register(InternalAudit)
class InternalAuditAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('audit_id', 'scope', 'scheduled_date', 'status', 'lead_auditor')
    list_filter = ('status', 'scheduled_date')
    search_fields = ('audit_id', 'scope')
    inlines = [AuditFindingInline]

# AuditFinding is primarily managed via the inline on InternalAudit, 
# but can be registered separately if needed.
@admin.register(AuditFinding)
class AuditFindingAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('audit', 'severity', 'clause_reference', 'linked_nc')
    list_filter = ('severity', 'audit')

from .models import Risk, ManagementReview, LabCleaningInspection, LabCleaningDailyRecord, MasterListRecord, MasterListFileFolder, CustomerFeedback

@admin.register(Risk)
class RiskAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('description', 'risk_type', 'likelihood', 'impact', 'risk_score', 'status')
    list_filter = ('risk_type', 'status')
    search_fields = ('description',)

@admin.register(ManagementReview)
class ManagementReviewAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('meeting_date', 'chairperson', 'status')
    list_filter = ('status', 'meeting_date')
    search_fields = ('inputs_discussion', 'outputs_and_decisions')



class LabCleaningDailyRecordInline(TabularInline):
    model = LabCleaningDailyRecord
    extra = 7

@admin.register(LabCleaningInspection)
class LabCleaningInspectionAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('section_area', 'month_year')
    inlines = [LabCleaningDailyRecordInline]
    actions = ['print_cleaning_inspection']
    
    @admin.action(description='Print Lab Cleaning Inspection Sheet (17.14)')
    def print_cleaning_inspection(self, request, queryset):
        html_string = render_to_string('management/lab_cleaning_inspection.html', {'inspections': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-17.14_Cleaning_Inspection.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

@admin.register(MasterListRecord)
class MasterListRecordAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('title', 'code', 'revision_no', 'location', 'retention_period')
    actions = ['print_master_list_records']
    
    @admin.action(description='Print Master List of Records (20.01)')
    def print_master_list_records(self, request, queryset):
        html_string = render_to_string('management/master_list_records.html', {'records': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-20.01_Master_List_Records.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

@admin.register(MasterListFileFolder)
class MasterListFileFolderAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ("title", "file_code", "volume", "keeper", "folder_status", "status")
    actions = ['print_master_list_files']
    
    @admin.action(description='Print Master List of Files and Folders (20.02)')
    def print_master_list_files(self, request, queryset):
        html_string = render_to_string('management/master_list_files.html', {'files': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-20.02_Master_List_Files.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('customer_name', 'date', 'percentage')
    actions = ['print_customer_feedback']
    
    @admin.action(description='Print Customer Feedback Form (21.01)')
    def print_customer_feedback(self, request, queryset):
        html_string = render_to_string('management/customer_feedback.html', {'feedbacks': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-21.01_Customer_Feedback.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response
