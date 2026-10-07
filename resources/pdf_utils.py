import io
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_iso_pdf(model_admin, request, queryset):
    """
    Universal Admin Action to generate an ISO-compliant PDF
    from selected records.
    """
    # Assuming one record selected for simplicity
    if queryset.count() != 1:
        # Just take the first one or loop
        pass
    
    obj = queryset.first()
    model_meta = obj._meta
    
    fields = []
    for f in model_meta.fields:
        if f.name in ['id']: continue
        value = getattr(obj, f.name)
        if hasattr(value, 'all'): # M2M
            value = ", ".join([str(v) for v in value.all()])
        elif f.choices:
            value = dict(f.choices).get(value, value)
        fields.append({
            'name': f.verbose_name.title(),
            'value': str(value) if value is not None else ''
        })
    

    # Try to extract the FRM code from verbose_name
    # e.g. "Training Need Assessment (2.02)" -> "FRM-2.02"
    doc_code = "ISO-17025 Document"
    if "(" in model_meta.verbose_name and ")" in model_meta.verbose_name:
        code = model_meta.verbose_name.split("(")[1].split(")")[0]
        doc_code = f"QCL-FRM-{code}"
        
    context = {
        'doc_title': model_meta.verbose_name.upper(),
        'doc_code': doc_code,
        'date_generated': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'fields': fields,
        'obj': obj,
    }
    
    template_name = 'resources/universal_iso_pdf.html'
    if model_meta.model_name == 'personnelauthorizationpermit':
        template_name = 'resources/pdf_1_01.html'
    if model_meta.model_name == 'competencyevalinternalsample':
        template_name = 'resources/pdf_1_01c.html'
    if model_meta.model_name == 'competencyevalptsample':
        template_name = 'resources/pdf_1_01d.html'
    if model_meta.model_name == 'gradingmatrixequipment':
        template_name = 'resources/pdf_1_01e.html'
    if model_meta.model_name == 'gradingmatrixproduct':
        template_name = 'resources/pdf_1_01f.html'
    if model_meta.model_name == 'gradingmatrixdocument':
        template_name = 'resources/pdf_1_01g.html'
    if model_meta.model_name == 'authorizedanalystlist':
        template_name = 'resources/pdf_1_02.html'
    if model_meta.model_name == 'technicalpersonnellist':
        template_name = 'resources/pdf_1_03.html'
    if model_meta.model_name == 'competencymonitoring':
        template_name = 'resources/pdf_1_04.html'
    if model_meta.model_name == 'trainingneedassessment':
        template_name = 'resources/pdf_2_02.html'
    if model_meta.model_name == 'annualtrainingplan':
        template_name = 'resources/pdf_2_03.html'
    if model_meta.model_name == 'trainingattendancesheet':
        template_name = 'resources/pdf_2_04.html'
    if model_meta.model_name == 'trainingevaluation':
        template_name = 'resources/pdf_2_05.html'
    if model_meta.model_name == 'trainingfeedback':
        template_name = 'resources/pdf_2_07.html'
    if model_meta.model_name == 'individualtrainingrecord':
        template_name = 'resources/pdf_2_08.html'
    if model_meta.model_name == 'orientationplan':
        template_name = 'resources/pdf_2_09.html'
    if model_meta.model_name == 'competencereassessment':
        template_name = 'resources/pdf_2_10.html'
    if model_meta.model_name == 'trainerevaluation':
        template_name = 'resources/pdf_2_12.html'
    
    pdf = render_to_pdf(template_name, context)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"{doc_code}_{obj.id}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponse("Error generating PDF")

generate_iso_pdf.short_description = "Export selected record as ISO PDF"
