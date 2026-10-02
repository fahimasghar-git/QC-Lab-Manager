import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(path, 'r') as f:
    content = f.read()

# Add admin actions for 6.04
old_actions = """    actions = ['print_supplier_selection', 'print_approved_supplier_list', 'print_supplier_evaluation']"""
new_actions = """    actions = ['print_supplier_selection', 'print_approved_supplier_list', 'print_supplier_evaluation', 'print_supplier_monitoring']"""
content = content.replace(old_actions, new_actions)

action_methods = """
    @admin.action(description='Print Supplier Performance Monitoring (QCL-FRM-6.04)')
    def print_supplier_monitoring(self, request, queryset):
        html_string = render_to_string('resources/supplier_performance_monitoring.html', {'suppliers': queryset, 'request': request})
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-6.04_Supplier_Monitoring.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response
"""

# Insert methods before "def print_supplier_evaluation"
content = content.replace("    @admin.action(description='Print Supplier Evaluation (QCL-FRM-6.03)')", action_methods + "\n    @admin.action(description='Print Supplier Evaluation (QCL-FRM-6.03)')")

with open(path, 'w') as f:
    f.write(content)
print("Supplier Admin patched with 6.04.")
