from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Municipality

admin.site.register(Municipality)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'municipality', 'ward_number']
    list_filter = ['role', 'municipality']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'phone', 'municipality', 'ward_number')}),
    )
