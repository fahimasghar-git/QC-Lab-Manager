from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from samples.models import Sample
from testing.models import TestResult
from resources.models import Equipment
from management.models import NonConformance, Document
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
        # Unified Approval Queue
        from management.models import Document, NonConformance, InternalAudit, RecordArchive
        from resources.models import CompetencyRecord, Supplier, PurchaseRequest
        
        for s in Sample.objects.filter(status='PENDING_APPROVAL'):
            approval_queue.append({'type': 'Sample', 'id': s.sample_id, 'status': 'Pending QCM', 'url': f"/admin/samples/sample/{s.id}/change/"})
        for d in Document.objects.filter(status='PENDING_APPROVAL'):
            approval_queue.append({'type': 'Document SOP', 'id': d.document_id, 'status': 'Pending QCM', 'url': f"/admin/management/document/{d.id}/change/"})
        for nc in NonConformance.objects.filter(status='PENDING_APPROVAL'):
            approval_queue.append({'type': 'Non-Conformance', 'id': nc.nc_id, 'status': 'Pending QCM', 'url': f"/admin/management/nonconformance/{nc.id}/change/"})
        for a in InternalAudit.objects.filter(status='PENDING_APPROVAL'):
            approval_queue.append({'type': 'Audit', 'id': a.audit_id, 'status': 'Pending QCM', 'url': f"/admin/management/internalaudit/{a.id}/change/"})
        for c in CompetencyRecord.objects.filter(status='PENDING_APPROVAL'):
            approval_queue.append({'type': 'Competency', 'id': f"{c.personnel.username} - {c.test_parameter.name}", 'status': 'Pending QCM', 'url': f"/admin/resources/competencyrecord/{c.id}/change/"})
        for sup in Supplier.objects.filter(status='PENDING_APPROVAL'):
            approval_queue.append({'type': 'Supplier', 'id': sup.name, 'status': 'Pending QCM', 'url': f"/admin/resources/supplier/{sup.id}/change/"})
        for pr in PurchaseRequest.objects.filter(status='PENDING_APPROVAL'):
            approval_queue.append({'type': 'Purchase Request', 'id': pr.pr_number, 'status': 'Pending QCM', 'url': f"/admin/resources/purchaserequest/{pr.id}/change/"})
        for ra in RecordArchive.objects.filter(status='PENDING_APPROVAL'):
            approval_queue.append({'type': 'Record Archive', 'id': ra.record_id, 'status': 'Pending QCM', 'url': f"/admin/management/recordarchive/{ra.id}/change/"})

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
