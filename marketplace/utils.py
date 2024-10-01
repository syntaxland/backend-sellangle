# from django.template.loader import get_template
# from xhtml2pdf import pisa
# from io import BytesIO

# def generate_ad_charges_receipt_pdf(ad_charges_data):
#     template_path = 'marketplace/ad_charges_receipt.html'
#     template = get_template(template_path)
#     html = template.render(ad_charges_data)

#     pdf_data = BytesIO()
#     pisa.CreatePDF(html, dest=pdf_data)

#     return pdf_data.getvalue()
