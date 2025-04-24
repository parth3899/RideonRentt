import datetime
import random
import os
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, logout, login
from django.db.models import Q
from django.shortcuts import render, redirect , get_object_or_404
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from .models import *
from datetime import date
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.core.files import File
import uuid
from django.urls import reverse
from .models import Booking , Vehicles
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.crypto import get_random_string
from .forms import  OTPForm, ResetPasswordForm
from .models import Booking
import csv
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import xlsxwriter
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import UserDetails 
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import UserDetails  # Ensure your UserDetails model is imported
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import random
from .models import UserDetails  # Ensure your UserDetails model is imported
from django.core.mail import send_mail
from datetime import date

from django.core.mail import send_mail
from datetime import date
import pandas as pd
from .forms import ExcelUploadForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Booking  # Adjust the import based on your project structure

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from .models import Booking
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.files.base import File
from django.core.files.storage import default_storage
import os, io
from .models import UserDetails, Vehicles, Brands


# Create your views here.





def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            email = request.session.get('otp_email')
            try:
                user = User.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('home')  # Redirect to home page after success
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
    
    form = ResetPasswordForm()  # Initialize the form for GET request
    return render(request, 'user/reset_password.html', {'form': form})


def mybookingDtls(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    try:
        booking = Booking.objects.get(id=pid)
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect('user_bookings')
    
    fd = booking.FromDate
    td = booking.ToDate
    totaldays = (td - fd).days
    grandtotal = int(booking.VehicleId.PricePerDay) * totaldays
    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': grandtotal,
        'item_name': f"Booking for {booking.VehicleId.VehiclesTitle}",
        'invoice': booking.invoice,
        'currency_code': 'INR',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
    }

    context = {
        'booking': booking,
        'totaldays': totaldays,
        'grandtotal': grandtotal,
        'paypal': paypal_checkout,
    }

    return render(request, 'user/mybookingDtls.html', context)

@csrf_exempt
def paypal_ipn(request):
    if request.method == "POST":
        payment_status = request.POST.get('payment_status')
        invoice = request.POST.get('invoice')

        if payment_status == "Completed":
            # Handle successful payment
            booking = Booking.objects.get(invoice=invoice)  # Ensure 'invoice' field exists
            booking.Status = 'Paid'
            booking.save()
            return HttpResponse("Payment processed successfully.", status=200)
        else:
            return HttpResponse("Payment status not completed.", status=400)

    return HttpResponse("Invalid request.", status=400)

def index(request):
    vehicles = Vehicles.objects.all()
    return render(request, 'index.html', {})


def about(request):
    return render(request, 'about.html')


def carlist(request):
    vehicles = Vehicles.objects.filter(is_approved=True)
    brand = Brands.objects.all()
    if request.method == "POST":
        brandid = request.POST['brand']
        fuelType = request.POST['fuelType']

        brands = Brands.objects.get(id=brandid)
        vehicles = Vehicles.objects.filter(
            Q(FuelType=fuelType) & Q(VehiclesBrand=brands) & Q(is_approved=True)
        )
        vehiclescount = vehicles.count()

        return render(request, 'searchcarList.html', locals())
    return render(request, 'carlist.html', locals())


def carDetails(request, pid):
    vehicle = Vehicles.objects.get(id=pid)
    vehicleid = vehicle.id
    vehiclebrand = vehicle.VehiclesBrand
    similarvehicle = Vehicles.objects.filter(~Q(id=vehicleid), VehiclesBrand=vehiclebrand)
    return render(request, 'carDetails.html', locals())


def contact(request):
    error = ""
    if request.method == "POST":
        Name = request.POST['Name']
        EmailId = request.POST['EmailId']
        ContactNo = request.POST['ContactNo']
        Message = request.POST['Message']

        try:
            Contactusquery.objects.create(Name=Name, EmailId=EmailId, ContactNo=ContactNo, Message=Message)
            error = "no"
        except:
            error = "yes"
    return render(request, 'contact.html', locals())


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html', locals())


