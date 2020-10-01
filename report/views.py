from django.contrib import messages
from django.shortcuts import render, redirect
from account.models import Customer, Supplier
from items.models import Product, Stock, Order
from account.decorators import login_required
from datetime import datetime, date, time
from django.http import HttpResponse
from django.db.models import Sum
from django.core.files.storage import FileSystemStorage
from reportlab.lib.enums import TA_CENTER
import reportlab.lib.pagesizes
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape
import xlwt
import calendar
import ssms.settings
import logging.config
log = ssms.settings.log_setting()
logging.config.dictConfig(log)
mylog = logging.getLogger('report')


def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % (doc.page))
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % (doc.page))
    canvas.restoreState()


def myLandscapePage(canvas, doc):
    canvas.saveState()
    canvas.setPageSize(landscape(letter))
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, ""))
    canvas.restoreState()


"""Customer Report"""
@login_required("logged_in", 'account:login')
def customer_report(request):
    try:
        language = "Eng"
        if 'language' in request.session:
            language = request.session['language']
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'urls': request.session['urls'],
            'language': language,
        }
        context = {
            'data': userdata,
        }
        return render(request, 'report/customer_report.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
def export_customer_report(request):
    try:
        if request.method == 'POST':
            dataset = Customer.objects.all()
            if not dataset.exists():
                messages.error(request, 'No Data Found')
                return redirect('report:customer_report')

            if 'xls_export' in request.POST:
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="Customer Report.xls"'
                wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
                ws = wb.add_sheet('customer_report')
                row_num = 3

                font_style = xlwt.XFStyle()
                common = "font:name Calibri, bold on, height 200;  align:wrap yes, horiz center, vert center ;"
                common1 = "align: wrap yes, horiz right, vert center ;"

                columns = ['SL', 'Name', 'E-mail', 'Phone', 'Address']

                ws.write_merge(0, 1, 0, 5, 'Customer Report', xlwt.easyxf(common))
                for col in range(len(columns)):
                    ws.write(row_num, col, columns[col], font_style)
                row_num += 1
                for count, data in enumerate((dataset)):
                    ws.write(row_num, 0, count + 1, font_style)
                    ws.write(row_num, 1, data.name, font_style)
                    ws.write(row_num, 2, data.email, font_style)
                    ws.write(row_num, 3, data.phone, font_style)
                    ws.write(row_num, 4, data.address, xlwt.easyxf(common1))
                    row_num += 1

                wb.save(response)
                return response

            elif 'pdf_export' in request.POST:
                styles = getSampleStyleSheet()
                doc = SimpleDocTemplate("assets/pdf_files/Customer Report.pdf", pagesize=reportlab.lib.pagesizes.letter)
                parastyles = ParagraphStyle(
                    'header',
                    parent=styles['Normal'],
                    fontName='Helvetica-Bold',
                    fontSize=8,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                )
                story = []
                elements = []
                columns = []
                columns.insert(0, [Paragraph('S/L', parastyles),
                                   Paragraph('Name', parastyles),
                                   Paragraph('Email', parastyles),
                                   Paragraph('Phone', parastyles),
                                   Paragraph('Address', parastyles)])

                texstyles = ParagraphStyle(
                    'text',
                    parent=styles['Normal'],
                    fontSize=8,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                )
                j = 1

                for count, data in enumerate((dataset)):
                    columns.insert(j, [Paragraph(str(j), texstyles),
                                       Paragraph(str(data.name), texstyles),
                                       Paragraph(str(data.email), texstyles),
                                       Paragraph(str(data.phone), texstyles),
                                       Paragraph(str(data.address), texstyles)])
                    j = j + 1

                t = Table(columns, repeatRows=1, splitByRow=1)
                t.setStyle(TableStyle(
                    [
                        ('FONTSIZE', (0, 0), (-1, -1), 1),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')
                    ]))

                dateofpdf = (datetime.now()).strftime("%d/%m/%Y")
                story.append(Paragraph("Customer Report", parastyles))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph("Printed Date: " + dateofpdf, styles['Normal']))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Spacer(1, 0.2 * inch))
                elements.append(t)
                story.append(t)
                doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
                fs = FileSystemStorage()
                with fs.open("pdf_files/Customer Report.pdf") as pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "Customer Report.pdf"
                    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                    return response
                return response
    except Exception as ex:
        messages.error(request, str(ex))
        mylog.exception('export_customer_report', exc_info=True)
        return redirect('report:customer_report')


