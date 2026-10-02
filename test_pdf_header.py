import os
import django
import logging
from io import BytesIO

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lims_core.settings")
django.setup()

from django.template.loader import render_to_string
from management.models import NonConformance
from xhtml2pdf import pisa

pisa.showLogging()

class MockRequest:
    scheme = "http"
    def get_host(self):
        return "127.0.0.1:8000"

ncs = NonConformance.objects.all()
html_string = render_to_string('management/non_conformance_log.html', {'ncs': ncs, 'request': MockRequest()})

out = BytesIO()
pisa_status = pisa.CreatePDF(html_string, dest=out)
print("Errors?", pisa_status.err)
