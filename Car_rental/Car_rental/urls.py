from django.contrib import admin
from django.urls import path, include
from carRental.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about', about, name='about'),
    path('carlist', carlist, name='carlist'),
    path('vehicles/', manageVehicle, name='vehicles'),  # Define the 'vehicles' URL here
    path('carDetails/<int:pid>', carDetails, name='carDetails'),
    path('contact', contact, name='contact'),
    path('admin_login', admin_login, name='admin_login'),
    path('user_login', user_login, name='user_login'),
    path('owner_add_vehicle', owner_add_vehicle, name='owner_add_vehicle'),
    path('signup', signup, name='signup'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('dashboard/', dashboard, name='dashboard'),
    path('brands', brands, name='brands'),
    path('editBrand/<int:pid>', editBrand, name='editBrand'),
    path('deleteBrand/<int:pid>', deleteBrand, name='deleteBrand'),
    path('addVehicle', addVehicle, name='addVehicle'),
    path('manageVehicle', manageVehicle, name='manageVehicle'),  # This could also be a candidate for the 'vehicles' URL
    path('thankyou/', Owner_Page, name='thankyou'),
    path('editVehicle/<int:pid>', editVehicle, name='editVehicle'),
    path('deleteVehicle/<int:pid>', deleteVehicle, name='deleteVehicle'),
    path('newBooking', newBooking, name='newBooking'),
    path('confirmBooking', confirmBooking, name='confirmBooking'),
    path('cancelBooking', cancelBooking, name='cancelBooking'),
    path('allBooking', allBooking, name='allBooking'),
    path('deleteBooking/<int:pid>', deleteBooking, name='deleteBooking'),
    path('viewBooking/<int:pid>', viewBooking, name='viewBooking'),
    path('unreadQuery', unreadQuery, name='unreadQuery'),
    path('readQuery', readQuery, name='readQuery'),
    path('viewQuery/<int:pid>', viewQuery, name='viewQuery'),
    path('deleteQuery/<int:pid>', deleteQuery, name='deleteQuery'),
    path('regUser', regUser, name='regUser'),
    path('search', search, name='search'),
    path('betweendateReport', betweendateReport, name='betweendateReport'),
    path('deleteUser/<int:pid>', deleteUser, name='deleteUser'),
    path('changePassword', changePassword, name='changePassword'),
    path('logout/', Logout, name='logout'),

    # User routes
    path('userindex', userindex, name='userindex'),
    path('vehicleDetails/<int:pid>', vehicleDetails, name='vehicleDetails'),
    path('userabout', userabout, name='userabout'),
    path('usercarlist', usercarlist, name='usercarlist'),
    path('myProfile', myProfile, name='myProfile'),
    path('myBooking/', myBooking, name='myBooking'),
    path('mybookingDtls/<int:pid>', mybookingDtls, name='mybookingDtls'),
    path('mychangePassword', mychangePassword, name='mychangePassword'),

    # Booking update and delete routes
    path('myBooking/update/<int:booking_id>/', updateBooking, name='updateBooking'),
    path('myBooking/delete/<int:booking_id>/', deleteBooking, name='deleteBooking'),

    # PayPal integration routes
    path('paypal-ipn/', paypal_ipn, name='paypal-ipn'),
    path('fake-payment/<int:booking_id>/', fake_payment, name='fake_payment'),

    # Password management
    path('upload_vehicle_excel/', upload_vehicle_excel, name='upload_vehicle_excel'),
    path('download_vehicle_excel/', download_vehicle_excel, name='download_vehicle_excel'),

    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-conditions/', terms_conditions, name='terms_conditions'),
    path('registration/', registration, name='registration'),
    path('affiliate-program/', affiliate_program, name='affiliate_program'),
    path('return-refund/', return_refund, name='return_refund'),
    path('help-faq/', help_faq, name='help_faq'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
