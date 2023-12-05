from django.contrib import admin
from armsApp import models

# Register your models here.

admin.site.register(models.Airlines)
admin.site.register(models.Airport)
admin.site.register(models.Flights)
admin.site.register(models.Reservation)