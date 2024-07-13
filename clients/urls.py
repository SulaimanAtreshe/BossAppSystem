from django.urls import path, reverse
from .views import client_list, client_create, client_detail, client_update, client_delete, generate_pdf, generate_pdf_receipt


urlpatterns = [
    path('', client_list, name='client_list'),
    path('new/', client_create, name='client_create'),
    # path('clients/<int:pk>/', client_detail, name='client_detail'),
    path('<int:pk>/', client_detail, name='client_detail'),
    path('<int:pk>/edit/', client_update, name='client_update'),
    path('<int:pk>/delete/', client_delete, name='client_delete'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('clients/<int:pk>/receipt/', generate_pdf_receipt, name='client_receipt_pdf'),
]