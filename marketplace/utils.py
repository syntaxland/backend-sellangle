from django.http import HttpResponse
from django.template.loader import get_template

def render_to_pdf(template_path, context):
    template = get_template(template_path)
    html = template.render(context)
    pdf = render_to_pdf('ad_charges_receipt_pdf_template.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Ad_Charges_Receipt.pdf"
        content = "attachment; filename=%s" % filename
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not Found")
