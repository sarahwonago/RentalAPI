from django.contrib import admin

from .models import Payment, Penalty, MonthlyRent

admin.site.register(Payment)
admin.site.register(Penalty)
admin.site.register(MonthlyRent)
