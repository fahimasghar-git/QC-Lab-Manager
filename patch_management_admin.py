import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/admin.py'
with open(path, 'r') as f:
    content = f.read()

# Make sure imports exist for PDF generation
imports = "from django.template.loader import render_to_string\nfrom django.http import HttpResponse\nfrom xhtml2pdf import pisa\n"
if "from xhtml2pdf import pisa" not in content:
    content = imports + content

old_action = """    def print_non_conformance(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'management/non_conformance_form.html', {'ncs': queryset})"""

new_action = """    def print_non_conformance(self, request, queryset):
        html_string = render_to_string('management/non_conformance_form.html', {'ncs': queryset, 'request': request})
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-14.01_Non_Conformance.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response"""

content = content.replace(old_action, new_action)

with open(path, 'w') as f:
    f.write(content)
print("Updated 14.01 admin action to use xhtml2pdf.")
