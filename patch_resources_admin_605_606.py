import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(path, 'r') as f:
    content = f.read()

import_str = "from .models import Equipment, CalibrationRecord, EquipmentMaintenance, CompetencyRecord, CompetencyEvaluation, ReagentStandard, Supplier, PurchaseRequest, ProductServiceInspection, PersonnelAuthorization"
new_import_str = import_str + ", ComparativeStatement, ComparativeStatementSupplier, SupplierEvaluationPlan, SupplierEvaluationPlanItem"
content = content.replace(import_str, new_import_str)

admin_classes = """

class ComparativeStatementSupplierInline(TabularInline):
    model = ComparativeStatementSupplier
    extra = 3

@admin.register(ComparativeStatement)
class ComparativeStatementAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('item_name', 'date', 'purchase_demand', 'prepared_by')
    search_fields = ('item_name',)
    inlines = [ComparativeStatementSupplierInline]
    actions = ['print_comparative_statement']
    
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
class SupplierEvaluationPlanAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('year', 'prepared_by', 'prepared_date', 'approved_by')
    search_fields = ('year',)
    inlines = [SupplierEvaluationPlanItemInline]
    actions = ['print_evaluation_plan']
    
    @admin.action(description='Print Supplier Evaluation Plan (QCL-FRM-6.06)')
    def print_evaluation_plan(self, request, queryset):
        html_string = render_to_string('resources/supplier_evaluation_plan.html', {'plans': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-6.06_Supplier_Evaluation_Plan.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response
"""

content = content + "\n\n" + admin_classes

with open(path, 'w') as f:
    f.write(content)
print("Added 6.05 and 6.06 admins.")
