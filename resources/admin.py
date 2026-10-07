from lims_core.admin_mixins import DigitalSignatureMixin
from django.contrib import admin
from django.shortcuts import render
from unfold.admin import ModelAdmin
from .pdf_utils import generate_iso_pdf
from .approval_utils import action_mark_prepared, action_mark_checked, action_mark_approved
from unfold.admin import TabularInline, StackedInline
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    EnvironmentalMonitoring_3_01, EnvironmentalMonitoringItem,
    HumidityControlChart_3_02, HumidityControlItem,
    TemperatureControlChart_3_03, TemperatureControlItem,
    CorrectiveActionRequest_4_01,
    MasterListEquipment_4_02, MasterListEquipmentItem,
    EquipmentMaintenanceRecord_4_03, MaintenanceRecordItem,
    CalibrationProgram_4_04, CalibrationProgramItem
)


from .models import (
    CRMList_5_01, CRMListItem,
    SupplierSelection_6_01, SupplierSelectionCriteria,
    ApprovedSupplierServiceProvider_6_02, ApprovedSupplierItem,
    ExternalProviderEvaluation_6_03, ExternalProviderEvaluationCriteria,
    SupplierPerformanceMonitoring_6_04, SupplierPerformanceItem,
    ComparativeStatement_6_05, ComparativeStatementItem_6_05,
    SupplierEvaluationPlan_6_06, SupplierEvaluationPlanItem_6_06,
    StorePurchaseDemand_6_07, StorePurchaseDemandItem,
    ProductsServicesInspection_6_08, ProductsServicesInspectionItem
)


from .models import (
    MasterListDocument_7_01, MasterListDocumentItem,
    DocumentChangeRequest_7_02
)


from .models import (
    RiskManagementSheet_8_01, RiskManagementItem,
    OpportunityAssessment_8_02, OpportunityAssessmentItem,
    CorrectiveActionRequest_9_01, CorrectiveActionsRequestLog_9_02, CorrectiveActionsLogItem,
    RootCauseAnalysisForm_9_04,
    AuditNotification_10_01, AuditSchedule_10_02, AuditScheduleItem, AuditScheduleDeptItem,
    MRMSchedule_10_03, MRMScheduleItem, TrainedAuditorsList_10_04, TrainedAuditorItem,
    AuditorCompetence_10_05, ConfidentialAgreementAuditors_10_06, ImpartialityForm_10_07,
    InternalAuditForm_10_08, InternalAuditCheckList_10_09, InternalAuditCheckListItem,
    AuditReport_10_10, MRMSchedule_11_01, MRMScheduleItem_11_01, MRMNotice_11_02, MRMNoticeParticipant,
    MRMAgenda_11_03, MRMAgendaItem, MRMForm_11_04, MRMFormItem
)

from .models import AuthorizedPersonnelList_2_06, NewInductionOrientation_2_11, InductionOrientationItem, Equipment, CalibrationRecord, EquipmentMaintenance, CompetencyRecord, CompetencyEvaluation, ReagentStandard, Supplier, PurchaseRequest, ProductServiceInspection, PersonnelAuthorization, ComparativeStatement, ComparativeStatementSupplier, SupplierEvaluationPlan, SupplierEvaluationPlanItem
from django.utils import timezone


from django.utils import timezone
from django.contrib import admin

@admin.action(description="Submit selected for Approval")
def submit_for_approval(modeladmin, request, queryset):
    updated = 0
    for obj in queryset:
        if hasattr(obj, 'status') and obj.status == 'DRAFT':
            obj.status = 'PENDING_APPROVAL'
            if hasattr(obj, 'prepared_by') and not obj.prepared_by:
                obj.prepared_by = request.user
                if hasattr(obj, 'prepared_at'):
                    obj.prepared_at = timezone.now()
            obj.save()
            updated += 1
    modeladmin.message_user(request, f"Successfully submitted {updated} records for approval.")

@admin.action(description="Approve selected records")
def approve_records(modeladmin, request, queryset):
    updated = 0
    for obj in queryset:
        if hasattr(obj, 'status') and obj.status == 'PENDING_APPROVAL':
            obj.status = 'APPROVED'
            if hasattr(obj, 'approved_by'):
                obj.approved_by = request.user
                if hasattr(obj, 'approved_at'):
                    obj.approved_at = timezone.now()
            elif hasattr(obj, 'approved_by'):
                obj.authorized_by = request.user
            obj.save()
            updated += 1
    modeladmin.message_user(request, f"Successfully approved {updated} records.")

