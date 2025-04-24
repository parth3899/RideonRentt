from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def set_default_address(apps, schema_editor):
    UserDetails = apps.get_model('carRental', 'UserDetails')  # Replace 'carRental' with your app's name
    UserDetails.objects.filter(Address__isnull=True).update(Address='Not provided')

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carRental', '0001_initial'),  # Replace with your actual previous migration file name
    ]

    operations = [
        migrations.RunPython(set_default_address),
        migrations.AlterField(
            model_name='userdetails',
            name='Address',
            field=models.CharField(max_length=250, null=False),  # Change to non-nullable
        ),
        migrations.AlterField(
            model_name='booking',
            name='BookingNumber',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='FromDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='LastUpdationDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='Status',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='ToDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='VehicleId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='carRental.vehicles'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='message',
            field=models.CharField(max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='carRental.userdetails'),
        ),
        migrations.AlterField(
            model_name='brands',
            name='BrandName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='brands',
            name='UpdationDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='contactusinfo',
            name='Address',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='contactusinfo',
            name='ContactNo',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='contactusinfo',
            name='EmailId',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contactusquery',
            name='ContactNo',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='contactusquery',
            name='EmailId',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contactusquery',
            name='Message',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='contactusquery',
            name='Name',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='contactusquery',
            name='Status',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='City',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='ContactNo',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='Country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='UpdationDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='AirConditioner',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='AntiLockBrakingSystem',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='BrakeAssist',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='CDPlayer',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='CentralLocking',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='CrashSensor',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='DriverAirbag',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='FuelType',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='LeatherSeats',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='ModelYear',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='PassengerAirbag',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='PowerDoorLocks',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='PowerSteering',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='PowerWindows',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='PricePerDay',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='SeatingCapacity',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='UpdationDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='VehiclesBrand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='carRental.brands'),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='VehiclesOverview',
            field=models.CharField(max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='VehiclesTitle',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
