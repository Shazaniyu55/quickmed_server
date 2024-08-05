from django.contrib import admin
from .models import AmbulanceSessionModel, AmbulanceAPIKeyModel

@admin.register(AmbulanceSessionModel)
class AmbulanceSessionModelAdmin(admin.ModelAdmin):  
    list_display = ('id', 'user', 'token', 'created_at', 'expires_at')
    search_fields = ('id', 'user__username', 'token')

@admin.register(AmbulanceAPIKeyModel)
class AmbulanceAPIKeyModelAdmin(admin.ModelAdmin):  
    list_display = ('key', 'description', 'is_active', 'created_at')
    search_fields = ('key', 'description')
