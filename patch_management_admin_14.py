import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/admin.py'
with open(path, 'r') as f:
    content = f.read()

# 1. Update fieldsets
old_fs = """        ('Root Cause Analysis & CAPA', {
            'fields': ('root_cause_analysis', 'corrective_action', 'preventive_action')
        }),"""
new_fs = """        ('Root Cause Analysis & CAPA', {
            'fields': (
                'root_cause_analysis', 'rca_man', 'rca_method', 'rca_machine', 'rca_material',
                'similar_non_conformance', 'rca_carried_out_by',
                'corrective_action', 'preventive_action'
            )
        }),"""
content = content.replace(old_fs, new_fs)

# 2. Add actions to NonConformanceAdmin
old_actions = "    actions = ['print_non_conformance']"
new_actions = "    actions = ['print_non_conformance', 'print_non_conformance_log', 'print_root_cause_analysis']"
content = content.replace(old_actions, new_actions)

# 3. Add the action methods
action_methods = """
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
"""

# inject right before `def print_non_conformance`
content = content.replace("    def print_non_conformance(", action_methods + "\n    def print_non_conformance(")

with open(path, 'w') as f:
    f.write(content)

print("Updated NonConformanceAdmin with 14.02 and 14.03 actions.")
