from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    service_type = models.CharField(max_length=100)
    service_date = models.DateField()
    additional_info = models.TextField(blank=True, null=True)
    fees = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    remaining_fees = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=[('USD', 'USD'), ('IQD', 'IQD')], default='USD')
    created_at = models.DateTimeField(auto_now_add=True)

    # Fields to store the initial data
    initial_name = models.CharField(max_length=100, blank=True, null=True)
    initial_phone = models.CharField(max_length=15, blank=True, null=True)
    initial_email = models.EmailField(blank=True, null=True)
    initial_service_type = models.CharField(max_length=100, blank=True, null=True)
    initial_service_date = models.DateField(blank=True, null=True)
    initial_additional_info = models.TextField(blank=True, null=True)
    initial_fees = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)    

    def save(self, *args, **kwargs):
        if not self.pk:
            # On creation, set initial data fields
            self.initial_name = self.name
            self.initial_phone = self.phone
            self.initial_email = self.email
            self.initial_service_type = self.service_type
            self.initial_service_date = self.service_date
            self.initial_additional_info = self.additional_info
            self.initial_fees = self.fees
        super().save(*args, **kwargs)
