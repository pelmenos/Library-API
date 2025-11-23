from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number', 'email', 'registration_date']
    list_filter = ['registration_date']
    search_fields = ['first_name', 'last_name', 'phone_number']