"""Supplier Report"""
@login_required("logged_in", 'account:login')
def supplier_report(request):
    try:
        language = "Eng"
        if 'language' in request.session:
            language = request.session['language']
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'urls': request.session['urls'],
            'language': language,
        }
        context = {
            'data': userdata,
        }
        return render(request, 'report/supplier_report.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
def export_supplier_report(request):
    try:
        if request.method == 'POST':
            dataset = Supplier.objects.all()
            if not dataset.exists():
                messages.error(request, 'No Data Found')
                return redirect('report:supplier_report')

            if 'xls_export' in request.POST:
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="Supplier Report.xls"'
                wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
                ws = wb.add_sheet('supplier_report')
                row_num = 3

                font_style = xlwt.XFStyle()
                common = "font:name Calibri, bold on, height 200;  align:wrap yes, horiz center, vert center ;"
                common1 = "align: wrap yes, horiz right, vert center ;"

                columns = ['SL', 'Name', 'E-mail', 'Phone', 'Address']

                ws.write_merge(0, 1, 0, 5, 'Supplier Report', xlwt.easyxf(common))
                for col in range(len(columns)):
                    ws.write(row_num, col, columns[col], font_style)
                row_num += 1
                for count, data in enumerate((dataset)):
                    ws.write(row_num, 0, count + 1, font_style)
                    ws.write(row_num, 1, data.name, font_style)
                    ws.write(row_num, 2, data.email, font_style)
                    ws.write(row_num, 3, data.phone, font_style)
                    ws.write(row_num, 4, data.address, xlwt.easyxf(common1))
                    row_num += 1

                wb.save(response)
                return response

            elif 'pdf_export' in request.POST:
                styles = getSampleStyleSheet()
                doc = SimpleDocTemplate("assets/pdf_files/Supplier Report.pdf", pagesize=reportlab.lib.pagesizes.letter)
                parastyles = ParagraphStyle(
                    'header',
                    parent=styles['Normal'],
                    fontName='Helvetica-Bold',
                    fontSize=8,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                )
                story = []
                elements = []
                columns = []
                columns.insert(0, [Paragraph('S/L', parastyles),
                                   Paragraph('Name', parastyles),
                                   Paragraph('Email', parastyles),
                                   Paragraph('Phone', parastyles),
                                   Paragraph('Address', parastyles)])

                texstyles = ParagraphStyle(
                    'text',
                    parent=styles['Normal'],
                    fontSize=8,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                )
                j = 1

                for count, data in enumerate((dataset)):
                    columns.insert(j, [Paragraph(str(j), texstyles),
                                       Paragraph(str(data.name), texstyles),
                                       Paragraph(str(data.email), texstyles),
                                       Paragraph(str(data.phone), texstyles),
                                       Paragraph(str(data.address), texstyles)])
                    j = j + 1

                t = Table(columns, repeatRows=1, splitByRow=1)
                t.setStyle(TableStyle(
                    [
                        ('FONTSIZE', (0, 0), (-1, -1), 1),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')
                    ]))

                dateofpdf = (datetime.now()).strftime("%d/%m/%Y")
                story.append(Paragraph("Supplier Report", parastyles))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph("Printed Date: " + dateofpdf, styles['Normal']))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Spacer(1, 0.2 * inch))
                elements.append(t)
                story.append(t)
                doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
                fs = FileSystemStorage()
                with fs.open("pdf_files/Supplier Report.pdf") as pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "Supplier Report.pdf"
                    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                    return response
                return response
    except Exception as ex:
        messages.error(request, str(ex))
        mylog.exception('export_supplier_report', exc_info=True)
        return redirect('report:supplier_report')


