from django.test import TestCase
from .models import Brands, Vehicles, UserDetails, Booking

class BrandsModelTest(TestCase):
    def setUp(self):
        self.brand = Brands.objects.create(
            brand_name='Toyota',
            brand_logo='path/to/logo.png'
        )
    
    def test_brand_creation(self):
        self.assertTrue(isinstance(self.brand, Brands))
        self.assertEqual(self.brand.__str__(), self.brand.brand_name)

class VehiclesModelTest(TestCase):
    def setUp(self):
        self.vehicle = Vehicles.objects.create(
            vehicle_model='Camry',
            vehicle_brand='Toyota',
            vehicle_price_per_day=100.00,
            vehicle_description='A comfortable sedan',
            vehicle_image='path/to/image.png'
        )
    
    def test_vehicle_creation(self):
        self.assertTrue(isinstance(self.vehicle, Vehicles))
        self.assertEqual(self.vehicle.__str__(), self.vehicle.vehicle_model)

class UserDetailsModelTest(TestCase):
    def setUp(self):
        self.user = UserDetails.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='securepassword',
            phone_number='1234567890',
            address='123 Test St',
            city='Test City',
            state='TS',
            zip_code='12345'
        )
    
    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, UserDetails))
        self.assertEqual(self.user.__str__(), self.user.username)

class BookingModelTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date='2024-08-01',
            end_date='2024-08-10',
            total_amount=1000.00
        )
    
    def test_booking_creation(self):
        self.assertTrue(isinstance(self.booking, Booking))
        self.assertEqual(self.booking.__str__(), f'{self.booking.user.username} - {self.booking.vehicle.vehicle_model}')
