from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('IQD', 'IQD'),
    ]

    currency = forms.ChoiceField(
        label='Currency',
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'email', 'service_type', 'service_date', 'additional_info', 'fees', 'paid_fees', 'remaining_fees', 'currency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'service_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Type'}),
            'service_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Service Date', 'type': 'date'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional Information'}),
            'fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'paid_fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'remaining_fees': forms.NumberInput(attrs={'class': 'form-control'}),
        }