"""Product Report"""
@login_required("logged_in", 'account:login')
def product_report(request):
    try:
        language = "Eng"
        if 'language' in request.session:
            language = request.session['language']
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'urls': request.session['urls'],
            'language': language,
        }
        context = {
            'data': userdata,
        }
        return render(request, 'report/product_report.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
def export_product_report(request):
    try:
        if request.method == 'POST':
            dataset = Product.objects.all()
            if not dataset.exists():
                messages.error(request, 'No Data Found')
                return redirect('report:product_report')

            if 'xls_export' in request.POST:
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="Product Report.xls"'
                wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
                ws = wb.add_sheet('product_report')
                row_num = 3

                font_style = xlwt.XFStyle()
                common = "font:name Calibri, bold on, height 200;  align:wrap yes, horiz center, vert center ;"
                common1 = "align: wrap yes, horiz right, vert center ;"

                columns = ['SL', 'Name', 'Brand', 'Size', 'Category', 'Expiry Date', 'Price']

                ws.write_merge(0, 1, 0, 5, 'Product Report', xlwt.easyxf(common))
                for col in range(len(columns)):
                    ws.write(row_num, col, columns[col], font_style)
                row_num += 1
                for count, data in enumerate((dataset)):
                    ws.write(row_num, 0, count + 1, font_style)
                    ws.write(row_num, 1, data.name, font_style)
                    ws.write(row_num, 2, data.brand, font_style)
                    ws.write(row_num, 3, data.size, font_style)
                    ws.write(row_num, 4, data.category.name, font_style)
                    ws.write(row_num, 5, str(data.expiry_date), font_style)
                    ws.write(row_num, 6, data.price, xlwt.easyxf(common1))
                    row_num += 1

                wb.save(response)
                return response

            elif 'pdf_export' in request.POST:
                styles = getSampleStyleSheet()
                doc = SimpleDocTemplate("assets/pdf_files/Product Report.pdf", pagesize=reportlab.lib.pagesizes.letter)
                parastyles = ParagraphStyle(
                    'header',
                    parent=styles['Normal'],
                    fontName='Helvetica-Bold',
                    fontSize=8,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                )
                story = []
                elements = []
                columns = []
                columns.insert(0, [Paragraph('S/L', parastyles),
                                   Paragraph('Name', parastyles),
                                   Paragraph('Brand', parastyles),
                                   Paragraph('Size', parastyles),
                                   Paragraph('Category', parastyles),
                                   Paragraph('Expiry Date', parastyles),
                                   Paragraph('Price', parastyles)])

                texstyles = ParagraphStyle(
                    'text',
                    parent=styles['Normal'],
                    fontSize=8,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                )
                j = 1

                for count, data in enumerate((dataset)):
                    columns.insert(j, [Paragraph(str(j), texstyles),
                                       Paragraph(str(data.name), texstyles),
                                       Paragraph(str(data.brand), texstyles),
                                       Paragraph(str(data.size), texstyles),
                                       Paragraph(str(data.category), texstyles),
                                       Paragraph(str(data.expiry_date), texstyles),
                                       Paragraph(str(data.price), texstyles)])
                    j = j + 1
                t = Table(columns, repeatRows=1, splitByRow=1)
                t.setStyle(TableStyle(
                    [
                        ('FONTSIZE', (0, 0), (-1, -1), 1),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')
                    ]))

                dateofpdf = (datetime.now()).strftime("%d/%m/%Y")
                story.append(Paragraph("Product Report", parastyles))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph("Printed Date: " + dateofpdf, styles['Normal']))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Spacer(1, 0.2 * inch))
                elements.append(t)
                story.append(t)
                doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
                fs = FileSystemStorage()
                with fs.open("pdf_files/Product Report.pdf") as pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "Product Report.pdf"
                    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                    return response
                return response
    except Exception as ex:
        messages.error(request, str(ex))
        mylog.exception('export_product_report', exc_info=True)
        return redirect('report:product_report')


