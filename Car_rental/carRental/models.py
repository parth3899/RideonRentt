from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid

class Brands(models.Model):
    BrandName = models.CharField(max_length=100, null=True, blank=False)
    Creationdate = models.DateTimeField(auto_now_add=True)
    UpdationDate = models.DateField(null=True)

    def __str__(self):
        return self.BrandName

class Contactusinfo(models.Model):
    Address = models.CharField(max_length=250, null=True, blank=False)
    EmailId = models.EmailField(max_length=100, null=True, blank=False)
    ContactNo = models.CharField(max_length=15, null=True, blank=False)  # Adjusted length

    def __str__(self):
        return self.EmailId

class Contactusquery(models.Model):
    Name = models.CharField(max_length=250, null=True, blank=False)
    EmailId = models.EmailField(max_length=100, null=True, blank=False)
    ContactNo = models.CharField(max_length=15, null=True, blank=False)  # Adjusted length
    Message = models.TextField(null=True, blank=False)  # Changed to TextField for longer messages
    PostingDate = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.Name

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_no = models.CharField(max_length=10, null=True, blank=True)
    ContactNo = models.CharField(max_length=15, null=False, blank=False)
    dob = models.DateField(null=False, blank=False)
    Country = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    City = models.CharField(max_length=50, null=False, blank=False)
    Address = models.TextField(null=False, blank=False)
    RegDate = models.DateTimeField(auto_now_add=True)
    UpdationDate = models.DateField(auto_now=True)
    is_owner = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"


class Vehicles(models.Model):
    VehiclesTitle = models.CharField(max_length=250, null=True, blank=False)
    VehiclesBrand = models.ForeignKey(Brands, on_delete=models.CASCADE, null=True)
    VehiclesOverview = models.TextField(null=True, blank=False)  # Changed to TextField for better flexibility
    PricePerDay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False)  # Use DecimalField for currency
    FuelType = models.CharField(max_length=150, null=True, blank=False)
    ModelYear = models.CharField(max_length=4, null=True, blank=False)  # Limit to 4 characters for year
    SeatingCapacity = models.IntegerField(null=True, blank=False)  # Changed to IntegerField for better validation
    Vimage1 = models.FileField(null=True, blank=True)
    Vimage2 = models.FileField(null=True, blank=True)
    Vimage3 = models.FileField(null=True, blank=True)
    Vimage4 = models.FileField(null=True, blank=True)
    Vimage5 = models.FileField(null=True, blank=True)
    AirConditioner = models.BooleanField(default=True)
    PowerDoorLocks = models.BooleanField(default=True)
    AntiLockBrakingSystem = models.BooleanField(default=True)
    BrakeAssist = models.BooleanField(default=True)
    PowerSteering = models.BooleanField(default=True)
    DriverAirbag = models.BooleanField(default=True)
    PassengerAirbag = models.BooleanField(default=True)
    PowerWindows = models.BooleanField(default=True)
    CDPlayer = models.BooleanField(default=True)
    CentralLocking = models.BooleanField(default=True)
    CrashSensor = models.BooleanField(default=True)
    LeatherSeats = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # Other features can be adjusted similarly...

    RegDate = models.DateTimeField(auto_now_add=True)
    UpdationDate = models.DateField(null=True)

    def __str__(self):
        return self.VehiclesTitle

class Booking(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=True)
    BookingNumber = models.CharField(max_length=150, null=True, blank=False)
    VehicleId = models.ForeignKey(Vehicles, on_delete=models.CASCADE, null=True)
    FromDate = models.DateField(null=True, blank=False)
    ToDate = models.DateField(null=True, blank=False)
    message = models.TextField(null=True, blank=True)
    Status = models.CharField(max_length=150, null=True, blank=False)
    PaymentStatus = models.CharField(max_length=150, default="Pending", null=True, blank=False)
    PostingDate = models.DateTimeField(auto_now_add=True)
    LastUpdationDate = models.DateField(auto_now=True)
    invoice = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def clean(self):
        if self.FromDate and self.ToDate and self.FromDate > self.ToDate:
            raise ValidationError("FromDate cannot be after ToDate.")
    
    def save(self, *args, **kwargs):
        if not self.invoice:  # Generate a unique invoice ID only if it doesn’t exist
            self.invoice = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.BookingNumber} for {self.VehicleId.VehiclesTitle} by {self.user.user.username}"
        
class TempUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    ContactNo = models.CharField(max_length=15)
    dob = models.DateField()
    Country = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Address = models.TextField(max_length=250)  # Changed to TextField for consistency
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)  # Expire after 10 minutes

    def to_user_details(self):
        """Convert TempUser instance to UserDetails."""
        user = User.objects.create_user(
            username=self.email,
            password=self.password,
            first_name=self.fname,
            last_name=self.lname,
        )
        user_details = UserDetails.objects.create(
            user=user,
            ContactNo=self.ContactNo,
            dob=self.dob,
            Country=self.Country,
            City=self.City,
            Address=self.Address
        )
        return user_details

    def __str__(self):
        return f"{self.fname} {self.lname} ({self.email})"