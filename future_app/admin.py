from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)

admin.site.register(Staff)

admin.site.register(Appointment)

admin.site.register(Blog)

admin.site.register(Notification)

admin.site.register(Contact)

admin.site.register(DesignPreference)

admin.site.register(Project)

admin.site.register(Subscription)

admin.site.register(Comment)