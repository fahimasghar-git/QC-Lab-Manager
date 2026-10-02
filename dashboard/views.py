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
    testing_queue = TestResult.objects.filter(assigned_to=request.user, status__in=['PENDING', 'ASSIGNED', 'IN_PROGRESS']) if not request.user.is_superuser else TestResult.objects.filter(status__in=['PENDING', 'ASSIGNED', 'IN_PROGRESS'])
    verification_queue = TestResult.objects.filter(status='PENDING_VERIFICATION')
    
    # QCM queue: Find samples where all tests are verified, but the sample itself isn't approved yet.
    # To avoid complex SQL, we'll fetch unapproved samples and check the property.
    unapproved_samples = Sample.objects.exclude(status='APPROVED')
    approval_queue = [s for s in unapproved_samples if s.is_ready_for_approval]
    
    is_analyst = request.user.groups.filter(name='Analyst').exists() or getattr(request.user, 'role', '') == 'ANALYST'
    is_reviewer = request.user.groups.filter(name='Reviewer').exists() or getattr(request.user, 'role', '') == 'AQCM'
    is_approver = request.user.groups.filter(name='Approver').exists() or getattr(request.user, 'role', '') == 'QCM'
    is_admin = request.user.is_superuser or request.user.groups.filter(name='Admin').exists() or getattr(request.user, 'role', '') == 'ADMIN'

    context = {
        'total_samples': total_samples,
        'pending_samples': pending_samples,
        'completed_samples': completed_samples,
        'pending_tests': pending_tests,
        'out_of_service_eq': out_of_service_eq,
        'open_ncs': open_ncs,
        'docs_review_due': docs_review_due,
        'recent_samples': recent_samples,
        
        # New context vars
        'testing_queue': testing_queue,
        'verification_queue': verification_queue,
        'approval_queue': approval_queue,
        'is_analyst': is_analyst,
        'is_reviewer': is_reviewer,
        'is_approver': is_approver,
        'is_admin': is_admin,
    }
    return render(request, 'dashboard/home.html', context)
