# Generated by Django 5.0.6 on 2024-06-26 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='additional_info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
