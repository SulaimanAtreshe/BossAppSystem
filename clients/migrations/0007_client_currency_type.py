# Generated by Django 5.0.6 on 2024-07-03 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_client_paid_fees_client_remaining_fees'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='currency_type',
            field=models.CharField(choices=[('USD', 'Dollar'), ('IQD', 'Dinar')], default='USD', max_length=3),
        ),
    ]