@admin.register(ReagentStandard)
class ReagentStandardAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    actions = [submit_for_approval, approve_records]
    list_display = ('name', 'lot_number', 'supplier', 'expiry_date', 'status')
    list_filter = ('status', 'supplier')
    search_fields = ('name', 'lot_number', 'certificate_reference')
    readonly_fields = ('receipt_date',)
    
    # Simple logic to auto-expire things could be added here or via a cron job
    
class CalibrationRecordInline(TabularInline):
    model = CalibrationRecord
    extra = 1

@admin.register(Equipment)
class EquipmentAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('name', 'identification_no', 'serial_number', 'status', 'location', 'calibration_frequency')
    list_filter = ('status', 'location', 'calibration_frequency')
    search_fields = ('name', 'identification_no', 'serial_number')
    actions = [submit_for_approval, approve_records, 'print_master_list', 'print_calibration_program']

    @admin.action(description='🖨️ Print Master List of Equipments (QCL-FRM-4.02)')
    def print_master_list(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/equipment_master_list.html', {'equipments': queryset})

    @admin.action(description='🖨️ Print Calibration Program (QCL-FRM-4.04)')
    def print_calibration_program(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/calibration_program.html', {'equipments': queryset})

    inlines = [CalibrationRecordInline]
    
    fieldsets = (
        ('Equipment Identification', {
            'fields': ('name', 'manufacturer', 'model_number', 'serial_number')
        }),
        ('Status & Location', {
            'fields': ('status', 'location', 'date_received', 'date_put_into_service')
        }),
    )


@admin.register(CompetencyRecord)
class CompetencyRecordAdmin(ModelAdmin):
    list_display = ('analyst', 'competency_level', 'total_score', 'status', 'training_date')
    list_filter = ('status', 'analyst')
    search_fields = ('analyst__username', 'test_method__name')
    readonly_fields = ('total_score', 'competency_level')
    actions = [submit_for_approval, approve_records, 'print_competency_report']

    fieldsets = (
        ('Analyst Information', {
            'fields': ('analyst', 'test_method', 'training_date', 'status')
        }),
        ('QCL-FRM-1.04 (Competency Scores 1-4)', {
            'fields': (
                'score_education', 'score_qualification', 'score_experience', 
                'score_training', 'score_technical_knowledge', 'score_skills', 
                'score_challenge_testing', 'score_proficiency_testing'
            ),
            'description': '4 = High Competence | 3 = Partial Competence | 2 = Low Competence | 1 = No Competence'
        }),
        ('Authorization & Approval', {
            'fields': ('total_score', 'competency_level', 'assessor', 'approved_by', 'comments', 'notes')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change or not getattr(obj, 'authorized_by_id', None):
            obj.authorized_by = request.user
        super().save_model(request, obj, form, change)

    @admin.action(description='🖨️ Print Competency Report (QCL-FRM-1.04)')
    def print_competency_report(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/competency_report.html', {'records': queryset})



@admin.register(CompetencyEvaluation)
class CompetencyEvaluationAdmin(ModelAdmin):
    list_display = ('analyst', 'evaluation_date', 'supervisor')
    list_filter = ('evaluation_date', 'analyst')
    search_fields = ('analyst__username', 'supervisor__username')
    actions = [submit_for_approval, approve_records, 'print_competency_evaluation']

    fieldsets = (
        ('Basic Information (Section A)', {
            'fields': ('analyst', 'supervisor', 'evaluation_date')
        }),
        ('Evaluation Description (Section C)', {
            'fields': (
                'score_analysis_skills', 'score_equipment_handling', 'score_iso_awareness',
                'score_testing_skills', 'score_sample_prep'
            ),
            'description': 'Scale: ND, AC, C, HC, E. (If ND in any parameter, training is required).'
        }),
        ('Remarks & Conclusion', {
            'fields': ('remarks',)
        }),
    )

    @admin.action(description='🖨️ Print Evaluation of Competency (QCL-FRM-2.09)')
    def print_competency_evaluation(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/competency_evaluation_report.html', {'evaluations': queryset})



    @admin.action(description='Print CRM List (QCL-FRM-5.01)')
    def print_crm_list(self, request, queryset):
        # We only want to print items marked as CRM
        crm_queryset = queryset.filter(is_crm=True)
        html_string = render_to_string('resources/crm_list.html', {'crms': crm_queryset, 'request': request})
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-5.01_CRM_List.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

@admin.register(Supplier)
class SupplierAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('name', 'evaluation_type', 'total_score', 'grading', 'decision', 'last_evaluation_date')
    list_filter = ('decision', 'evaluation_type')
    search_fields = ('name', 'contact_person')
    readonly_fields = ('total_score', 'grading')
    actions = [submit_for_approval, approve_records, 'print_supplier_selection', 'print_approved_supplier_list', 'print_supplier_evaluation', 'print_supplier_monitoring']

    fieldsets = (
        ('Supplier Information', {
            'fields': ('name', 'contact_person', 'email', 'phone', 'evaluation_type')
        }),
        ('Section-A: General Evaluation (0-3)', {
            'fields': (
                'score_market_image', 'score_market_share', 'score_technical_capacity',
                'score_lead_time', 'score_product_quality', 'score_order_processing',
                'score_fulfill_requirements'
            ),
            'description': '0=Poor, 1=Fair, 2=Good, 3=Excellence'
        }),
        ('Section-B & C: Approval', {
            'fields': (
                'total_score', 'grading', 'sample_approved_by_qc', 'decision',
                'remarks', 'evaluated_by', 'approved_by', 'last_evaluation_date', 'next_evaluation_date'
            )
        }),
    )

    @admin.action(description='🖨️ Print External Provider Evaluation (QCL-FRM-6.03)')
    def print_supplier_evaluation(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/supplier_evaluation.html', {'suppliers': queryset})


@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('id', 'item_description', 'quantity_required', 'status', 'requested_by', 'requested_date')
    list_filter = ('status', 'supplier')
    search_fields = ('item_description', 'specification', 'purpose')
    actions = [submit_for_approval, approve_records, 'print_purchase_demand']

    fieldsets = (
        ('Request Details', {
            'fields': ('item_description', 'specification', 'purpose')
        }),
        ('Quantities', {
            'fields': ('quantity_required', 'stock_in_hand')
        }),
        ('Document Control', {
            'fields': ('spd_no', 'insp_mints_no', 'service_call_no')
        }),
        ('Status & Signatures', {
            'fields': ('supplier', 'status', 'requested_by', 'store_keeper', 'approved_by')
        }),
    )

    @admin.action(description='🖨️ Print Store Purchase Demand (QCL-FRM-6.07)')
    def print_purchase_demand(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/store_purchase_demand.html', {'requests': queryset})


@admin.register(EquipmentMaintenance)
class EquipmentMaintenanceAdmin(ModelAdmin):
    list_display = ('equipment', 'maintenance_date', 'maintenance_by')
    list_filter = ('maintenance_date', 'equipment')
    search_fields = ('equipment__name', 'equipment__identification_no', 'maintenance_by')
    actions = [submit_for_approval, approve_records, 'print_maintenance_record']
    
    fieldsets = (
        ('Maintenance Details', {
            'fields': ('equipment', 'maintenance_date', 'parts_repaired_replaced', 'maintenance_by', 'remarks')
        }),
        ('Signatures', {
            'fields': ('prepared_by', 'reviewed_by', 'approved_by')
        }),
    )

    @admin.action(description='🖨️ Print Equipment Maintenance Record (QCL-FRM-4.03)')
    def print_maintenance_record(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/equipment_maintenance_record.html', {'maintenances': queryset})


@admin.register(ProductServiceInspection)
class ProductServiceInspectionAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    actions = [submit_for_approval, approve_records]
    list_display = ('description', 'inspection_type', 'external_provider', 'date_of_receipt', 'status')
    list_filter = ('inspection_type', 'status', 'date_of_receipt')
    search_fields = ('description', 'gate_pass_no', 'pr_po_no', 'invoice_no')
    
    fieldsets = (
        ('Basic Info (QCL-FRM-6.08)', {
            'fields': ('inspection_type', 'description', 'external_provider', 'provider_status')
        }),
        ('Document Tracking', {
            'fields': ('gate_pass_no', 'pr_po_no', 'invoice_no', 'date_of_receipt')
        }),
        ('Products Check (Leave blank if Services)', {
            'fields': (
                'prod_coa_remarks', 'prod_spec_remarks', 'prod_qty_remarks', 
                'prod_lot_remarks', 'prod_mfg_remarks', 'prod_exp_remarks', 'prod_model_remarks'
            ),
            'classes': ('collapse',)
        }),
        ('Services Check (Leave blank if Products)', {
            'fields': (
                'srv_traceability_remarks', 'srv_scope_remarks', 'srv_training_remarks',
                'srv_response_remarks', 'srv_skills_remarks', 'srv_validity_remarks'
            ),
            'classes': ('collapse',)
        }),
        ('Final Status & Approval', {
            'fields': ('status', 'received_by')
        }),
    )
    
    actions = [submit_for_approval, approve_records, 'print_inspection_form']
    
    @admin.action(description='Print Products/Services Inspection Form (QCL-FRM-6.08)')
    def print_inspection_form(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one Inspection for 6.08.", level='ERROR')
            return
        
        inspection = queryset.first()
        html_string = render_to_string('resources/product_service_inspection.html', {'inspection': inspection, 'request': request})
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="QCL-FRM-6.08_Inspection_{inspection.id}.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response



@admin.register(PersonnelAuthorization)
class PersonnelAuthorizationAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('user', 'employee_code', 'designation', 'authorization_date')
    search_fields = ('user__username', 'user__first_name', 'employee_code', 'designation')
    
    actions = [submit_for_approval, approve_records, 'print_authorization_permit', 'print_list_of_authorized_staff']
    
    fieldsets = (
        ('Staff Info', {
            'fields': ('user', 'employee_code', 'designation')
        }),
        ('Instrument Operation (1.01)', {
            'fields': (
                'op_flame_photometer', 'op_uv_vis', 'op_karl_fischer', 'op_kjeldhals', 
                'op_furnace', 'op_ph_meter', 'op_tds_meter', 'op_analytical_balance'
            ),
            'classes': ('collapse',)
        }),
        ('Tests & Parameters (1.01)', {
            'fields': (
                'test_loi', 'test_density', 'test_ph', 'test_conductivity', 'test_tds',
                'test_lod', 'test_weighing', 'test_sieve', 'test_calcium', 'test_sulfur',
                'test_nitrogen', 'test_titrations', 'test_humic_acid', 'test_phosphorus',
                'test_toc', 'test_cn_ratio', 'test_organic_matter', 'test_cec', 'test_sodium',
                'test_zinc', 'test_boron', 'test_copper', 'test_moisture'
            ),
            'classes': ('collapse',)
        }),
        ('Quality & Lab Activities (1.01)', {
            'fields': (
                'act_environmental', 'act_intermediate_checks', 'act_control_chart', 
                'act_sample_receiving', 'act_method_validation', 'act_sample_handling', 
                'act_report_prep', 'act_review_reports', 'act_measurement_uncertainty', 
                'act_internal_auditing', 'act_training_lms', 'act_prep_procedures', 
                'act_approve_reports', 'act_prep_release_slip', 'act_practical_demo', 
                'act_assign_samples', 'act_analyze_samples', 'act_housekeeping', 
                'act_solution_prep', 'act_sample_retaining', 'act_sample_discard', 
                'act_stock_management', 'act_id_non_conformity', 'act_id_improvement', 
                'act_temp_humidity', 'act_cleaning_inspections', 'act_standardization', 
                'act_pt_samples'
            ),
            'classes': ('collapse',)
        }),
        ('Master List Authorizations (1.02)', {
            'fields': (
                'auth_dev_mod', 'auth_perform', 'auth_validation', 'auth_supervision',
                'auth_report_review', 'auth_analysis_results', 'auth_auth_results', 'auth_uncertainty'
            ),
            'classes': ('collapse',)
        }),
        ('Signatures', {
            'fields': ('prepared_by', 'approved_by')
        }),
    )

    @admin.action(description='Print Personnel Authorization Permit (QCL-FRM-1.01)')
    def print_authorization_permit(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one record for the Permit.", level='ERROR')
            return
        
        permit = queryset.first()
        html_string = render_to_string('resources/personnel_authorization_permit.html', {'permit': permit, 'request': request})
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="QCL-FRM-1.01_{permit.user.username}.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

    @admin.action(description='Print List of Authorized Staff (QCL-FRM-1.02)')
    def print_list_of_authorized_staff(self, request, queryset):
        # We print all selected or all available in the queryset
        html_string = render_to_string('resources/list_of_authorized_staff.html', {'staff_list': queryset, 'request': request})
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-1.02_Authorized_Staff.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response




class ComparativeStatementSupplierInline(TabularInline):
    model = ComparativeStatementSupplier
    extra = 3

@admin.register(ComparativeStatement)
class ComparativeStatementAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('item_name', 'date', 'purchase_demand', 'prepared_by')
    search_fields = ('item_name',)
    inlines = [ComparativeStatementSupplierInline]
    actions = [submit_for_approval, approve_records, 'print_comparative_statement']
    
    @admin.action(description='Print Comparative Statement (QCL-FRM-6.05)')
    def print_comparative_statement(self, request, queryset):
        html_string = render_to_string('resources/comparative_statement.html', {'statements': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-6.05_Comparative_Statement.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

class SupplierEvaluationPlanItemInline(TabularInline):
    model = SupplierEvaluationPlanItem
    extra = 1

@admin.register(SupplierEvaluationPlan)
class SupplierEvaluationPlanAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
    list_display = ('year', 'prepared_by', 'prepared_at', 'approved_by')
    search_fields = ('year',)
    inlines = [SupplierEvaluationPlanItemInline]
    actions = [submit_for_approval, approve_records, 'print_evaluation_plan']
    
    @admin.action(description='Print Supplier Evaluation Plan (QCL-FRM-6.06)')
    def print_evaluation_plan(self, request, queryset):
        html_string = render_to_string('resources/supplier_evaluation_plan.html', {'plans': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-6.06_Supplier_Evaluation_Plan.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    InternalSampleTestRow, PTSampleTestRow, GradingMatrixEquipmentRow, GradingMatrixProductRow, GradingMatrixDocumentRow,
    PersonnelAuthorizationPermit,
    
    
    CompetencyEvalInternalSample,
    CompetencyEvalPTSample,
    GradingMatrixEquipment,
    GradingMatrixProduct,
    GradingMatrixDocument,
    AuthorizedAnalystList,
    TechnicalPersonnelList
,
    CompetencyMonitoring)





@admin.register(PersonnelAuthorizationPermit)
class PersonnelAuthorizationPermitAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'issue_date', 'valid_until', 'approved_by']
    

class InternalSampleTestRowInline(admin.TabularInline):
    model = InternalSampleTestRow
    extra = 1

@admin.register(CompetencyEvalInternalSample)
class CompetencyEvalInternalSampleAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'evaluation_date', 'material_description', 'status']
    inlines = [InternalSampleTestRowInline]

class PTSampleTestRowInline(admin.TabularInline):
    model = PTSampleTestRow
    extra = 1

@admin.register(CompetencyEvalPTSample)
class CompetencyEvalPTSampleAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'evaluation_date', 'pt_round_name', 'status']
    inlines = [PTSampleTestRowInline]

class GradingMatrixEquipmentRowInline(admin.TabularInline):
    model = GradingMatrixEquipmentRow
    extra = 1

@admin.register(GradingMatrixEquipment)
class GradingMatrixEquipmentAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'date', 'status']
    inlines = [GradingMatrixEquipmentRowInline]

class GradingMatrixProductRowInline(admin.TabularInline):
    model = GradingMatrixProductRow
    extra = 1

@admin.register(GradingMatrixProduct)
class GradingMatrixProductAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'product_name', 'date', 'status']
    inlines = [GradingMatrixProductRowInline]

class GradingMatrixDocumentRowInline(admin.TabularInline):
    model = GradingMatrixDocumentRow
    extra = 1

@admin.register(GradingMatrixDocument)
class GradingMatrixDocumentAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'date', 'status']
    inlines = [GradingMatrixDocumentRowInline]

@admin.register(AuthorizedAnalystList)
class AuthorizedAnalystListAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['revision_number', 'date_issued', 'approved_by']

@admin.register(TechnicalPersonnelList)
class TechnicalPersonnelListAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['revision_number', 'date_issued', 'approved_by']
from django.contrib import admin
from unfold.admin import ModelAdmin
from .pdf_utils import generate_iso_pdf
from .approval_utils import action_mark_prepared, action_mark_checked, action_mark_approved
from .models import (
    InternalSampleTestRow, PTSampleTestRow, GradingMatrixEquipmentRow, GradingMatrixProductRow, GradingMatrixDocumentRow,
    TrainingNeedAssessment,
    AnnualTrainingPlan,
    TrainingPlanItem,
    TrainingAttendanceSheet,
    AttendanceRecord,
    TrainingEvaluation,
    TrainingFeedback,
    IndividualTrainingRecord,
    OrientationPlan,
    OrientationPlanTopic,
    CompetenceReassessment,
    TrainerEvaluation
)

@admin.register(TrainingNeedAssessment)
class TrainingNeedAssessmentAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'assessment_year', 'total_percentage', 'approved_by']

class TrainingPlanItemInline(admin.TabularInline):
    model = TrainingPlanItem
    extra = 1

@admin.register(AnnualTrainingPlan)
class AnnualTrainingPlanAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['plan_no', 'month_year', 'prepared_by', 'approved_by']
    inlines = [TrainingPlanItemInline]

class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 1

@admin.register(TrainingAttendanceSheet)
class TrainingAttendanceSheetAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['reference', 'title', 'date_held', 'instructor']
    inlines = [AttendanceRecordInline]

@admin.register(TrainingEvaluation)
class TrainingEvaluationAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'training', 'evaluation_date', 'total_obtained_percentage', 'final_remarks']

@admin.register(TrainingFeedback)
class TrainingFeedbackAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'training', 'overall_rating']
    
    def overall_rating(self, obj):
        return f"{(obj.content_rating + obj.instructor_rating)/2}/5"

@admin.register(IndividualTrainingRecord)
class IndividualTrainingRecordAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'training_title', 'date_completed', 'verified_by']

class OrientationPlanTopicInline(admin.TabularInline):
    model = OrientationPlanTopic
    extra = 1

@admin.register(OrientationPlan)
class OrientationPlanAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'department', 'start_date', 'mentor']
    inlines = [OrientationPlanTopicInline]

@admin.register(CompetenceReassessment)
class CompetenceReassessmentAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'date', 'outcome', 'evaluator']

@admin.register(TrainerEvaluation)
class TrainerEvaluationAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['trainer', 'date', 'overall_effectiveness', 'evaluator']


@admin.register(CompetencyMonitoring)
class CompetencyMonitoringAdmin(ModelAdmin):
    actions = [generate_iso_pdf, action_mark_prepared, action_mark_checked, action_mark_approved]
    list_display = ['analyst', 'main_functions', 'overall_score', 'status']


@admin.register(AuthorizedPersonnelList_2_06)
class AuthorizedPersonnelList206Admin(ModelAdmin):
    list_display = ('revision_number', 'date_issued')

class InductionOrientationItemInline(StackedInline):
    model = InductionOrientationItem
    extra = 1

@admin.register(NewInductionOrientation_2_11)
class NewInductionOrientationAdmin(ModelAdmin):
    list_display = ('candidate_name', 'joining_date', 'probation_period')
    inlines = [InductionOrientationItemInline]

# LSP-03 Admin
class EnvironmentalMonitoringItemInline(StackedInline):
    model = EnvironmentalMonitoringItem
    extra = 1

@admin.register(EnvironmentalMonitoring_3_01)
class EnvironmentalMonitoringAdmin(ModelAdmin):
    list_display = ('month', 'year', 'location', 'status')
    inlines = [EnvironmentalMonitoringItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class HumidityControlItemInline(StackedInline):
    model = HumidityControlItem
    extra = 1

@admin.register(HumidityControlChart_3_02)
class HumidityControlChartAdmin(ModelAdmin):
    list_display = ('month', 'year', 'location', 'status')
    inlines = [HumidityControlItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class TemperatureControlItemInline(StackedInline):
    model = TemperatureControlItem
    extra = 1

@admin.register(TemperatureControlChart_3_03)
class TemperatureControlChartAdmin(ModelAdmin):
    list_display = ('month', 'year', 'location', 'status')
    inlines = [TemperatureControlItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

# LSP-04 Admin
@admin.register(CorrectiveActionRequest_4_01)
class CorrectiveActionRequestAdmin(ModelAdmin):
    list_display = ('car_no', 'department', 'initiated_on', 'initiated_by', 'status')
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class MasterListEquipmentItemInline(StackedInline):
    model = MasterListEquipmentItem
    extra = 1

@admin.register(MasterListEquipment_4_02)
class MasterListEquipmentAdmin(ModelAdmin):
    list_display = ('lab_name', 'status')
    inlines = [MasterListEquipmentItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class MaintenanceRecordItemInline(StackedInline):
    model = MaintenanceRecordItem
    extra = 1

@admin.register(EquipmentMaintenanceRecord_4_03)
class EquipmentMaintenanceRecordAdmin(ModelAdmin):
    list_display = ('for_the_year', 'status')
    inlines = [MaintenanceRecordItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class CalibrationProgramItemInline(StackedInline):
    model = CalibrationProgramItem
    extra = 1

@admin.register(CalibrationProgram_4_04)
class CalibrationProgramAdmin(ModelAdmin):
    list_display = ('year', 'status')
    inlines = [CalibrationProgramItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

# LSP-05 Admin
class CRMListItemInline(StackedInline):
    model = CRMListItem
    extra = 1

@admin.register(CRMList_5_01)
class CRMListAdmin(ModelAdmin):
    list_display = ('month', 'year', 'status')
    inlines = [CRMListItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

# LSP-06 Admin
class SupplierSelectionCriteriaInline(StackedInline):
    model = SupplierSelectionCriteria
    extra = 1

@admin.register(SupplierSelection_6_01)
class SupplierSelectionAdmin(ModelAdmin):
    list_display = ('name_of_supplier', 'form_no', 'selection_date', 'status')
    inlines = [SupplierSelectionCriteriaInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class ApprovedSupplierItemInline(StackedInline):
    model = ApprovedSupplierItem
    extra = 1

@admin.register(ApprovedSupplierServiceProvider_6_02)
class ApprovedSupplierServiceProviderAdmin(ModelAdmin):
    list_display = ('period', 'status')
    inlines = [ApprovedSupplierItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class ExternalProviderEvaluationCriteriaInline(StackedInline):
    model = ExternalProviderEvaluationCriteria
    extra = 1

@admin.register(ExternalProviderEvaluation_6_03)
class ExternalProviderEvaluationAdmin(ModelAdmin):
    list_display = ('supplier_name', 'evaluation_date', 'status')
    inlines = [ExternalProviderEvaluationCriteriaInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class SupplierPerformanceItemInline(StackedInline):
    model = SupplierPerformanceItem
    extra = 1

@admin.register(SupplierPerformanceMonitoring_6_04)
class SupplierPerformanceMonitoringAdmin(ModelAdmin):
    list_display = ('period', 'assessed_by', 'status')
    inlines = [SupplierPerformanceItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class ComparativeStatementItem605Inline(StackedInline):
    model = ComparativeStatementItem_6_05
    extra = 1

@admin.register(ComparativeStatement_6_05)
class ComparativeStatement605Admin(ModelAdmin):
    list_display = ('item_name', 'statement_date', 'status')
    inlines = [ComparativeStatementItem605Inline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class SupplierEvaluationPlanItem606Inline(StackedInline):
    model = SupplierEvaluationPlanItem_6_06
    extra = 1

@admin.register(SupplierEvaluationPlan_6_06)
class SupplierEvaluationPlan606Admin(ModelAdmin):
    list_display = ('for_the_year', 'status')
    inlines = [SupplierEvaluationPlanItem606Inline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class StorePurchaseDemandItemInline(StackedInline):
    model = StorePurchaseDemandItem
    extra = 1

@admin.register(StorePurchaseDemand_6_07)
class StorePurchaseDemandAdmin(ModelAdmin):
    list_display = ('demand_date', 'status')
    inlines = [StorePurchaseDemandItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class ProductsServicesInspectionItemInline(StackedInline):
    model = ProductsServicesInspectionItem
    extra = 1

@admin.register(ProductsServicesInspection_6_08)
class ProductsServicesInspectionAdmin(ModelAdmin):
    list_display = ('external_provider', 'type_of_purchase', 'date_of_receipt', 'status')
    inlines = [ProductsServicesInspectionItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

# LSP-07 Admin
class MasterListDocumentItemInline(StackedInline):
    model = MasterListDocumentItem
    extra = 1

@admin.register(MasterListDocument_7_01)
class MasterListDocumentAdmin(ModelAdmin):
    list_display = ('description', 'status')
    inlines = [MasterListDocumentItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

@admin.register(DocumentChangeRequest_7_02)
class DocumentChangeRequestAdmin(ModelAdmin):
    list_display = ('dcr_no', 'dcr_date', 'document_title', 'status')
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

# ==========================================
# LSP-08 to LSP-11 Admin
# ==========================================

class RiskManagementItemInline(StackedInline):
    model = RiskManagementItem
    extra = 1

@admin.register(RiskManagementSheet_8_01)
class RiskManagementSheetAdmin(ModelAdmin):
    list_display = ('last_updated_on', 'status')
    inlines = [RiskManagementItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class OpportunityAssessmentItemInline(StackedInline):
    model = OpportunityAssessmentItem
    extra = 1

@admin.register(OpportunityAssessment_8_02)
class OpportunityAssessmentAdmin(ModelAdmin):
    list_display = ('review_date', 'status')
    inlines = [OpportunityAssessmentItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

@admin.register(CorrectiveActionRequest_9_01)
class CorrectiveActionRequest901Admin(ModelAdmin):
    list_display = ('car_no', 'department', 'car_initiated_date', 'status')
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class CorrectiveActionsLogItemInline(StackedInline):
    model = CorrectiveActionsLogItem
    extra = 1

@admin.register(CorrectiveActionsRequestLog_9_02)
class CorrectiveActionsRequestLogAdmin(ModelAdmin):
    list_display = ('sheet_no', 'year', 'status')
    inlines = [CorrectiveActionsLogItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

@admin.register(RootCauseAnalysisForm_9_04)
class RootCauseAnalysisFormAdmin(ModelAdmin):
    list_display = ('rca_team_lead', 'rca_start_date', 'status')
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

@admin.register(AuditNotification_10_01)
class AuditNotificationAdmin(ModelAdmin):
    list_display = ('date', 'to_person', 'status')
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class AuditScheduleItemInline(StackedInline):
    model = AuditScheduleItem
    extra = 1

class AuditScheduleDeptItemInline(StackedInline):
    model = AuditScheduleDeptItem
    extra = 1

@admin.register(AuditSchedule_10_02)
class AuditScheduleAdmin(ModelAdmin):
    list_display = ('for_the_year', 'audit_type', 'status')
    inlines = [AuditScheduleItemInline, AuditScheduleDeptItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class MRMScheduleItemInline(StackedInline):
    model = MRMScheduleItem
    extra = 1

@admin.register(MRMSchedule_10_03)
class MRMSchedule1003Admin(ModelAdmin):
    list_display = ('for_the_year', 'status')
    inlines = [MRMScheduleItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class TrainedAuditorItemInline(StackedInline):
    model = TrainedAuditorItem
    extra = 1

@admin.register(TrainedAuditorsList_10_04)
class TrainedAuditorsListAdmin(ModelAdmin):
    list_display = ('date', 'status')
    inlines = [TrainedAuditorItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

@admin.register(AuditorCompetence_10_05)
class AuditorCompetenceAdmin(ModelAdmin):
    list_display = ('auditor_name', 'designation', 'status')
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

@admin.register(ConfidentialAgreementAuditors_10_06)
class ConfidentialAgreementAuditorsAdmin(ModelAdmin):
    list_display = ('mr_name', 'date_of_agreement', 'status')
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

@admin.register(ImpartialityForm_10_07)
class ImpartialityFormAdmin(ModelAdmin):
    list_display = ('mr_name', 'date_of_agreement', 'status')
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

@admin.register(InternalAuditForm_10_08)
class InternalAuditFormAdmin(ModelAdmin):
    list_display = ('department', 'date_of_audit', 'status')
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class InternalAuditCheckListItemInline(StackedInline):
    model = InternalAuditCheckListItem
    extra = 1

@admin.register(InternalAuditCheckList_10_09)
class InternalAuditCheckListAdmin(ModelAdmin):
    list_display = ('auditor_name', 'date_of_audit', 'status')
    inlines = [InternalAuditCheckListItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

@admin.register(AuditReport_10_10)
class AuditReportAdmin(ModelAdmin):
    list_display = ('audit_number', 'date', 'status')
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class MRMScheduleItem1101Inline(StackedInline):
    model = MRMScheduleItem_11_01
    extra = 1

@admin.register(MRMSchedule_11_01)
class MRMSchedule1101Admin(ModelAdmin):
    list_display = ('for_the_year', 'status')
    inlines = [MRMScheduleItem1101Inline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class MRMNoticeParticipantInline(StackedInline):
    model = MRMNoticeParticipant
    extra = 1

@admin.register(MRMNotice_11_02)
class MRMNoticeAdmin(ModelAdmin):
    list_display = ('mrm_no', 'held_on_date', 'status')
    inlines = [MRMNoticeParticipantInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class MRMAgendaItemInline(StackedInline):
    model = MRMAgendaItem
    extra = 1

@admin.register(MRMAgenda_11_03)
class MRMAgendaAdmin(ModelAdmin):
    list_display = ('mrm_no', 'mrm_date', 'status')
    inlines = [MRMAgendaItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']

class MRMFormItemInline(StackedInline):
    model = MRMFormItem
    extra = 1

@admin.register(MRMForm_11_04)
class MRMFormAdmin(ModelAdmin):
    list_display = ('mrm_no', 'held_on', 'status')
    inlines = [MRMFormItemInline]
    actions = [action_mark_prepared, action_mark_checked, action_mark_approved, 'generate_pdf']
