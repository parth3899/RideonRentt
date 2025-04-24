from django.contrib import admin
from .models import Brands, Vehicles, UserDetails, Booking, Contactusinfo, Contactusquery

@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ('BrandName', 'Creationdate', 'UpdationDate')
    search_fields = ('BrandName',)

@admin.register(Vehicles)
class VehiclesAdmin(admin.ModelAdmin):
    list_display = ('VehiclesTitle', 'VehiclesBrand', 'PricePerDay', 'ModelYear', 'SeatingCapacity', 'FuelType')
    list_filter = ('VehiclesBrand', 'FuelType', 'ModelYear')
    search_fields = ('VehiclesTitle', 'VehiclesBrand__BrandName')

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'ContactNo', 'Address')
    search_fields = ('user__username', 'ContactNo')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('VehicleId', 'user', 'FromDate', 'ToDate', 'Status')
    list_filter = ('Status', 'FromDate', 'ToDate')
    search_fields = ('user__user__username', 'VehicleId__VehiclesTitle')

@admin.register(Contactusinfo)
class ContactusinfoAdmin(admin.ModelAdmin):
    list_display = ('Address', 'ContactNo', 'EmailId')
    search_fields = ('EmailId', 'ContactNo')

@admin.register(Contactusquery)
class ContactusqueryAdmin(admin.ModelAdmin):
    list_display = ('Name', 'EmailId', 'Message', 'Status')
    list_filter = ('Status',)
    search_fields = ('Name', 'EmailId', 'Message')
