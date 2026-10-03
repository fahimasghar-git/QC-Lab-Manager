from lims_core.admin_mixins import DigitalSignatureMixin
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.admin import TabularInline, StackedInline
from simple_history.admin import SimpleHistoryAdmin
from django.shortcuts import render
from .models import Client, Sample
from testing.models import TestResult
from django.utils import timezone

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone')
    search_fields = ('name', 'contact_person', 'email')

class TestResultInline(TabularInline):
    model = TestResult
    extra = 1
    # Removed readonly_fields so you can actually type into them!
    fields = ('result_type', 'parameter', 'method', 'result_value', 'unit', 'measurement_uncertainty', 'equipment_used', 'reagents_used', 'status')
    
    # We exclude traceability fields here because the system will auto-fill them in the background
    exclude = ('analyst', 'reviewed_by', 'reviewed_at', 'remarks')
    can_delete = True

from django.contrib import messages

@admin.action(description='🖨️ Print Analysis Request / Sample Receipt')
def print_analysis_request(modeladmin, request, queryset):
    return render(request, 'samples/analysis_request.html', {'samples': queryset})

@admin.action(description='▶️ Submit for AQCM Verification')
def submit_for_verification(modeladmin, request, queryset):
    updated = queryset.filter(status__in=['RECEIVED', 'IN_PROGRESS']).update(status='PENDING_VERIFICATION')
    modeladmin.message_user(request, f"{updated} sample(s) submitted to AQCM for verification.", messages.SUCCESS)

@admin.action(description='✔️ Verify & Submit for QCM Approval')
def verify_and_submit(modeladmin, request, queryset):
    # Only transition samples that are pending verification
    samples = queryset.filter(status='PENDING_VERIFICATION')
    for sample in samples:
        sample.status = 'PENDING_APPROVAL'
        sample.verified_by = request.user
        sample.verified_at = timezone.now()
        sample.save()
    modeladmin.message_user(request, f"{len(samples)} sample(s) verified and sent to QCM.", messages.SUCCESS)

@admin.action(description='✅ Approve Results (QCM)')
def approve_results(modeladmin, request, queryset):
    samples = queryset.filter(status='PENDING_APPROVAL')
    for sample in samples:
        sample.status = 'APPROVED'
        sample.approved_by = request.user
        sample.approved_at = timezone.now()
        
        # Also approve the individual test results
        for test in sample.test_results.all():
            if test.status != 'APPROVED':
                test.status = 'APPROVED'
                test.reviewed_by = request.user
                test.reviewed_at = timezone.now()
                test.save()
        
        sample.save()
    modeladmin.message_user(request, f"{len(samples)} sample(s) officially APPROVED.", messages.SUCCESS)

@admin.action(description='📜 Generate Certificate of Analysis (CoA)')
def generate_coa(modeladmin, request, queryset):
    from django.template.loader import get_template
    from django.http import HttpResponse
    from xhtml2pdf import pisa
    from io import BytesIO
    from django.core.files.base import ContentFile
    from management.models import RecordArchive
    from datetime import timedelta
    
    approved_samples = queryset.filter(status='APPROVED')
    if not approved_samples.exists():
        modeladmin.message_user(request, "Only APPROVED samples can generate a CoA.", messages.ERROR)
        return
        
    template = get_template('samples/certificate_of_analysis.html')
    html = template.render({'samples': approved_samples})
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        pdf_content = result.getvalue()
        
        # Save to ISO 17025 Record Archive for each sample
        for sample in approved_samples:
            # Check if this CoA was already archived recently, or just archive it
            archive = RecordArchive(
                record_id=f"CoA-{sample.sample_id}",
                record_type="Certificate of Analysis",
                archived_by=request.user,
                retention_date=timezone.now().date() + timedelta(days=5*365) # 5 years retention
            )
            
            archive.file.save(f"CoA_{sample.sample_id}_{timezone.now().strftime('%Y%m%d%H%M')}.pdf", ContentFile(pdf_content))
            archive.save()
            
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="CoA_Batch.pdf"'
        return response
    else:
        modeladmin.message_user(request, "Error generating PDF CoA.", messages.ERROR)
        return