"""Stock Report"""
@login_required("logged_in", 'account:login')
def stock_report(request):
    try:
        language = "Eng"
        if 'language' in request.session:
            language = request.session['language']
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'urls': request.session['urls'],
            'language': language,
        }
        context = {
            'data': userdata,
        }
        return render(request, 'report/stock_report.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
def export_stock_report(request):
    try:
        if request.method == 'POST':
            start_date = request.POST['from_date']
            end_date = request.POST['to_date']
            filter_args = {}
            smonth, sday, syear = start_date.split('/')
            emonth, eday, eyear = end_date.split('/')
            start_date = date(int(syear), int(smonth), int(sday))
            end_date = date(int(eyear), int(emonth), int(eday))
            filter_args['created_date__range'] = (
                datetime.combine(start_date, time.min), datetime.combine(end_date, time.max))
            daterange = 'From ' + start_date.strftime('%b %d, %Y') + ' to ' + end_date.strftime('%b %d, %Y')
            dataset = Stock.objects.filter(**filter_args)
            if not dataset.exists():
                messages.error(request, 'No Data Found')
                return redirect('report:stock_report')

            if 'xls_export' in request.POST:
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="Stock Report.xls"'
                wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
                ws = wb.add_sheet('stock_report')
                row_num = 4

                font_style = xlwt.XFStyle()
                common = "font:name Calibri, bold on, height 200;  align:wrap yes, horiz center, vert center ;"
                common1 = "align: wrap yes, horiz right, vert center ;"

                columns = ['SL', 'Name', 'Brand', 'Size', 'Category', 'Price', 'Quantity', 'Expiry Date', 'Supplier']

                ws.write_merge(0, 1, 0, 5, 'Stock Report', xlwt.easyxf(common))
                ws.write_merge(2, 3, 0, 5, daterange, xlwt.easyxf(common))
                for col in range(len(columns)):
                    ws.write(row_num, col, columns[col], font_style)
                row_num += 1
                for count, data in enumerate((dataset)):
                    ws.write(row_num, 0, count + 1, font_style)
                    ws.write(row_num, 1, data.product.name, font_style)
                    ws.write(row_num, 2, data.product.brand, font_style)
                    ws.write(row_num, 3, data.product.size, font_style)
                    ws.write(row_num, 4, data.product.category.name, font_style)
                    ws.write(row_num, 5, str(data.product.price), font_style)
                    ws.write(row_num, 6, str(data.quantity), font_style)
                    ws.write(row_num, 7, str(data.expiry_date), font_style)
                    ws.write(row_num, 8, data.supplier.name, xlwt.easyxf(common1))
                    row_num += 1

                wb.save(response)
                return response

            elif 'pdf_export' in request.POST:
                styles = getSampleStyleSheet()
                doc = SimpleDocTemplate("assets/pdf_files/Stock Report.pdf", pagesize=reportlab.lib.pagesizes.landscape(letter))
                parastyles = ParagraphStyle(
                    'header',
                    parent=styles['Normal'],
                    fontName='Helvetica-Bold',
                    fontSize=8,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                )
                story = []
                elements = []
                columns = []
                columns.insert(0, [Paragraph('S/L', parastyles),
                                   Paragraph('Name', parastyles),
                                   Paragraph('Brand', parastyles),
                                   Paragraph('Size', parastyles),
                                   Paragraph('Category', parastyles),
                                   Paragraph('Price', parastyles),
                                   Paragraph('Quantity', parastyles),
                                   Paragraph('Expiry Date', parastyles),
                                   Paragraph('Supplier', parastyles)])

                texstyles = ParagraphStyle(
                    'text',
                    parent=styles['Normal'],
                    fontSize=8,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                )
                j = 1

                for count, data in enumerate((dataset)):
                    columns.insert(j, [Paragraph(str(j), texstyles),
                                       Paragraph(str(data.product.name), texstyles),
                                       Paragraph(str(data.product.brand), texstyles),
                                       Paragraph(str(data.product.size), texstyles),
                                       Paragraph(str(data.product.category), texstyles),
                                       Paragraph(str(data.product.price), texstyles),
                                       Paragraph(str(data.quantity), texstyles),
                                       Paragraph(str(data.expiry_date), texstyles),
                                       Paragraph(str(data.supplier.name), texstyles)])
                    j = j + 1
                t = Table(columns, repeatRows=1, splitByRow=1)
                t.setStyle(TableStyle(
                    [
                        ('FONTSIZE', (0, 0), (-1, -1), 1),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')
                    ]))

                dateofpdf = (datetime.now()).strftime("%d/%m/%Y")
                story.append(Paragraph("Stock Report", parastyles))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph(daterange, parastyles))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph("Printed Date: " + dateofpdf, styles['Normal']))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Spacer(1, 0.2 * inch))
                elements.append(t)
                story.append(t)
                doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
                fs = FileSystemStorage()
                with fs.open("pdf_files/Stock Report.pdf") as pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "Stock Report.pdf"
                    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                    return response
                return response
    except Exception as ex:
        messages.error(request, str(ex))
        mylog.exception('export_stock_report', exc_info=True)
        return redirect('report:stock_report')


