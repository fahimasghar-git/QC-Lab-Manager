import os

file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/dashboard/views.py'
with open(file_path, 'r') as f:
    content = f.read()

# Replace action queues block
old_queues = """    # --- NEW: Action Queues (Eliminate Human Wait Factor) ---
    testing_queue = Sample.objects.filter(status__in=['RECEIVED', 'IN_PROGRESS'])
    verification_queue = Sample.objects.filter(status='PENDING_VERIFICATION')
    approval_queue = Sample.objects.filter(status='PENDING_APPROVAL')"""

new_queues = """    # --- NEW: Parameter-Level Routing (Eliminate Human Wait Factor) ---
    testing_queue = TestResult.objects.filter(assigned_to=request.user, status__in=['PENDING', 'ASSIGNED', 'IN_PROGRESS']) if not request.user.is_superuser else TestResult.objects.filter(status__in=['PENDING', 'ASSIGNED', 'IN_PROGRESS'])
    verification_queue = TestResult.objects.filter(status='PENDING_VERIFICATION')
    
    # QCM queue: Find samples where all tests are verified, but the sample itself isn't approved yet.
    # To avoid complex SQL, we'll fetch unapproved samples and check the property.
    unapproved_samples = Sample.objects.exclude(status='APPROVED')
    approval_queue = [s for s in unapproved_samples if s.is_ready_for_approval]"""

content = content.replace(old_queues, new_queues)

# We need to change approval_queue.count in the template to len(approval_queue) or approval_queue|length
with open(file_path, 'w') as f:
    f.write(content)

# Update home.html template
tpl_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/dashboard/templates/dashboard/home.html'
with open(tpl_path, 'r') as f:
    tpl = f.read()

tpl = tpl.replace('{{ testing_queue.count }} sample(s) waiting to be tested.', '{{ testing_queue.count }} parameter test(s) assigned to you.')
tpl = tpl.replace('<a href="/admin/samples/sample/" class="alert-link">View testing queue</a>', '<a href="/admin/testing/testresult/?status__in=ASSIGNED,IN_PROGRESS" class="alert-link">View assigned parameters</a>')

tpl = tpl.replace('{{ verification_queue.count }} sample(s) waiting for data verification (AQCM).', '{{ verification_queue.count }} parameter test(s) waiting for data verification (AQCM).')
tpl = tpl.replace('<a href="/admin/samples/sample/?status__exact=PENDING_VERIFICATION" class="alert-link">Review them now</a>', '<a href="/admin/testing/testresult/?status__exact=PENDING_VERIFICATION" class="alert-link">Review them now</a>')

tpl = tpl.replace('{{ approval_queue.count }} verified sample(s)', '{{ approval_queue|length }} fully-verified sample(s)')

with open(tpl_path, 'w') as f:
    f.write(tpl)
