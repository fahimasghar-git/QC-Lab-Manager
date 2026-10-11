import io
import re
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from django.contrib import admin

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

@admin.action(description="🖨️ Print / Export ISO PDF")
def generate_iso_pdf(model_admin, request, queryset):
    """
    Universal Admin Action to generate an ISO-compliant PDF
    from selected records.
    """
    if not queryset.exists():
        return HttpResponse("No records selected", status=400)
    
    obj = queryset.first()
    model_meta = obj._meta
    
    fields = []
    for f in model_meta.fields:
        if f.name in ['id']: continue
        value = getattr(obj, f.name, None)
        if hasattr(value, 'all'): # M2M
            value = ", ".join([str(v) for v in value.all()])
        elif getattr(f, 'choices', None):
            value = dict(f.choices).get(value, value)
        fields.append({
            'name': f.verbose_name.title(),
            'value': str(value) if value is not None else ''
        })

    # Try to extract the FRM code from verbose_name or model_name
    doc_code = "ISO-17025 Document"
    if "(" in model_meta.verbose_name and ")" in model_meta.verbose_name:
        code = model_meta.verbose_name.split("(")[1].split(")")[0]
        doc_code = f"QCL-FRM-{code}"
    else:
        m = re.search(r'(\d+)_(\d+)', model_meta.model_name)
        if m:
            doc_code = f"QCL-FRM-{m.group(1)}.{m.group(2)}"
        
    raw_title = str(model_meta.verbose_name)
    if "(" in raw_title:
        clean_title = raw_title.split("(")[0].strip().upper()
    else:
        clean_title = raw_title.upper()

    context = {
        'doc_title': clean_title,
        'doc_code': doc_code,
        'date_generated': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'fields': fields,
        'obj': obj,
    }
    
    template_name = 'resources/universal_iso_pdf.html'
    
    # Specific legacy mappings
    specific_overrides = {
        'personnelauthorizationpermit': 'resources/pdf_1_01.html',
        'competencyevalinternalsample': 'resources/pdf_1_01c.html',
        'competencyevalptsample': 'resources/pdf_1_01d.html',
        'gradingmatrixequipment': 'resources/pdf_1_01e.html',
        'gradingmatrixproduct': 'resources/pdf_1_01f.html',
        'gradingmatrixdocument': 'resources/pdf_1_01g.html',
        'authorizedanalystlist': 'resources/pdf_1_02.html',
        'technicalpersonnellist': 'resources/pdf_1_03.html',
        'competencymonitoring': 'resources/pdf_1_04.html',
        'trainingneedassessment': 'resources/pdf_2_02.html',
        'annualtrainingplan': 'resources/pdf_2_03.html',
        'trainingattendancesheet': 'resources/pdf_2_04.html',
        'trainingevaluation': 'resources/pdf_2_05.html',
        'trainingfeedback': 'resources/pdf_2_07.html',
        'individualtrainingrecord': 'resources/pdf_2_08.html',
        'orientationplan': 'resources/pdf_2_09.html',
        'competencereassessment': 'resources/pdf_2_10.html',
        'trainerevaluation': 'resources/pdf_2_12.html',
    }
    
    m_name = model_meta.model_name.lower()
    if m_name in specific_overrides:
        template_name = specific_overrides[m_name]
    else:
        # Check if model has a pattern like _12_01 or 12_01
        m = re.search(r'(\d+_\d+)', m_name)
        if m:
            candidate = f"resources/pdf_{m.group(1)}.html"
            try:
                get_template(candidate)
                template_name = candidate
            except Exception:
                pass

    response = render_to_pdf(template_name, context)

    if response:
        filename = f"{doc_code}_{obj.id}.pdf"
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response
    return HttpResponse("Error generating PDF")

# Alias for compatibility
generate_pdf = generate_iso_pdf
