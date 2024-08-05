from django.contrib import admin
from .models import HospitalAPIKeyModel, HospitalSessionModel

@admin.register(HospitalSessionModel)
class HospitalSessionModelAdmin(admin.ModelAdmin):  
    list_display = ('id', 'user', 'token', 'created_at', 'expires_at')
    search_fields = ('id', 'user__username', 'token')

@admin.register(HospitalAPIKeyModel)
class HospitalAPIKeyModelAdmin(admin.ModelAdmin):  
    list_display = ('key', 'description', 'is_active', 'created_at')
    search_fields = ('key', 'description')
