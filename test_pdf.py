import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lims_core.settings")
django.setup()

from django.template.loader import render_to_string
from management.models import NonConformance
from xhtml2pdf import pisa

class MockRequest:
    scheme = "http"
    def get_host(self):
        return "127.0.0.1:8000"

ncs = NonConformance.objects.all()
html_string = render_to_string('management/non_conformance_log.html', {'ncs': ncs, 'request': MockRequest()})

with open('test_output.pdf', 'wb') as f:
    pisa_status = pisa.CreatePDF(html_string, dest=f)

if pisa_status.err:
    print("PISA ERROR!")
else:
    print("SUCCESS!")
