from django.contrib import admin
from .models import EconsultantAPIKeyModel, EconsultantSessionModel

@admin.register(EconsultantSessionModel)
class EconsultantSessionModelAdmin(admin.ModelAdmin):  
    list_display = ('id', 'user', 'token', 'created_at', 'expires_at')
    search_fields = ('id', 'user__username', 'token')

@admin.register(EconsultantAPIKeyModel)
class EconsultantAPIKeyModelAdmin(admin.ModelAdmin):  
    list_display = ('key', 'description', 'is_active', 'created_at')
    search_fields = ('key', 'description')