"""Sales Report"""
@login_required("logged_in", 'account:login')
def sales_report(request):
    try:
        language = "Eng"
        if 'language' in request.session:
            language = request.session['language']
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'urls': request.session['urls'],
            'language': language,
        }
        context = {
            'data': userdata,
        }
        return render(request, 'report/sales_report.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
def export_sales_report(request):
    try:
        if request.method == 'POST':
            start_date = request.POST['from_date']
            end_date = request.POST['to_date']
            filter_args = {}
            smonth, sday, syear = start_date.split('/')
            emonth, eday, eyear = end_date.split('/')
            start_date = date(int(syear), int(smonth), int(sday))
            end_date = date(int(eyear), int(emonth), int(eday))
            filter_args['ordered_date__range'] = (
                datetime.combine(start_date, time.min), datetime.combine(end_date, time.max))
            daterange = 'From ' + start_date.strftime('%b %d, %Y') + ' to ' + end_date.strftime('%b %d, %Y')
            dataset = Order.objects.filter(**filter_args)
            if not dataset.exists():
                messages.error(request, 'No Data Found')
                return redirect('report:sales_report')

            if 'xls_export' in request.POST:
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="Sales Report.xls"'
                wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
                ws = wb.add_sheet('sales_report')
                row_num = 4

                font_style = xlwt.XFStyle()
                common = "font:name Calibri, bold on, height 200;  align:wrap yes, horiz center, vert center ;"
                common1 = "align: wrap yes, horiz right, vert center ;"
                columns = ['SL', 'Product', 'Brand', 'Category', 'Size', 'Unit Price', 'Quantity', 'Customer Name', 'Customer Phone', 'Shipping Address', 'Order Date', 'Discount Rate', 'Total Price']

                ws.write_merge(0, 1, 0, 5, 'Sales Report', xlwt.easyxf(common))
                ws.write_merge(2, 3, 0, 5, daterange, xlwt.easyxf(common))
                for col in range(len(columns)):
                    ws.write(row_num, col, columns[col], font_style)

                total = 0.0
                row_num += 1
                for count, data in enumerate((dataset)):
                    discount_rate = 0.0
                    if data.discount:
                        discount_rate = data.discount.rate
                    total += data.product.price
                    ws.write(row_num, 0, count + 1, font_style)
                    ws.write(row_num, 1, data.product.name, font_style)
                    ws.write(row_num, 2, data.product.brand, font_style)
                    ws.write(row_num, 3, data.product.category.name, font_style)
                    ws.write(row_num, 4, data.product.size, font_style)
                    ws.write(row_num, 5, str(data.product.price), font_style)
                    ws.write(row_num, 6, str(data.quantity), font_style)
                    ws.write(row_num, 7, data.customer.name, font_style)
                    ws.write(row_num, 8, data.customer.phone, font_style)
                    ws.write(row_num, 9, data.shipping_address, font_style)
                    ws.write(row_num, 10, str(data.ordered_date), font_style)
                    ws.write(row_num, 11, str(discount_rate), font_style)
                    ws.write(row_num, 12, str(data.net_total), xlwt.easyxf(common1))
                    row_num += 1

                ws.write(row_num, 11, "Total", font_style)
                ws.write(row_num, 12, str(total), xlwt.easyxf(common1))

                wb.save(response)
                return response

            elif 'pdf_export' in request.POST:
                styles = getSampleStyleSheet()
                doc = SimpleDocTemplate("assets/pdf_files/Sales Report.pdf", pagesize=reportlab.lib.pagesizes.landscape(letter))
                parastyles = ParagraphStyle(
                    'header',
                    parent=styles['Normal'],
                    fontName='Helvetica-Bold',
                    fontSize=8,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                )
                story = []
                elements = []
                columns = []
                columns.insert(0, [Paragraph('S/L', parastyles),
                                   Paragraph('Product', parastyles),
                                   Paragraph('Brand', parastyles),
                                   Paragraph('Category', parastyles),
                                   Paragraph('Size', parastyles),
                                   Paragraph('Unit Price', parastyles),
                                   Paragraph('Quantity', parastyles),
                                   Paragraph('Customer Name', parastyles),
                                   Paragraph('Customer Phone', parastyles),
                                   Paragraph('Shipping Address', parastyles),
                                   Paragraph('Order Date', parastyles),
                                   Paragraph('Discount Rate', parastyles),
                                   Paragraph('Total Price', parastyles)])

                texstyles = ParagraphStyle(
                    'text',
                    parent=styles['Normal'],
                    fontSize=8,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                )
                total = 0.0
                j = 1
                for count, data in enumerate((dataset)):
                    discount_rate = 0.0
                    if data.discount:
                        discount_rate = data.discount.rate
                    total += data.product.price
                    columns.insert(j, [Paragraph(str(j), texstyles),
                                       Paragraph(str(data.product.name), texstyles),
                                       Paragraph(str(data.product.brand), texstyles),
                                       Paragraph(str(data.product.category.name), texstyles),
                                       Paragraph(str(data.product.size), texstyles),
                                       Paragraph(str(data.product.price), texstyles),
                                       Paragraph(str(data.quantity), texstyles),
                                       Paragraph(str(data.customer.name), texstyles),
                                       Paragraph(str(data.customer.phone), texstyles),
                                       Paragraph(str(data.shipping_address), texstyles),
                                       Paragraph(str(data.ordered_date), texstyles),
                                       Paragraph(str(discount_rate), texstyles),
                                       Paragraph(str(data.net_total), texstyles)])
                    j = j + 1
                columns.insert(j, [Paragraph("", texstyles),
                                   Paragraph("", texstyles),
                                   Paragraph("", texstyles),
                                   Paragraph("", texstyles),
                                   Paragraph("", texstyles),
                                   Paragraph("", texstyles),
                                   Paragraph("", texstyles),
                                   Paragraph("", texstyles),
                                   Paragraph("", texstyles),
                                   Paragraph("", texstyles),
                                   Paragraph("", texstyles),
                                   Paragraph("Total", texstyles),
                                   Paragraph(str(total), texstyles)])
                t = Table(columns, repeatRows=1, splitByRow=1)
                t.setStyle(TableStyle(
                    [
                        ('FONTSIZE', (0, 0), (-1, -1), 1),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')
                    ]))

                dateofpdf = (datetime.now()).strftime("%d/%m/%Y")
                story.append(Paragraph("Sales Report", parastyles))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph(daterange, parastyles))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph("Printed Date: " + dateofpdf, styles['Normal']))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Spacer(1, 0.2 * inch))
                elements.append(t)
                story.append(t)
                doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
                fs = FileSystemStorage()
                with fs.open("pdf_files/Sales Report.pdf") as pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "Sales Report.pdf"
                    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                    return response
                return response
    except Exception as ex:
        messages.error(request, str(ex))
        mylog.exception('export_sales_report', exc_info=True)
        return redirect('report:sales_report')


