from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)

admin.site.register(Staff)

admin.site.register(Appointment)

admin.site.register(Blog)