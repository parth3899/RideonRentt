# Generated by Django 3.1.12 on 2024-09-30 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carRental', '0004_auto_20240919_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='invoice',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
