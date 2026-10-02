import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/admin.py'
with open(path, 'r') as f:
    content = f.read()

# Make sure imports are updated
old_imports = "from .models import Document, NonConformance, RecordArchive, InternalAudit, AuditFinding, Risk, ManagementReview"
new_imports = old_imports + ", LabCleaningInspection, LabCleaningDailyRecord, MasterListRecord, MasterListFileFolder, CustomerFeedback"
content = content.replace(old_imports, new_imports)

# Append new admins
new_admins = """

class LabCleaningDailyRecordInline(TabularInline):
    model = LabCleaningDailyRecord
    extra = 7

@admin.register(LabCleaningInspection)
class LabCleaningInspectionAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('section_area', 'month_year')
    inlines = [LabCleaningDailyRecordInline]
    actions = ['print_cleaning_inspection']
    
    @admin.action(description='Print Lab Cleaning Inspection Sheet (17.14)')
    def print_cleaning_inspection(self, request, queryset):
        html_string = render_to_string('management/lab_cleaning_inspection.html', {'inspections': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-17.14_Cleaning_Inspection.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

@admin.register(MasterListRecord)
class MasterListRecordAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('title', 'code', 'revision_no', 'location', 'retention_period')
    actions = ['print_master_list_records']
    
    @admin.action(description='Print Master List of Records (20.01)')
    def print_master_list_records(self, request, queryset):
        html_string = render_to_string('management/master_list_records.html', {'records': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-20.01_Master_List_Records.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

@admin.register(MasterListFileFolder)
class MasterListFileFolderAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('title', 'file_code', 'volume', 'keeper', 'status')
    actions = ['print_master_list_files']
    
    @admin.action(description='Print Master List of Files and Folders (20.02)')
    def print_master_list_files(self, request, queryset):
        html_string = render_to_string('management/master_list_files.html', {'files': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-20.02_Master_List_Files.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('customer_name', 'date', 'percentage')
    actions = ['print_customer_feedback']
    
    @admin.action(description='Print Customer Feedback Form (21.01)')
    def print_customer_feedback(self, request, queryset):
        html_string = render_to_string('management/customer_feedback.html', {'feedbacks': queryset, 'request': request})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="QCL-FRM-21.01_Customer_Feedback.pdf"'
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response
"""

content = content + "\n" + new_admins

with open(path, 'w') as f:
    f.write(content)
print("Updated management/admin.py")
