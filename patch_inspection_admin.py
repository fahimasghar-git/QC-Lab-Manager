path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(path, 'r') as f:
    content = f.read()

import_line = "from .models import Equipment, EquipmentMaintenance, TestMethod, Chemical, CRM, TrainingRecord, Supplier, PurchaseRequest"
new_import_line = "from .models import Equipment, EquipmentMaintenance, TestMethod, Chemical, CRM, TrainingRecord, Supplier, PurchaseRequest, ProductServiceInspection"
content = content.replace(import_line, new_import_line)

admin_code = """
@admin.register(ProductServiceInspection)
class ProductServiceInspectionAdmin(ModelAdmin, SimpleHistoryAdmin):
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
    
    actions = ['print_inspection_form']
    
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
"""

content = content + "\n" + admin_code
with open(path, 'w') as f:
    f.write(content)
print("Added ProductServiceInspectionAdmin.")
