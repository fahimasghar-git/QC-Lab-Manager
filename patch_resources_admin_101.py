import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(path, 'r') as f:
    content = f.read()

import_line = "from .models import Equipment, CalibrationRecord, EquipmentMaintenance, CompetencyRecord, CompetencyEvaluation, ReagentStandard, Supplier, PurchaseRequest, ProductServiceInspection"
new_import_line = "from .models import Equipment, CalibrationRecord, EquipmentMaintenance, CompetencyRecord, CompetencyEvaluation, ReagentStandard, Supplier, PurchaseRequest, ProductServiceInspection, PersonnelAuthorization"

content = content.replace(import_line, new_import_line)

admin_class = """
@admin.register(PersonnelAuthorization)
class PersonnelAuthorizationAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('user', 'employee_code', 'designation', 'authorization_date')
    search_fields = ('user__username', 'user__first_name', 'employee_code', 'designation')
    
    actions = ['print_authorization_permit', 'print_list_of_authorized_staff']
    
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
            'fields': ('prepared_by', 'authorized_by')
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
"""

content = content + "\n\n" + admin_class

with open(path, 'w') as f:
    f.write(content)
print("Added PersonnelAuthorizationAdmin.")
