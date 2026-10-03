from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from samples.models import Sample
from testing.models import TestResult
from resources.models import Equipment, CompetencyRecord, Supplier, PurchaseRequest
from management.models import NonConformance, Document, InternalAudit, RecordArchive
from django.utils import timezone

@login_required
def home(request):
    # Gather statistics for the dashboard
    total_samples = Sample.objects.count()
    pending_samples = Sample.objects.filter(status__in=['RECEIVED', 'IN_PROGRESS', 'PENDING_VERIFICATION', 'PENDING_APPROVAL']).count()
    completed_samples = Sample.objects.filter(status='APPROVED').count()
    
    pending_tests = TestResult.objects.filter(status__in=['PENDING', 'DRAFT']).count()
    
    out_of_service_eq = Equipment.objects.filter(status='OUT_OF_SERVICE').count()
    
    # Clause 8 metrics
    open_ncs = NonConformance.objects.exclude(status='CLOSED').count()
    docs_review_due = Document.objects.filter(status='ACTIVE', next_review_date__lte=timezone.now().date()).count()
    
    # Recent samples
    recent_samples = Sample.objects.order_by('-received_date')[:5]

    # --- NEW: Parameter-Level Routing (Eliminate Human Wait Factor) ---
    
    # Enforce strict group checks based on our new ISO groups
    is_analyst = request.user.groups.filter(name='Analyst').exists()
    is_aqcm = request.user.groups.filter(name='AQCM').exists()
    is_qcm = request.user.groups.filter(name='QCM').exists()
    is_ceo = request.user.groups.filter(name='CEO').exists()
    is_admin = request.user.is_superuser or request.user.groups.filter(name='IT Admin').exists()

    # Higher ranks can see lower rank queues:
    can_see_analyst_queue = is_analyst or is_aqcm or is_qcm or is_admin
    can_see_aqcm_queue = is_aqcm or is_qcm or is_admin
    can_see_qcm_queue = is_qcm or is_ceo or is_admin

    testing_queue = []
    if can_see_analyst_queue:
        q = TestResult.objects.filter(assigned_to=request.user, status__in=['PENDING', 'ASSIGNED', 'IN_PROGRESS']) if is_analyst and not (is_aqcm or is_qcm or is_admin) else TestResult.objects.filter(status__in=['PENDING', 'ASSIGNED', 'IN_PROGRESS'])
        for t in q:
            testing_queue.append({
                'type': 'Testing',
                'id': f"Test: {t.parameter.name} on {t.sample.sample_id}",
                'status': t.get_status_display(),
                'url': f"/admin/testing/testresult/{t.id}/change/"
            })

    verification_queue = []
    if can_see_aqcm_queue:
        for s in Sample.objects.filter(status='PENDING_VERIFICATION'):
            verification_queue.append({'type': 'Sample Verification', 'id': s.sample_id, 'status': 'Pending AQCM', 'url': f"/admin/samples/sample/{s.id}/change/"})
        # If any other model needs AQCM review in future, add here.


    approval_queue = []
    if can_see_qcm_queue:
        # Unified Approval Queue - Safely constructed
        from django.core.exceptions import FieldError

        def add_to_queue(queryset, item_type, id_attr_func, url_pattern):
            try:
                for obj in queryset:
                    try:
                        identifier = id_attr_func(obj)
                    except AttributeError:
                        identifier = f"{item_type} #{obj.pk}"
                    
                    approval_queue.append({
                        'type': item_type,
                        'id': identifier,
                        'status': 'Pending QCM',
                        'url': url_pattern.format(obj.id)
                    })
            except Exception:
                pass # Catch all so the dashboard NEVER crashes due to a bad model query

        # Samples
        try:
            add_to_queue(Sample.objects.filter(status='PENDING_APPROVAL'), 'Sample', lambda s: s.sample_id, "/admin/samples/sample/{}/change/")
        except: pass

        # Documents
        try:
            add_to_queue(Document.objects.filter(status='DRAFT'), 'Document SOP', lambda d: getattr(d, 'document_id', f"Doc #{d.id}"), "/admin/management/document/{}/change/")
        except: pass

        # Non-Conformances
        try:
            add_to_queue(NonConformance.objects.filter(status='OPEN'), 'Non-Conformance', lambda nc: getattr(nc, 'nc_id', f"NC #{nc.id}"), "/admin/management/nonconformance/{}/change/")
        except: pass

        # Audits
        try:
            add_to_queue(InternalAudit.objects.filter(status='SCHEDULED'), 'Audit', lambda a: getattr(a, 'audit_id', f"Audit #{a.id}"), "/admin/management/internalaudit/{}/change/")
        except: pass

        # Competency
        try:
            # Safely handle CompetencyRecord fields which are analyst and test_method
            add_to_queue(
                CompetencyRecord.objects.filter(status='IN_TRAINING'), 
                'Competency', 
                lambda c: f"{getattr(c.analyst, 'username', 'User')} - {getattr(c.test_method, 'name', 'Method')}", 
                "/admin/resources/competencyrecord/{}/change/"
            )
        except: pass

        # Supplier
        try:
            # Supplier might not have status field at all
            if hasattr(Supplier, 'status'):
                add_to_queue(Supplier.objects.filter(status='PENDING_APPROVAL'), 'Supplier', lambda s: s.name, "/admin/resources/supplier/{}/change/")
        except: pass

        # Purchase Request
        try:
            add_to_queue(PurchaseRequest.objects.filter(status='REQUESTED'), 'Purchase Request', lambda p: getattr(p, 'item_description', f"PR #{p.id}"), "/admin/resources/purchaserequest/{}/change/")
        except: pass

        # Record Archive
        try:
            add_to_queue(RecordArchive.objects.filter(status='PENDING_APPROVAL'), 'Record Archive', lambda r: getattr(r, 'record_id', f"Record #{r.id}"), "/admin/management/recordarchive/{}/change/")
        except: pass

    context = {

        'total_samples': total_samples,
        'pending_samples': pending_samples,
        'completed_samples': completed_samples,
        'pending_tests': pending_tests,
        'out_of_service_eq': out_of_service_eq,
        'open_ncs': open_ncs,
        'docs_review_due': docs_review_due,
        'recent_samples': recent_samples,
        
        # Unified Queues
        'testing_queue': testing_queue,
        'verification_queue': verification_queue,
        'approval_queue': approval_queue,
        
        # Permissions
        'can_see_analyst_queue': can_see_analyst_queue,
        'can_see_aqcm_queue': can_see_aqcm_queue,
        'can_see_qcm_queue': can_see_qcm_queue,
    }
    return render(request, 'dashboard/home.html', context)
