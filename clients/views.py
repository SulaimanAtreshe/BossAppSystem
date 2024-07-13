from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .models import Client
from .forms import ClientForm
from django.db.models import Count
from collections import defaultdict
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


def client_list(request):
    clients = Client.objects.all().order_by('-service_date')
    grouped_clients = defaultdict(list)
    total_income_per_day_iqd = defaultdict(Decimal)
    total_income_per_day_usd = defaultdict(Decimal)

    for client in clients:
        service_date_str = client.service_date.strftime('%m/%d/%Y')
        grouped_clients[service_date_str].append(client)

        if client.currency == 'IQD':
            total_income_per_day_iqd[service_date_str] += client.paid_fees if client.paid_fees else Decimal(0)
        elif client.currency == 'USD':
            total_income_per_day_usd[service_date_str] += client.paid_fees if client.paid_fees else Decimal(0)

    grouped_clients = dict(sorted(grouped_clients.items(), key=lambda x: datetime.strptime(x[0], '%m/%d/%Y'), reverse=True))

    context = {
        'grouped_clients': grouped_clients,
        'total_income_per_day_iqd': total_income_per_day_iqd,
        'total_income_per_day_usd': total_income_per_day_usd,
    }

    return render(request, 'clients/client_list.html', context)

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'clients/client_form.html', {'form': form})

# def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    
    context = {
        'client': client,
        'form': form,
    }
    return render(request, 'clients/client_detail.html', context)

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    # Get today's date in the local timezone
    today = timezone.localtime().date()
    
    # Query for all clients with the same service date as the client being viewed
    clients = Client.objects.filter(service_date=client.service_date)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
        
    
    # Create forms for all clients
    client_forms = [(client, ClientForm(instance=client)) for client in clients]
    
    context = {
        'clients': clients,
        'client_forms': client_forms,
    }
    return render(request, 'clients/client_detail.html', context)

def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_detail', pk=pk)  # Redirect to client_detail view with updated client pk
    else:
        form = ClientForm(instance=client)
    
    context = {
        'client': client,
        'form': form,
    }
    return render(request, 'clients/client_update.html', context)

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'clients/client_confirm_delete.html', {'client': client})

def home(request):
    return redirect('client_list')

def generate_pdf(request):
    # Get today's date and the start of the day
    today = datetime.now().date()
    start_of_day = datetime.combine(today, datetime.min.time())

    # Filter clients registered today
    clients_today = Client.objects.filter(created_at__gte=start_of_day)

    # Create PDF document
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle('Today\'s Customers Report')

    # Header text
    header_text = 'Boss Salon Daily Report'
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawCentredString(letter[0] / 2, letter[1] - 50, header_text)

    # Set up PDF content
    table_data = []
    table_data.append(['Name', 'Phone', 'Email', 'Service Type', 'Service Date', 'Paid Fees', 'Remaining Fees'])

    for client in clients_today:
        table_data.append([
            client.initial_name,
            client.initial_phone,
            client.initial_email,
            client.initial_service_type,
            str(client.initial_service_date),
            str(client.paid_fees),
            str(client.remaining_fees)
        ])

    # Define the style of the table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
        ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, (0, 0, 0)),
        ('BOX', (0, 0), (-1, -1), 0.25, (0, 0, 0)),
    ])

    # Create the table
    table = Table(table_data)

    # Apply style to the table
    table.setStyle(table_style)

    # Get table width to adjust layout
    table.wrapOn(pdf, 700, 400)
    table_width, table_height = table.wrap(700, 400)

    # Calculate starting point to center the table on the page
    x = (letter[0] - table_width) / 2
    y = letter[1] - 100 - table_height

    # Draw the table on the PDF
    table.drawOn(pdf, x, y)

    # Save the PDF
    pdf.showPage()
    pdf.save()

    # Return the response with PDF mime type
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def generate_pdf_receipt(request, pk):
    client = get_object_or_404(Client, pk=pk)

    # Create a BytesIO buffer to store PDF
    buffer = BytesIO()

    # Create a canvas object
    c = canvas.Canvas(buffer, pagesize=letter)

    # PDF Title
    c.setFont('Helvetica-Bold', 24)
    c.drawCentredString(300, 750, 'Client Receipt')

    # Table data for Client Information
    data = [
        ['Name', client.name],
        ['Phone', client.phone],
        ['Email', client.email],
        ['Service Type', client.service_type],
        ['Service Date', client.service_date.strftime('%Y-%m-%d')],  # Format as needed
        ['Paid Fees', f'{client.paid_fees} {client.currency}'],
        ['Remaining Fees', f'{client.remaining_fees} {client.currency}'],
        ['Additional Information', client.additional_info],
    ]

    # Create a Table object
    table = Table(data, colWidths=[150, 350])

    # Style for the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.burlywood),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ])

    # Apply style to the table
    table.setStyle(style)

    # Position the table on the PDF
    table.wrapOn(c, 800, 600)  # Adjust width and height as needed
    table.drawOn(c, 50, 550)  # Adjust x and y positions as needed

    # Footer
    c.setFont('Helvetica-Bold', 12)
    c.drawRightString(550, 50, 'Boss Salon Management Team')
    c.drawRightString(170, 50, client.name)

    # Save PDF to buffer
    c.showPage()
    c.save()

    # Get the value of BytesIO buffer and return as HttpResponse
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="client_receipt_{client.pk}.pdf"'
    response.write(pdf)

    return response