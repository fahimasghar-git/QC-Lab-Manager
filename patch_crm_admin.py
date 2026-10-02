import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(path, 'r') as f:
    content = f.read()

# Update fieldsets in ReagentStandardAdmin
old_fs = """    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'lot_number', 'supplier')
        }),
        ('Status & Validity', {
            'fields': ('expiry_date', 'status', 'certificate_reference')
        }),
    )"""

new_fs = """    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'is_crm', 'lot_number', 'supplier', 'catalog_no', 'traceability', 'quantity')
        }),
        ('Status & Validity', {
            'fields': ('expiry_date', 'status', 'certificate_reference')
        }),
    )"""

content = content.replace(old_fs, new_fs)

# Add admin action to print CRM list
if "'print_crm_list'" not in content:
    content = content.replace("list_display = ('name', 'lot_number', 'supplier', 'receipt_date', 'expiry_date', 'status')", "list_display = ('name', 'is_crm', 'lot_number', 'supplier', 'receipt_date', 'expiry_date', 'status')\n    actions = ['print_crm_list']")
    
    action_code = """
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
"""
    # Find ReagentStandardAdmin class definition end and append the method
    # It ends right before "@admin.register(Supplier)"
    content = content.replace("@admin.register(Supplier)", action_code + "\n@admin.register(Supplier)")

with open(path, 'w') as f:
    f.write(content)
print("Updated ReagentStandardAdmin for CRM list.")
