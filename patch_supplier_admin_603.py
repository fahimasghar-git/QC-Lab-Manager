import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(path, 'r') as f:
    content = f.read()

old_action = """    @admin.action(description='Print Supplier Evaluation (QCL-FRM-6.03)')
    def print_supplier_evaluation(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/supplier_evaluation.html', {'suppliers': queryset})"""

new_action = """    @admin.action(description='Print Supplier Evaluation (QCL-FRM-6.03)')
    def print_supplier_evaluation(self, request, queryset):
        html_string = render_to_string('resources/supplier_evaluation.html', {'suppliers': queryset, 'request': request})
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-6.03_Supplier_Evaluation.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response"""

content = content.replace(old_action, new_action)

with open(path, 'w') as f:
    f.write(content)
print("Updated 6.03 admin action to use xhtml2pdf.")