@admin.register(Sample)
class SampleAdmin(ModelAdmin, SimpleHistoryAdmin):

    class Media:
        js = ('js/sample_category_toggle.js',)

    list_display = ('sample_id', 'serial_number', 'category', 'product_name', 'client', 'status', 'received_date')
    list_filter = ('status', 'received_date', 'product_name')
    search_fields = ('category', 'sample_id', 'product_name', 'batch_number', 'client__name')
    readonly_fields = ('sample_id', 'serial_number', 'received_date', 'verified_by', 'verified_at', 'approved_by', 'approved_at')
    inlines = [TestResultInline]
    actions = [print_analysis_request, submit_for_verification, verify_and_submit, approve_results, generate_coa]
    
    fieldsets = (
        ('Sample Identification & AR Details', {
            'fields': ('category', 'sample_id', 'serial_number', 'client', 'product_name', 'batch_number', 'sample_quantity', 'assay')
        }),
        ('Condition & Storage', {
            'fields': ('description', 'storage_condition', 'status', 'rejection_reason')
        }),
        ('Chain of Custody & Signatures', {
            'fields': ('customer_signature', 'received_by', 'received_date', 'notes')
        }),
        ('ISO 17025 Authorization', {
            'fields': ('verified_by', 'verified_at', 'approved_by', 'approved_at')
        }),
    )

    # Automatically set the 'received_by' field to the logged-in user when creating a new sample
    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.received_by = request.user
        super().save_model(request, obj, form, change)

    # ISO 17025 Traceability: Auto-assign analyst to inline TestResults ONLY when results are entered
    def save_formset(self, request, form, formset, change):
        from resources.models import CompetencyRecord
        
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, TestResult):
                # If a result is typed in, but no analyst is set, assign the current user as the analyst
                if instance.result_value is not None:
                    if not getattr(instance, 'analyst_id', None) or instance.analyst is None:
                        instance.analyst = request.user
                        instance.tested_at = timezone.now()
                        if instance.status == 'PENDING':
                            instance.status = 'DRAFT'
                            
                    # ISO 17025 Check: Is the analyst authorized for this method?
                    if instance.method:
                        is_competent = CompetencyRecord.objects.filter(
                            analyst=instance.analyst,
                            test_method=instance.method,
                            status='AUTHORIZED'
                        ).exists()
                        
                        if not is_competent:
                            messages.warning(request, f"⚠️ ISO 17025 WARNING: Analyst {instance.analyst.username} is NOT officially authorized to perform method '{instance.method.name}'.")
                
                # If status changed to APPROVED in the inline, stamp the reviewer
                if instance.status == 'APPROVED' and instance.reviewed_by is None:
                    instance.reviewed_by = request.user
                    instance.reviewed_at = timezone.now()
            instance.save()
        formset.save_m2m()
        
        # ISO 17025 Metrological Traceability Check
        for instance in instances:
            if isinstance(instance, TestResult) and instance.result_value is not None:
                # Check for expired reagents
                expired_reagents = instance.reagents_used.filter(status='EXPIRED')
                for reagent in expired_reagents:
                    messages.error(request, f"🛑 ISO 17025 VIOLATION: Analyst used an EXPIRED reagent ({reagent.name} - Lot {reagent.lot_number}) for {instance.parameter.name}.")
                
                # Check for out of service equipment
                bad_equipment = instance.equipment_used.exclude(status='ACTIVE')
                for eq in bad_equipment:
                    messages.error(request, f"🛑 ISO 17025 VIOLATION: Equipment '{eq.name}' is currently {eq.get_status_display()} but was used for {instance.parameter.name}.")


from .models import SampleReturn

@admin.register(SampleReturn)
class SampleReturnAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):
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


from .models import PendingApproval, PendingVerification

@admin.register(PendingApproval)
class PendingApprovalAdmin(SampleAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='PENDING_APPROVAL')

@admin.register(PendingVerification)
class PendingVerificationAdmin(SampleAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='PENDING_VERIFICATION')