"""Profit/Loss Report"""
@login_required("logged_in", 'account:login')
def profit_loss_report(request):
    try:
        language = "Eng"
        if 'language' in request.session:
            language = request.session['language']
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'urls': request.session['urls'],
            'language': language,
        }
        context = {
            'data': userdata,
        }
        return render(request, 'report/profit_loss_report.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
def export_profit_loss_report(request):
    try:
        if request.method == 'POST':
            order_filter_args = {}
            stock_filter_args = {}
            year = request.POST['year']
            month_obj = Get_Processed_Month(request.POST['month'], year)
            month = month_obj[0]
            order_filter_args['ordered_date__range'] = (datetime.combine(month_obj[1], time.min), datetime.combine(month_obj[2], time.max))
            stock_filter_args['created_date__range'] = (datetime.combine(month_obj[1], time.min), datetime.combine(month_obj[2], time.max))
            daterange = 'Report for - ' + str(month) + ', ' + str(year)
            no_of_order = Order.objects.filter(**order_filter_args).aggregate(Sum('id'))['id__sum']
            sum_of_order = Order.objects.filter(**order_filter_args).aggregate(Sum('net_total'))['net_total__sum']
            no_of_stock = Stock.objects.filter(**stock_filter_args).aggregate(Sum('id'))['id__sum']
            sum_of_stock = Stock.objects.filter(**stock_filter_args).aggregate(Sum('total_price'))['total_price__sum']
            if 'xls_export' in request.POST:
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="Profit-Loss Report.xls"'
                wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
                ws = wb.add_sheet('profit_loss_report')
                common = "font:name Calibri, bold on, height 200;  align:wrap yes, horiz center, vert center ;"
                ws.write_merge(0, 1, 0, 5, 'Profit-Loss Report', xlwt.easyxf(common))
                ws.write_merge(2, 3, 0, 5, daterange, xlwt.easyxf(common))
                ws.write_merge(5, 5, 0, 5, "No of Total Order - " + str(no_of_order), xlwt.easyxf(common))
                ws.write_merge(6, 6, 0, 5, "Sum of Total Order - " + str(sum_of_order), xlwt.easyxf(common))
                ws.write_merge(8, 8, 0, 5, "No of Total Purchase - " + str(no_of_stock), xlwt.easyxf(common))
                ws.write_merge(9, 9, 0, 5, "Sum of Total Purchase - " + str(sum_of_stock), xlwt.easyxf(common))
                wb.save(response)
                return response

            elif 'pdf_export' in request.POST:
                styles = getSampleStyleSheet()
                doc = SimpleDocTemplate("assets/pdf_files/Profit-Loss Report.pdf", pagesize=reportlab.lib.pagesizes.letter)
                parastyles = ParagraphStyle(
                    'header',
                    parent=styles['Normal'],
                    fontName='Helvetica-Bold',
                    fontSize=12,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                )
                story = []
                dateofpdf = (datetime.now()).strftime("%d/%m/%Y")
                story.append(Paragraph("Profit-Loss Report", parastyles))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph(daterange, styles['Normal']))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph("Printed Date: " + dateofpdf, styles['Normal']))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph("No of Total Order - " + str(no_of_order), parastyles))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph("Sum of Total Order - " + str(sum_of_order), parastyles))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph("No of Total Purchase - " + str(no_of_stock), parastyles))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph("Sum of Total Purchase - " + str(sum_of_stock), parastyles))
                doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
                fs = FileSystemStorage()
                with fs.open("pdf_files/Profit-Loss Report.pdf") as pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "Profit-Loss Report.pdf"
                    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                    return response
                return response
    except Exception as ex:
        messages.error(request, str(ex))
        mylog.exception('export_profit_loss_report', exc_info=True)
        return redirect('report:profit_loss_report')


def Get_Processed_Month(month, year):
    try:
        w_month = "December"
        if month == "1":
            w_month = "January"
        elif month == "2":
            w_month = "February"
        elif month == "3":
            w_month = "March"
        elif month == "4":
            w_month = "April"
        elif month == "5":
            w_month = "May"
        elif month == "6":
            w_month = "June"
        elif month == "7":
            w_month = "July"
        elif month == "8":
            w_month = "August"
        elif month == "9":
            w_month = "September"
        elif month == "10":
            w_month = "October"
        elif month == "11":
            w_month = "November"
        num_days = calendar.monthrange(int(year), int(month))
        from_date = str(year) + "/" + str(month) + "/01"
        to_date = str(year) + "/" + str(month) + "/" + str(num_days[1])
        syear, smonth, sday = from_date.split('/')
        eyear, emonth, eday = to_date.split('/')
        start_date = date(int(syear), int(smonth), int(sday))
        end_date = date(int(eyear), int(emonth), int(eday))
        all_items = [w_month, start_date, end_date]
        return all_items
    except Exception:
        mylog.exception('get_processed_month_for_report', exc_info=True)
        return redirect('report:profit_loss_report')
