from django.contrib import admin
from .models import Profile, Bonuses, Delivery

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'avatar')

admin.site.register(Profile, ProfileAdmin)


class BonusesAdmin(admin.ModelAdmin):
    list_display = ('user', 'summa', 'description', 'date')

admin.site.register(Bonuses, BonusesAdmin)

admin.site.register(Delivery)
