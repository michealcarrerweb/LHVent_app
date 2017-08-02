from __future__ import unicode_literals

import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from django.shortcuts import get_object_or_404

from customer_finance.models import Invoice, InvoiceAlteration


class MyPrint:
    def __init__(self, buffer, pagesize, slug):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize
        self.slug = slug

    @staticmethod
    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='head-centered', fontSize=18, alignment=TA_CENTER))
 
        # Header
        header = Paragraph(
            'Lehigh Valley Lint Removal - ' + str(datetime.date.today()), styles['head-centered']
            )
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
 
        # Footer
        footer = Paragraph('Thank you for choosing Lehigh Valley Lint Removal', styles['head-centered'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
 
        # Release the canvas
        canvas.restoreState()
 
    def print_users(self):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch/2,
                                leftMargin=inch/2,
                                topMargin=inch/1.3,
                                bottomMargin=inch/2,
                                pagesize=self.pagesize)
 
        # Our container for 'Flowable' objects
        elements = []
 
        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', fontSize=13, alignment=TA_CENTER))
 
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        invoice = get_object_or_404(Invoice, slug=self.slug)

        full_name = "{}".format(invoice.work_order.client.full_family_name())
        address_line1 = invoice.work_order.client.account.get_address()
        num = str(invoice.pk)
        if len(num) < 5:
            while len(num) < 5:
                num = "0" + num
        balance_due = invoice.get_balance_due()
        element_list = [
            ("4561 Center Lane", 'centered', 1, 4),
            ("Foglesville PA 18921", 'centered', 1, 4),
            ("1800 345 5555", 'centered', 1, 4),
            ("Permit 087-2344-999821", 'centered', 1, 4),
            ("Tax ID 23-543-12", 'centered', 1, 12),

            ("{} - Invoice # {} - {}".format(
                full_name, num, str(datetime.datetime.now().date())), 'Heading3', 0, 0),
            ("Service description:", 'Heading4', 0, 0),
            (invoice.work_order.description, 'Normal', 1, 12),
            (full_name, 'Normal', 0, 0),
            (address_line1, 'Normal', 1, 12),
            ("Service charge: $" + str(
                invoice.invoice_quote.total_price_quoted - invoice.invoice_quote.tax_on_quote), 
                'Normal', 0, 0),
            ("Taxes: $" + str(
                invoice.invoice_quote.tax_on_quote), 'Normal', 0, 0),
            ("Total: $" + str(
                invoice.invoice_quote.total_price_quoted), 'Normal', 1, 12),
            
        ]
        for element in element_list:
            elements.append(Paragraph(element[0], styles[element[1]]))
            elements.append(Spacer(element[2], element[3]))
        total_alterations = InvoiceAlteration.objects.filter(invoice=invoice)
        payments = 0
        if total_alterations:
            for item in total_alterations:
                payments += item.transaction_amount
        elements.append(Paragraph("Total payments: $" + str(payments), styles['Normal']))
        if balance_due > 0:
            elements.append(Paragraph("Balance due: $" + str(invoice.get_balance_due()), styles['Heading4']))
            if invoice.due_by:
                elements.append(Paragraph("Due on or before: " + invoice.due_by.strftime('%m/%d/%Y'), styles['Normal']))
        elif balance_due < 0:
            elements.append(Paragraph("Refund: $" + str(invoice.get_balance_due()), styles['Heading4']))       
        else:
            elements.append(Paragraph("PAID IN FULL, thank you!", styles['Normal']))
 
        doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer)#,
                  # canvasmaker=NumberedCanvas)
 
        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf  
