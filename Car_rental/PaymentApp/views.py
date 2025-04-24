from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from .models import Booking
import uuid
from django.views.decorators.csrf import csrf_exempt

def mybookingDtls(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')

    # Retrieve the booking safely
    booking = get_object_or_404(Booking, id=pid)

    fd = booking.FromDate
    td = booking.ToDate

    # Ensure total days is at least 1
    totaldays = max((td - fd).days, 1)
    grandtotal = int(booking.VehicleId.PricePerDay) * totaldays
    host = request.get_host()

    # PayPal checkout setup
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': grandtotal,
        'item_name': f"Booking for {booking.VehicleId.VehiclesTitle}",
        'invoice': str(uuid.uuid4()),  # Unique invoice identifier
        'currency_code': 'INR',  # Correct currency code
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",  # IPN URL
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'booking': booking,
        'totaldays': totaldays,
        'grandtotal': grandtotal,
        'paypal': paypal_payment,
    }

    return render(request, 'user/mybookingDtls.html', context)

def paymentSuccessful(request, booking_id):
    # Retrieve booking details based on booking_id
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Update the booking status to 'Paid'
    booking.Status = 'Paid'
    booking.save()

    messages.success(request, f"Payment successful! Your booking for {booking.VehicleId.VehiclesTitle} is confirmed.")
    
    return render(request, 'payment-success.html', {'booking': booking})

def paymentFailed(request, booking_id):
    # Retrieve booking details based on booking_id
    booking = get_object_or_404(Booking, id=booking_id)
    
    messages.error(request, "Payment failed. Please try again.")
    
    return render(request, 'payment-failed.html', {'booking': booking})

@csrf_exempt
def paypal_ipn(request):
    if request.method == "POST":
        payment_status = request.POST.get('payment_status')
        invoice = request.POST.get('invoice')

        if payment_status == "Completed":
            # Update the booking status using the invoice
            booking = get_object_or_404(Booking, invoice=invoice)  # Ensure 'invoice' field exists in your Booking model
            booking.Status = 'Paid'
            booking.save()
            return HttpResponse("Payment processed successfully.", status=200)
        else:
            return HttpResponse("Payment status not completed.", status=400)

    return HttpResponse("Invalid request.", status=400)
