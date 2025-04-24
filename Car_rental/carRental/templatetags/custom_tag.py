from django import template
from carRental.models import Booking  # Import Booking model

register = template.Library()

@register.filter(name='notification')
def notification(obj):
    # If `obj` is not used for filtering, this function could be simplified or removed.
    # If `obj` is used for filtering based on the object, make sure to implement the filter logic.
    booking = Booking.objects.filter(Status=None)  # Use 'Status' as defined in the model
    return booking

@register.simple_tag()
def notificationcount():
    # Count bookings where Status is None
    bookingcount = Booking.objects.filter(Status=None).count()  # Use 'Status' as defined in the model
    return bookingcount
