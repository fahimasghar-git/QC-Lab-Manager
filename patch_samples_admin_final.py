import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/admin.py'
with open(path, 'r') as f:
    content = f.read()

# 1. Ensure new fields are in SampleAdmin fieldsets
old_fs = """        ('Analysis Request (12.01)', {
            'fields': ('priority', 'uncertainty_required', 'sample_quantity', 'packing_condition', 'environmental_conditions', 'special_instructions', 'capability_decision', 'rejection_reason')
        }),"""
new_fs = """        ('Assignment & Summary (19.01)', {
            'fields': ('assigned_date', 'due_date', 'container_type')
        }),
        ('Analysis Request (12.01)', {
            'fields': ('priority', 'uncertainty_required', 'sample_quantity', 'packing_condition', 'environmental_conditions', 'special_instructions', 'capability_decision', 'rejection_reason')
        }),"""
content = content.replace(old_fs, new_fs)

# 2. Add print_assignment_form to actions
old_actions = "    actions = ['print_analysis_request', 'print_certificate_of_analysis']"
new_actions = "    actions = ['print_analysis_request', 'print_certificate_of_analysis', 'print_assignment_form']"
content = content.replace(old_actions, new_actions)

action_method = """
    @admin.action(description='Print Assignment, Summary and Review Form (19.01)')
    def print_assignment_form(self, request, queryset):
        html_string = render_to_string('samples/assignment_form.html', {'samples': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-19.01_Assignment_Form.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response
"""
content = content.replace("    def print_analysis_request(", action_method + "\n    def print_analysis_request(")


# 3. Add SampleReturnAdmin
sample_return_admin = """
from .models import SampleReturn

@admin.register(SampleReturn)
class SampleReturnAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('sample', 'return_date', 'reason')
    actions = ['print_sample_return_form']
    
    @admin.action(description='Print Sample Return Form (22.01)')
    def print_sample_return_form(self, request, queryset):
        html_string = render_to_string('samples/sample_return_form.html', {'returns': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-22.01_Sample_Return.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response
"""
content = content + "\n" + sample_return_admin

with open(path, 'w') as f:
    f.write(content)
print("Updated samples/admin.py")
