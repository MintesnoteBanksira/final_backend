from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('full_name', 'location', 'farm_size', 'coffee_type', 'last_farming_time')}),
    )

admin.site.register(User, CustomUserAdmin)
