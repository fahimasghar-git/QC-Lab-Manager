import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(path, 'r') as f:
    content = f.read()

# Replace SupplierAdmin fieldsets
old_fs = """    fieldsets = (
        ('Supplier Basic Info', {
            'fields': ('name', 'contact_person', 'email', 'phone')
        }),
        ('Evaluation Details', {"""

new_fs = """    fieldsets = (
        ('Supplier Basic Info', {
            'fields': ('name', 'contact_person', 'email', 'phone', 'website', 'requirements_from_supplier')
        }),
        ('QCL-FRM-6.01 Selection Criteria', {
            'fields': (
                ('crit_1_registered', 'crit_1_evidence'),
                ('crit_2_market_1yr', 'crit_2_evidence'),
                ('crit_3_offers_range', 'crit_3_evidence'),
                ('crit_4_equipment_docs', 'crit_4_evidence'),
                ('crit_5_calibration_traceability', 'crit_5_evidence'),
                ('crit_6_iso17025', 'crit_6_evidence'),
                ('crit_7_iso17043', 'crit_7_evidence'),
                ('crit_8_training_exp', 'crit_8_evidence'),
                ('crit_9_msds', 'crit_9_evidence'),
                ('crit_10_crm_coa', 'crit_10_evidence'),
                'selection_evaluator'
            ),
            'classes': ('collapse',)
        }),
        ('Evaluation Details', {"""
content = content.replace(old_fs, new_fs)

# Add admin actions for 6.01 and 6.02
old_actions = """    actions = ['print_supplier_evaluation']"""
new_actions = """    actions = ['print_supplier_selection', 'print_approved_supplier_list', 'print_supplier_evaluation']"""
content = content.replace(old_actions, new_actions)

action_methods = """
    @admin.action(description='Print Supplier Selection Form (QCL-FRM-6.01)')
    def print_supplier_selection(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one Supplier for 6.01.", level='ERROR')
            return
        
        supplier = queryset.first()
        html_string = render_to_string('resources/supplier_selection.html', {'supplier': supplier, 'request': request})
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="QCL-FRM-6.01_{supplier.name}.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

    @admin.action(description='Print Approved Supplier List (QCL-FRM-6.02)')
    def print_approved_supplier_list(self, request, queryset):
        # Ignored queryset, we just print all approved suppliers
        suppliers = Supplier.objects.filter(is_approved=True)
        html_string = render_to_string('resources/approved_supplier_list.html', {'suppliers': suppliers, 'request': request})
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-6.02_Approved_Suppliers.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response
"""

# Insert methods before "def print_supplier_evaluation"
content = content.replace("    @admin.action(description='Print Supplier Evaluation (QCL-FRM-6.03)')", action_methods + "\n    @admin.action(description='Print Supplier Evaluation (QCL-FRM-6.03)')")

with open(path, 'w') as f:
    f.write(content)
print("Supplier Admin patched.")