# SIGNUP VIEW
@csrf_exempt
def signup(request):
    if request.method == "POST":
        fname = request.POST.get('firstName')
        lname = request.POST.get('lastName')
        email = request.POST.get('emailid')
        password = request.POST.get('password')
        cpassword = request.POST.get('confirm_password')
        contact_no = request.POST.get('ContactNo')
        dob = request.POST.get('dob')
        country = request.POST.get('Country') or "USA"
        state = request.POST.get('state')
        city = request.POST.get('City')
        zipcode = request.POST.get('ZipCode')  # Optional if model includes it
        address = request.POST.get('Address')
        license_no = request.POST.get('LicenseNo')
        otp = random.randint(100000, 999999)

        # Check if verified user already exists
        existing_user = User.objects.filter(username=email).first()
        if existing_user:
            try:
                user_details = UserDetails.objects.get(user=existing_user)
                if user_details.is_verified:
                    messages.error(request, "User already exists and is verified. Please log in.")
                    return redirect('user_login')
            except UserDetails.DoesNotExist:
                pass  # allow signup to continue if details are missing

        # Store signup data in session (not creating user yet)
        request.session['signup_data'] = {
            'fname': fname,
            'lname': lname,
            'email': email,
            'password': password,
            'ContactNo': contact_no,
            'dob': dob,
            'Country': country,
            'State': state,
            'City': city,
            'Address': address,
            'LicenseNo': license_no,
            'otp': otp
        }

        try:
            send_mail(
                'Your OTP for Registration',
                f'Your OTP is {otp}',
                'rideonrentt@gmail.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, "OTP sent! Please check your email for verification.")
        except Exception as e:
            messages.error(request, "Failed to send OTP. Please try again.")
            return redirect('signup')

        return redirect('verify_otp')

    return render(request, 'signup.html')



@csrf_exempt
def owner_add_vehicle(request):
    from .models import Brands
    brands = Brands.objects.all()
    error = ""
    otp_verified = request.session.get('otp_verified', False)
    accessories = [
        'AirConditioner', 'PowerDoorLocks', 'AntiLockBrakingSystem', 'BrakeAssist',
        'PowerSteering', 'DriverAirbag', 'PassengerAirbag', 'PowerWindows',
        'CDPlayer', 'CentralLocking', 'CrashSensor', 'LeatherSeats'
    ]

    if request.method == "POST":
        # Step 1: Get Owner info
        fname = request.POST.get('firstName')
        lname = request.POST.get('lastName')
        email = request.POST.get('emailid')
        contact_no = request.POST.get('ContactNo')
        dob = request.POST.get('dob')
        country = request.POST.get('Country', 'USA')
        state = request.POST.get('State')
        city = request.POST.get('City')
        zipcode = request.POST.get('ZipCode')
        address = request.POST.get('Address')

        # Step 2: Car Info
        vehicles_title = request.POST.get('VehiclesTitle')
        vehicles_brand_id = request.POST.get('VehiclesBrand')
        vehicles_overview = request.POST.get('VehiclesOverview')
        price_per_day = request.POST.get('PricePerDay')
        fuel_type = request.POST.get('FuelType')
        model_year = request.POST.get('ModelYear')
        seating_capacity = request.POST.get('SeatingCapacity')
        selected_accessories = {acc: request.POST.get(acc) == 'yes' for acc in accessories}

        # Step 3: Save uploaded images to temp location
        uploaded_images = {}
        for i in range(1, 6):
            image_field = f'Vimage{i}'
            file = request.FILES.get(image_field)
            if file:
                temp_path = f'temp/{file.name}'
                saved_path = default_storage.save(temp_path, file)
                uploaded_images[image_field] = saved_path

        # Step 4: Save data in session
        otp = random.randint(100000, 999999)
        request.session['owner_signup_data'] = {
            'firstName': fname,
            'lastName': lname,
            'emailid': email,
            'ContactNo': contact_no,
            'dob': dob,
            'Country': country,
            'State': state,
            'City': city,
            'ZipCode': zipcode,
            'Address': address,
            'otp': otp,
            'is_owner': True
        }
        request.session['car_data'] = {
            'VehiclesTitle': vehicles_title,
            'VehiclesBrand': vehicles_brand_id,
            'VehiclesOverview': vehicles_overview,
            'PricePerDay': price_per_day,
            'FuelType': fuel_type,
            'ModelYear': model_year,
            'SeatingCapacity': seating_capacity,
            'Accessories': selected_accessories
        }
        request.session['uploaded_images'] = uploaded_images

        # Step 5: Send OTP
        try:
            send_mail(
                'Your OTP for Registration',
                f'Your OTP is {otp}',
                'rideonrentt@gmail.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, "OTP sent to your email!")
        except Exception as e:
            messages.error(request, f"Failed to send OTP: {e}")
            return redirect('owner_add_vehicle')

        return redirect('verify_otp')

    return render(request, 'owner_add_vehicle.html', {
        'brands': brands,
        'accessories': accessories,
        'otp_verified': otp_verified,
        'error': error
    })




def verify_otp(request):
    error = ""
    email = None

    if request.method == "POST":
        input_otp = request.POST.get('otp')

        # Detect whether it's an owner or regular user flow
        session_data = request.session.get('owner_signup_data') or request.session.get('signup_data')
        car_data = request.session.get('car_data', {})
        uploaded_images = request.session.get('uploaded_images', {})
        is_owner_flow = 'owner_signup_data' in request.session

        if session_data:
            generated_otp = session_data.get('otp')
            email = session_data.get('emailid') or session_data.get('email')

            if input_otp and input_otp.isdigit() and int(input_otp) == int(generated_otp):
                if User.objects.filter(username=email).exists():
                    messages.error(request, "User already exists. Please log in.")
                    return redirect('user_login')

                # ✅ Create user
                user = User.objects.create_user(
                    username=email,
                    password=session_data.get('password', ''),  # Blank for owner, present for user
                    first_name=session_data.get('firstName') or session_data.get('fname'),
                    last_name=session_data.get('lastName') or session_data.get('lname')
                )

                # ✅ Create user profile
                UserDetails.objects.create(
                    user=user,
                    ContactNo=session_data.get('ContactNo'),
                    dob=session_data.get('dob'),
                    Country=session_data.get('Country'),
                    state = session_data.get('state') or "Tennessee",
                    City=session_data.get('City'),
                    Address=session_data.get('Address'),
                    is_verified=True,
                    is_owner=is_owner_flow,
                    license_no=session_data.get('LicenseNo') if not is_owner_flow else None
                )

                # ✅ If owner: create vehicle and attach uploaded images
                if is_owner_flow:
                    try:
                        brand = Brands.objects.get(id=car_data['VehiclesBrand'])

                        vehicle = Vehicles(
                            VehiclesTitle=car_data['VehiclesTitle'],
                            VehiclesBrand=brand,
                            VehiclesOverview=car_data['VehiclesOverview'],
                            PricePerDay=car_data['PricePerDay'],
                            FuelType=car_data['FuelType'],
                            ModelYear=car_data['ModelYear'],
                            SeatingCapacity=car_data['SeatingCapacity'],
                            **{k: v for k, v in car_data['Accessories'].items()}
                        )
                        vehicle.user = user

                        # Attach uploaded images
                        for i in range(1, 6):
                            image_field = f'Vimage{i}'
                            path = uploaded_images.get(image_field)
                            if path and default_storage.exists(path):
                                with default_storage.open(path, 'rb') as f:
                                    content = f.read()
                                    setattr(vehicle, image_field, File(io.BytesIO(content), name=os.path.basename(path)))

                        vehicle.save()

                        # Notify admin
                        send_mail(
                            subject='New Vehicle Listing Submitted',
                            message=f"A new vehicle titled '{vehicle.VehiclesTitle}' was submitted by {user.first_name} {user.last_name} ({user.username}).",
                            from_email='rideonrentt2407@gmail.com',
                            recipient_list=['rideonrentt2407@gmail.com'],
                            fail_silently=False,
                        )

                        # Clean up uploaded temp files
                        for path in uploaded_images.values():
                            if default_storage.exists(path):
                                default_storage.delete(path)

                    except Exception as e:
                        messages.error(request, f"Error while saving vehicle: {e}")
                        return redirect('owner_add_vehicle')

                # ✅ Cleanup sessions
                for key in ['signup_data', 'owner_signup_data', 'car_data', 'uploaded_images']:
                    request.session.pop(key, None)

                messages.success(request, "Registration complete!" if not is_owner_flow else "Owner & vehicle submitted for approval!")
                return redirect('user_login' if not is_owner_flow else 'thankyou')

            else:
                messages.error(request, "Invalid OTP. Please try again.")
        else:
            messages.error(request, "Session expired. Please register again.")
            return redirect('signup' if not is_owner_flow else 'owner_add_vehicle')

    return render(request, 'email_verification.html', {'error': error, 'email': email})


def user_login(request):
    error = ""
    if request.method == 'POST':
        e = request.POST['emailid']
        p = request.POST['password']
        user = authenticate(username=e, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'user_login.html', locals())



def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    from django.db.models import Count

    stats = {
        'totaluser': UserDetails.objects.count(),
        'totalbooking': Booking.objects.count(),
        'totalbrand': Brands.objects.count(),
        'totalvehicle': Vehicles.objects.count(),
        'totalunread': Contactusquery.objects.filter(Status=None).count(),
        'totalread': Contactusquery.objects.filter(Status='yes').count()
    }
    return render(request, 'admin/dashboard.html', stats)

def brands(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    brand = Brands.objects.all()
    error = ""
    if request.method == "POST":
        BrandName = request.POST['BrandName']
        try:
            Brands.objects.create(BrandName=BrandName)
            error = "no"
        except:
            error = "yes"
    return render(request, 'admin/brands.html', {'brand': brand, 'error': error})

def editBrand(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    brand = Brands.objects.get(id=pid)
    error = ""
    if request.method == "POST":
        BrandName = request.POST['BrandName']
        brand.BrandName = BrandName
        try:
            brand.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'admin/editBrand.html', {'brand': brand, 'error': error})

def deleteBrand(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    Brands.objects.filter(id=pid).delete()
    return redirect('brands')

def addVehicle(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    brands = Brands.objects.all()
    error = ""
    if request.method == "POST":
        try:
            brandid = request.POST['VehiclesBrand']
            brandsid = Brands.objects.get(id=brandid)

            vehicle_data = {
                'VehiclesBrand': brandsid,
                'VehiclesTitle': request.POST['VehiclesTitle'],
                'VehiclesOverview': request.POST['VehiclesOverview'],
                'PricePerDay': request.POST['PricePerDay'],
                'FuelType': request.POST['FuelType'],
                'ModelYear': request.POST['ModelYear'],
                'SeatingCapacity': request.POST['SeatingCapacity'],
                'Vimage1': request.FILES.get('Vimage1'),
                'Vimage2': request.FILES.get('Vimage2'),
                'Vimage3': request.FILES.get('Vimage3'),
                'Vimage4': request.FILES.get('Vimage4'),
                'Vimage5': request.FILES.get('Vimage5'),
                'AirConditioner': request.POST.get('AirConditioner', 'yes') == 'yes',
                'PowerDoorLocks': request.POST.get('PowerDoorLocks', 'yes') == 'yes',
                'AntiLockBrakingSystem': request.POST.get('AntiLockBrakingSystem', 'yes') == 'yes',
                'BrakeAssist': request.POST.get('BrakeAssist', 'yes') == 'yes',
                'PowerSteering': request.POST.get('PowerSteering', 'yes') == 'yes',
                'DriverAirbag': request.POST.get('DriverAirbag', 'yes') == 'yes',
                'PassengerAirbag': request.POST.get('PassengerAirbag', 'yes') == 'yes',
                'PowerWindows': request.POST.get('PowerWindows', 'yes') == 'yes',
                'CDPlayer': request.POST.get('CDPlayer', 'yes') == 'yes',
                'CentralLocking': request.POST.get('CentralLocking', 'yes') == 'yes',
                'CrashSensor': request.POST.get('CrashSensor', 'yes') == 'yes',
                'LeatherSeats': request.POST.get('LeatherSeats', 'yes') == 'yes',
                'is_approved' : True,

            }

            Vehicles.objects.create(**vehicle_data)
            error = "no"
        except Exception as e:
            print("Error in vehicle creation:", e)
            error = "yes"
    return render(request, 'admin/addVehicle.html', {'brands': brands, 'error': error})

def manageVehicle(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    vehicle = Vehicles.objects.select_related('VehiclesBrand').all()
    return render(request, 'admin/manageVehicle.html', {'vehicle': vehicle})


def editVehicle(request, pid):
    brands = Brands.objects.all()
    vehicle = Vehicles.objects.get(id=pid)
    error = ""

    if request.method == "POST":
        try:
            # Brand and basic details
            brandid = request.POST['VehiclesBrand']
            brandsid = Brands.objects.get(id=brandid)

            vehicle.VehiclesBrand = brandsid
            vehicle.VehiclesTitle = request.POST['VehiclesTitle']
            vehicle.VehiclesOverview = request.POST['VehiclesOverview']
            vehicle.PricePerDay = float(request.POST['PricePerDay'])
            vehicle.FuelType = request.POST['FuelType']
            vehicle.ModelYear = request.POST['ModelYear']
            vehicle.SeatingCapacity = request.POST['SeatingCapacity']

            # Convert checkbox input to boolean
            def get_checkbox(name):
                return request.POST.get(name) == 'yes'

            vehicle.AirConditioner = get_checkbox('AirConditioner')
            vehicle.PowerDoorLocks = get_checkbox('PowerDoorLocks')
            vehicle.AntiLockBrakingSystem = get_checkbox('AntiLockBrakingSystem')
            vehicle.BrakeAssist = get_checkbox('BrakeAssist')
            vehicle.PowerSteering = get_checkbox('PowerSteering')
            vehicle.DriverAirbag = get_checkbox('DriverAirbag')
            vehicle.PassengerAirbag = get_checkbox('PassengerAirbag')
            vehicle.PowerWindows = get_checkbox('PowerWindows')
            vehicle.CDPlayer = get_checkbox('CDPlayer')
            vehicle.CentralLocking = get_checkbox('CentralLocking')
            vehicle.CrashSensor = get_checkbox('CrashSensor')
            vehicle.LeatherSeats = get_checkbox('LeatherSeats')

            # Handle image replacements (only if new ones uploaded)
            for i in range(1, 6):
                image_field = f'Vimage{i}'
                if image_field in request.FILES:
                    setattr(vehicle, image_field, request.FILES[image_field])

            # Handle approval or decline
            approve = request.POST.get('approve_status') == 'approve'
            decline = request.POST.get('decline_status') == 'decline'

            if approve:
                vehicle.is_approved = True
            elif decline:
                vehicle.is_approved = False

            vehicle.UpdationDate = date.today()
            vehicle.save()

            # Send email based on action
            user_email = vehicle.user.username  # assuming `vehicle.user` exists
            vehicle_name = vehicle.VehiclesTitle

            if approve:
                send_mail(
                    'Vehicle Approved',
                    f'Your vehicle "{vehicle_name}" has been approved and is now live on RideOnRent.',
                    'rideonrentt@gmail.com',
                    [user_email],
                    fail_silently=False
                )
            elif decline:
                send_mail(
                    'Vehicle Declined',
                    f'Your vehicle "{vehicle_name}" was reviewed but unfortunately has been declined by the admin. Please contact support for more details.',
                    'rideonrentt@gmail.com',
                    [user_email],
                    fail_silently=False
                )

            error = "no"

        except Exception as e:
            print("Error during vehicle update:", e)
            error = "yes"

    return render(request, 'admin/editVehicle.html', {
        'brands': brands,
        'vehicle': vehicle,
        'error': error
    })


    



# from django.shortcuts import get_object_or_404

def deleteVehicle(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    # Use get_object_or_404 to handle the case where the vehicle does not exist
    vehicle = get_object_or_404(Vehicles, id=pid)
    vehicle.delete()
    return redirect('vehicles')

def newBooking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    booking = Booking.objects.filter(Status__isnull=True)
    return render(request, 'admin/newBooking.html', locals())


def confirmBooking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    booking = Booking.objects.filter(Status='Confirm')
    return render(request, 'admin/confirmBooking.html', locals())


def cancelBooking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    booking = Booking.objects.filter(Status='Cancel')
    return render(request, 'admin/cancelBooking.html', locals())


def allBooking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    booking = Booking.objects.all()
    return render(request, 'admin/allBooking.html', locals())




def fake_payment(request, booking_id):
    # Get the booking object or return a 404 error if not found
    booking = get_object_or_404(Booking, id=booking_id)

    # Calculate total days and grand total
    total_days = (booking.ToDate - booking.FromDate).days
    grand_total = total_days * booking.VehicleId.PricePerDay  # Assuming VehicleId has a PricePerDay attribute

    if request.method == "POST":
        # Check if the payment method is valid (you can add more validation as needed)
        payment_method = request.POST.get('payment_method')
        if payment_method:
            # Update the booking status
            booking.PaymentStatus = "Paid"
            #booking.Status = "Payment Completed"  # Assuming you want to update the booking status as well
            booking.save()  # Save the changes to the database

            # Prepare email details
            user_subject = "Payment Receipt"
            admin_subject = "New Payment Received"

            # Render HTML for user email
            user_message = render_to_string('user/payment_receipt.html', {
                'user': request.user,
                'booking': booking,
                'total_amount': grand_total,
            })

            # Render HTML for admin email
            admin_message = render_to_string('user/admin_notification.html', {
                'user': request.user,
                'booking': booking,
                'total_amount': grand_total,
            })

            # Send emails
            user_email = EmailMultiAlternatives(
                subject=user_subject,
                body='This is a fallback message if HTML is not supported.',
                from_email=settings.EMAIL_HOST_USER,
                to=[request.user.email]
            )
            user_email.attach_alternative(user_message, 'text/html')  # Attach HTML content
            user_email.send()

            admin_email = EmailMultiAlternatives(
                subject=admin_subject,
                body='This is a fallback message if HTML is not supported.',
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.ADMIN_EMAIL]  # Make sure ADMIN_EMAIL is set in your settings
            )
            admin_email.attach_alternative(admin_message, 'text/html')  # Attach HTML content
            admin_email.send()

            messages.success(request, "Payment completed successfully! A confirmation email has been sent.")
            return redirect('mybookingDtls', pid=booking.id)  # Redirect to booking details page
        else:
            messages.error(request, "Please select a valid payment method.")  # Handle no payment method selected

    # Render the payment page with additional context
    context = {
        'booking': booking,
        'total_days': total_days,
        'grand_total': grand_total,
        'user': request.user,  # Pass the user information
    }
    return render(request, 'fake_payment.html', context)



def viewBooking(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    bookingDtls = Booking.objects.get(id=pid)
    fd = bookingDtls.FromDate
    td = bookingDtls.ToDate
    totaldays = td - fd
    totaldays = str(totaldays)[0:1]
    grandtotal = int(bookingDtls.VehicleId.PricePerDay) * int(totaldays)
    error = ""

    if request.method == "POST":
        Status = request.POST['Status']
        bookingDtls.Status = Status
        bookingDtls.LastUpdationDate = date.today()

        try:
            bookingDtls.save()

            # Send email based on the booking status
            user_email = bookingDtls.user.user.username
            vehicle_name = bookingDtls.VehicleId.VehiclesTitle
            booking_number = bookingDtls.BookingNumber

            if Status == 'Confirm':
                # Send confirmation email
                send_mail(
                    'Booking Confirmed',
                    f'Your booking for the vehicle {vehicle_name} has been confirmed. Your booking number is {booking_number}.',
                    'rideonrentt@gmail.com',  # Replace with your sender email
                    [user_email],
                    fail_silently=False,
                )
            elif Status == 'Cancel':
                # Send cancellation email
                send_mail(
                    'Booking Cancelled',
                    f'Your booking for the vehicle {vehicle_name} has been canceled. Your booking number was {booking_number}.',
                    'rideonrentt@gmail.com',  # Replace with your sender email
                    [user_email],
                    fail_silently=False,
                )
            

            error = "no"
        except:
            error = "yes"
    
    return render(request, 'admin/viewBooking.html', locals())



def deleteBooking(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    booking = Booking.objects.get(id=pid)
    booking.delete()
    return redirect('allBooking')


def unreadQuery(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact = Contactusquery.objects.filter(Status__isnull=True)
    return render(request, 'admin/unreadQuery.html', locals())


def readQuery(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact = Contactusquery.objects.filter(Status='yes')
    return render(request, 'admin/readQuery.html', locals())


def viewQuery(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contacts = Contactusquery.objects.get(id=pid)
    contacts.Status = "yes"
    contacts.save()
    return render(request, 'admin/viewQuery.html', locals())


def deleteQuery(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contacts = Contactusquery.objects.get(id=pid)
    contacts.delete()
    return redirect('readQuery')


def regUser(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    userDtls = UserDetails.objects.all()
    return render(request, 'admin/regUser.html', locals())

def search(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method=='POST':
        sd = request.POST['searchdata']
    try:
        booking = Booking.objects.filter(Q(BookingNumber=sd))
    except:
        booking = ""
    return render(request, 'admin/search.html', locals())

def betweendateReport(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == 'POST':
        fd = request.POST['fromDate']
        td = request.POST['toDate']

        booking = Booking.objects.filter(Q(PostingDate__gte=fd) & Q(PostingDate__lte=td))
        return render(request, 'admin/betweendateReportDtls.html', locals())
    return render(request, 'admin/betweendateReport.html', locals())


def deleteUser(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    User.objects.get(id=pid).delete()
    return redirect('regUser')


def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'admin/changePassword.html', locals())


def Logout(request):
    logout(request)
    return redirect('index')


def Owner_Page(request):
    
    return render(request, 'thankyou.html')


def userindex(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    vehicle = Vehicles.objects.all()
    return render(request, 'user/userindex.html', locals())


def vehicleDetails(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')

    vehicle = Vehicles.objects.get(id=pid)
    vehiclebrand = vehicle.VehiclesBrand
    similarvehicle = Vehicles.objects.filter(~Q(id=vehicle.id), VehiclesBrand=vehiclebrand)

    users = request.user  # No need to fetch user again

    try:
        userdtls = UserDetails.objects.get(user=users)
    except UserDetails.DoesNotExist:
        userdtls = None  # Or handle it appropriately (e.g., redirect or show warning)

    error = None
    bookingNo = None

    if request.method == "POST":
        FromDate = request.POST['FromDate']
        ToDate = request.POST['ToDate']
        message = request.POST['message']
        bookingNo = str(random.randint(10000000, 99999999))

        # Check for date conflict (without matching BookingNumber)
        overlapping_bookings = Booking.objects.filter(
            VehicleId=vehicle,
            FromDate__lte=ToDate,
            ToDate__gte=FromDate
        ).exists()

        if overlapping_bookings:
            error = "date_unavailable"
        else:
            try:
                booking = Booking.objects.create(
                    user=userdtls,
                    VehicleId=vehicle,
                    FromDate=FromDate,
                    ToDate=ToDate,
                    message=message,
                    BookingNumber=bookingNo
                )
                error = "no"
                # Send email only if booking was Initiated.
                # Prepare email details
                vehicle_name = vehicle.VehiclesTitle
                email_subject = 'Booking Initiated - RideOnRent'

                email_plain = f"""Booking Initiated! Your Booking Number is {bookingNo}.

                Vehicle: {vehicle_name}
                From: {FromDate}
                To: {ToDate}

                The booking status is currently *Pending*. You can check the status in the "My Booking" section.
                Once it is confirmed, you will be able to make the payment.

                Thank you for choosing RideOnRent!
                """

                email_html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2>Booking Successful!</h2>
                    <p><strong>Your Booking Number:</strong> {bookingNo}</p>

                    <p><strong>Vehicle:</strong> {vehicle_name}<br>
                    <strong>From:</strong> {FromDate}<br>
                    <strong>To:</strong> {ToDate}</p>

                    <p>The booking status is currently <strong>Pending</strong>. You can check the status in the <em>"My Booking"</em> section.<br>
                    Once it is confirmed, you will be able to make the payment.</p>

                    <p>Thank you for choosing <strong>RideOnRent</strong>!</p>
                </body>
                </html>
                """

                user_email = users.username  # Or use users.email if applicable

                send_mail(
                    subject=email_subject,
                    message=email_plain,
                    from_email='rideonrentt@gmail.com',
                    recipient_list=[user_email],
                    fail_silently=False,
                    html_message=email_html  # This is what Gmail will use
                )
            except Exception as e:
                print(f"Error creating booking: {e}")
                error = "yes"
        

        return render(request, 'user/vehicleDetails.html', {
            'vehicle': vehicle,
            'similarvehicle': similarvehicle,
            'error': error,
            'bookingNo': bookingNo
        })

    # GET request
    return render(request, 'user/vehicleDetails.html', {
        'vehicle': vehicle,
        'similarvehicle': similarvehicle,
        'error': error
    })


def userabout(request):
    return render(request, 'user/userabout.html')


def usercarlist(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    users = request.user  # No need to fetch user again
    vehicles = Vehicles.objects.all()
    brand = Brands.objects.all()
    if request.method == "POST":
        brandid = request.POST['brand']
        fuelType = request.POST['fuelType']

        brands = Brands.objects.get(id=brandid)
        vehicles = Vehicles.objects.filter(Q(FuelType=fuelType) & Q(VehiclesBrand=brands))
        vehiclescount = Vehicles.objects.filter(Q(FuelType=fuelType) & Q(VehiclesBrand=brands)).count()
        return render(request, 'user/searchCarList.html', locals())
    return render(request, 'user/usercarlist.html', locals())


def myProfile(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    user = request.user  # More efficient than querying by ID

    try:
        userDtls = UserDetails.objects.get(user=user)
    except UserDetails.DoesNotExist:
        # Option 1: Redirect to profile creation form
        # return redirect('create_profile')  # You can create this view if needed

        # Option 2: Auto-create empty UserDetails (safer with on-site forms)
        userDtls = UserDetails.objects.create(user=user)
    
    error = ""

    if request.method == "POST":
        fname = request.POST.get('firstName')
        lname = request.POST.get('lastName')
        ContactNo = request.POST.get('ContactNo')
        dob = request.POST.get('dob')
        Country = request.POST.get('Country')
        City = request.POST.get('City')
        Address = request.POST.get('Address')

        user.first_name = fname
        user.last_name = lname
        userDtls.ContactNo = ContactNo
        userDtls.dob = dob
        userDtls.Country = Country
        userDtls.City = City
        userDtls.Address = Address

        try:
            userDtls.save()
            user.save()
            error = "no"
        except Exception as e:
            print("Error saving profile:", e)
            error = "yes"

    return render(request, 'user/myProfile.html', locals())

def myBooking(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    if request.user.is_superuser:
        # Superuser can view all bookings
        booking = Booking.objects.all()
        return render(request, 'admin/allBooking.html', {
            'booking': booking
        })   

    try:
        userDtls = UserDetails.objects.get(user=request.user)
        booking = Booking.objects.filter(user=userDtls)
    except UserDetails.DoesNotExist:
        booking = []
        # Optional: Log this or inform the user to complete their profile

    return render(request, 'user/myBooking.html', {
        'booking': booking
    })





def mychangePassword(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'user/mychangePassword.html', locals())


def my_booking(request):
    bookings = Booking.objects.filter(user=request.user)  # Assuming user-based filtering
    context = {
        'booking': bookings
    }
    return render(request, 'user/mybooking.html', context)

def updateBooking(request, booking_id):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    booking = get_object_or_404(Booking, id=booking_id)
    vehicle = booking.VehicleId  # Get the vehicle related to the booking

    if request.method == 'POST':
        # Get updated data from form submission
        new_from_date = request.POST.get('from_date')
        new_to_date = request.POST.get('to_date')

        # Ensure no other booking exists for the same car in the new date range
        conflicting_bookings = Booking.objects.filter(
            VehicleId=vehicle,
            FromDate__lte=new_to_date,
            ToDate__gte=new_from_date
        ).exclude(id=booking.id)  # Exclude the current booking

        if conflicting_bookings.exists():
            messages.error(request, "This vehicle is already booked for the selected dates. Please choose a different date range.")
        else:
            # Update booking details
            booking.FromDate = new_from_date
            booking.ToDate = new_to_date
            booking.Status = 'Updated'
            booking.save()
            messages.success(request, "Booking updated successfully.")
            return redirect('myBooking')

    # Initial form pre-filled with current booking details
    context = {
        'booking': booking,
        'vehicle': vehicle,
    }
    return render(request, 'user/update_booking.html', context)

def deleteBooking(request, booking_id):
    if not request.user.is_authenticated:
        return redirect('user_login')

   
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':

        booking.delete()
        messages.success(request, 'Booking deleted successfully!')
        return redirect('myBooking')

    return render(request, 'user/delete_booking.html', {'booking': booking})

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_conditions(request):
    return render(request, 'terms_conditions.html')

def registration(request):
    return render(request, 'registration.html')

def affiliate_program(request):
    return render(request, 'affiliate_program.html')

def return_refund(request):
    return render(request, 'return_refund.html')

def help_faq(request):
    return render(request, 'help_faq.html')



# View to handle Excel file upload
from django.utils.dateparse import parse_date

def upload_vehicle_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)

            # Print the column names for debugging
            print("Columns in the uploaded Excel file:", df.columns.tolist())

            for index, row in df.iterrows():
                # Convert dates to the correct format
                reg_date = str(row['RegDate']) if pd.notnull(row['RegDate']) else None
                updation_date = str(row['UpdationDate']) if pd.notnull(row['UpdationDate']) else None
                
                # Print the dates for debugging
                print(f"RegDate: {reg_date}, UpdationDate: {updation_date}")

                # Create the Vehicles instance using the correct field names
                vehicle = Vehicles(
                    VehiclesTitle=row['VehiclesTitle'],
                    VehiclesBrand_id=row['VehiclesBrand_id'],  # Make sure this matches your foreign key field
                    VehiclesOverview=row['VehiclesOverview'],
                    PricePerDay=row['PricePerDay'],
                    FuelType=row['FuelType'],
                    ModelYear=row['ModelYear'],
                    SeatingCapacity=row['SeatingCapacity'],
                    Vimage1=row['Vimage1'],
                    Vimage2=row['Vimage2'],
                    Vimage3=row['Vimage3'],
                    Vimage4=row['Vimage4'],
                    Vimage5=row['Vimage5'],
                    AirConditioner=row['AirConditioner'],
                    RegDate=reg_date,  # Ensure the date is in the correct format
                    UpdationDate=updation_date  # Ensure the date is in the correct format
                )
                vehicle.save()

            messages.success(request, 'Vehicles uploaded successfully!')
            return redirect('manageVehicle')
    else:
        form = ExcelUploadForm()
    
    return render(request, 'admin/upload_vehicle.html', {'form': form})




# View to download vehicles data as Excel
def download_vehicle_excel(request):
    # Fetch vehicles data
    vehicles = Vehicles.objects.all().values()

    # Create a DataFrame
    df = pd.DataFrame(list(vehicles))

    # Debugging: Print out the DataFrame column types
    print("DataFrame Column Types:")
    print(df.dtypes)

    # Convert any datetime columns to timezone-naive
    for column in df.select_dtypes(include=['datetime64[ns, UTC]', 'datetime64[ns]']):
        df[column] = df[column].dt.tz_localize(None)  # Make it timezone-naive

    # Debugging: Print out the modified DataFrame
    print("Modified DataFrame:")
    print(df)

    # Create an Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=vehicles.xlsx'

    # Use Pandas to write the DataFrame to the response
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Vehicles', index=False)

    return response